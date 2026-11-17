from django.test import TestCase
from django.urls import reverse

from . import tools
from .models import Item


class InventoryToolTests(TestCase):
    """The agent's tools are plain database code, so they can be tested without Gemini."""

    def setUp(self):
        Item.objects.create(name="Hammer", quantity=10, price="2.50")

    def test_check_stock_ignores_case(self):
        self.assertEqual(
            tools.check_stock("hAmMeR"),
            {"name": "Hammer", "quantity": 10, "price": 2.5},
        )

    def test_check_stock_unknown_item(self):
        self.assertIn("error", tools.check_stock("Anvil"))

    def test_add_item_creates_then_restocks(self):
        created = tools.add_item("Saw", 5, 12)
        self.assertTrue(created["created"])

        restocked = tools.add_item("saw", 3)
        self.assertFalse(restocked["created"])
        self.assertEqual(restocked["quantity"], 8)
        self.assertEqual(Item.objects.filter(name__iexact="saw").count(), 1)

    def test_remove_stock(self):
        self.assertEqual(tools.remove_stock("Hammer", 4)["quantity"], 6)

    def test_remove_stock_cannot_go_negative(self):
        result = tools.remove_stock("Hammer", 11)
        self.assertIn("error", result)
        self.assertEqual(Item.objects.get(name="Hammer").quantity, 10)

    def test_set_price_rejects_negative(self):
        self.assertIn("error", tools.set_price("Hammer", -1))
        self.assertEqual(float(Item.objects.get(name="Hammer").price), 2.5)

    def test_calculate_cost_with_vat(self):
        result = tools.calculate_cost("Hammer", 4, 10)
        self.assertEqual(result["subtotal"], 10.0)
        self.assertEqual(result["vat_amount"], 1.0)
        self.assertEqual(result["total"], 11.0)

    def test_calculate_cost_needs_a_price(self):
        Item.objects.create(name="Gift", quantity=1)
        self.assertIn("error", tools.calculate_cost("Gift", 1))

    def test_delete_item(self):
        self.assertEqual(tools.delete_item("Hammer"), {"deleted": "Hammer"})
        self.assertFalse(Item.objects.filter(name="Hammer").exists())


class ChatPageTests(TestCase):
    def test_chat_page_loads(self):
        response = self.client.get(reverse("chat"))
        self.assertEqual(response.status_code, 200)
