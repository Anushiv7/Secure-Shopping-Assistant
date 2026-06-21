import pytest
from app.agent import process_cart_checkout, CARTS, DISCOUNT_CODES, REDEEMED_BY

@pytest.fixture(autouse=True)
def setup_state():
    """Reset the global state before each test."""
    CARTS.clear()
    CARTS.update({
        "cart_1": {"user_id": "user_1", "total": 100.0, "status": "active"},
        "cart_2": {"user_id": "user_2", "total": 200.0, "status": "active"},
    })
    DISCOUNT_CODES.clear()
    DISCOUNT_CODES.update({
        "WELCOME50": {"discount": "50%", "redeemed": False},
        "SUMMER20": {"discount": "20%", "redeemed": False},
    })
    REDEEMED_BY.clear()

def test_checkout_success_no_discount():
    result = process_cart_checkout(cart_id="cart_1", user_id="user_1")
    assert "Checkout successful" in result
    assert "Final Total: $100.00" in result
    assert CARTS["cart_1"]["status"] == "processed"

def test_checkout_success_with_discount():
    result = process_cart_checkout(cart_id="cart_1", discount_code="WELCOME50", user_id="user_1")
    assert "Checkout successful" in result
    assert "Discount WELCOME50 applied: -$50.00" in result
    assert "Final Total: $50.00" in result
    assert DISCOUNT_CODES["WELCOME50"]["redeemed"] is True
    assert REDEEMED_BY["WELCOME50"] == "user_1"

def test_checkout_invalid_cart():
    result = process_cart_checkout(cart_id="non_existent", user_id="user_1")
    assert "Error: Cart non_existent not found" in result

def test_checkout_wrong_user():
    # User 2 tries to checkout User 1's cart
    result = process_cart_checkout(cart_id="cart_1", user_id="user_2")
    assert "Error: User user_2 is not authorized to checkout cart cart_1" in result
    assert CARTS["cart_1"]["status"] == "active"

def test_checkout_already_processed():
    process_cart_checkout(cart_id="cart_1", user_id="user_1")
    result = process_cart_checkout(cart_id="cart_1", user_id="user_1")
    assert "Error: Cart cart_1 has already been processed" in result

def test_checkout_already_redeemed_discount():
    # First use
    process_cart_checkout(cart_id="cart_1", discount_code="WELCOME50", user_id="user_1")
    # Second use on different cart
    result = process_cart_checkout(cart_id="cart_2", discount_code="WELCOME50", user_id="user_2")
    assert "Error: Discount code WELCOME50 has already been redeemed" in result

def test_checkout_invalid_discount_code():
    result = process_cart_checkout(cart_id="cart_1", discount_code="FAKECODE", user_id="user_1")
    assert "Error: Invalid discount code FAKECODE" in result
