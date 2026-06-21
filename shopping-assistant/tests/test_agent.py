import pytest
from app.agent import redeem_discount_code, DISCOUNT_CODES, REDEEMED_BY

@pytest.fixture(autouse=True)
def setup_state():
    """Reset the global state before each test to ensure isolation."""
    DISCOUNT_CODES.clear()
    DISCOUNT_CODES.update({
        "WELCOME50": {"discount": "50%", "redeemed": False},
        "SUMMER20": {"discount": "20%", "redeemed": False},
    })
    REDEEMED_BY.clear()

def test_redeem_success():
    """Verify a valid discount code can be redeemed successfully."""
    user_id = "user_123"
    code = "WELCOME50"
    result = redeem_discount_code(code, user_id)

    assert "Success!" in result
    assert f"User {user_id} redeemed code {code}" in result
    assert DISCOUNT_CODES[code]["redeemed"] is True
    assert REDEEMED_BY[code] == user_id

def test_redeem_invalid_code():
    """Verify that an invalid discount code returns the correct error message."""
    result = redeem_discount_code("INVALID_CODE", "user_123")
    assert result == "Invalid discount code."
    # Ensure no state was modified
    for code in DISCOUNT_CODES:
        assert DISCOUNT_CODES[code]["redeemed"] is False

def test_redeem_already_redeemed():
    """Verify that a code cannot be redeemed more than once."""
    code = "SUMMER20"
    user_1 = "user_1"
    user_2 = "user_2"

    # First redemption
    redeem_discount_code(code, user_1)
    assert DISCOUNT_CODES[code]["redeemed"] is True

    # Second redemption attempt
    result = redeem_discount_code(code, user_2)
    assert f"The discount code {code} has already been redeemed." in result
    assert REDEEMED_BY[code] == user_1 # Should still be the first user

def test_redeem_case_insensitivity():
    """Verify that discount codes are treated case-insensitively."""
    user_id = "user_123"
    code_lower = "welcome50"
    result = redeem_discount_code(code_lower, user_id)

    assert "Success!" in result
    assert "WELCOME50" in result # The function converts to upper
    assert DISCOUNT_CODES["WELCOME50"]["redeemed"] is True

def test_redeem_empty_inputs():
    """Verify behavior with empty strings for code or user_id."""
    # Empty code should be invalid
    assert redeem_discount_code("", "user_1") == "Invalid discount code."
    # Empty user_id should still allow redemption in current implementation
    # (but state should be updated with empty string)
    result = redeem_discount_code("WELCOME50", "")
    assert "Success!" in result
    assert REDEEMED_BY["WELCOME50"] == ""
