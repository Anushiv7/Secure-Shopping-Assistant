# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# In-memory store for single-use discount codes
DISCOUNT_CODES = {
    "WELCOME50": {"discount": "50%", "redeemed": False},
    "SUMMER20": {"discount": "20%", "redeemed": False},
}
REDEEMED_BY = {}

# In-memory store for shopping carts
CARTS = {
    "cart_1": {"user_id": "user_1", "total": 100.0, "status": "active"},
    "cart_2": {"user_id": "user_2", "total": 200.0, "status": "active"},
}


def redeem_discount_code(code: str, user_id: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem.
        user_id: The ID of the registered user redeeming the code.

    Returns:
        A message indicating whether the redemption was successful and the discount amount.
    """
    code = code.upper()
    if code not in DISCOUNT_CODES:
        return "Invalid discount code."

    if DISCOUNT_CODES[code]["redeemed"]:
        return f"The discount code {code} has already been redeemed."

    # Mark as redeemed and track which user used it
    DISCOUNT_CODES[code]["redeemed"] = True
    REDEEMED_BY[code] = user_id
    return f"Success! User {user_id} redeemed code {code} for a {DISCOUNT_CODES[code]['discount']} discount."


def process_cart_checkout(cart_id: str, discount_code: str = None, user_id: str = None) -> str:
    """Processes the checkout for a shopping cart, applying an optional discount code.

    Args:
        cart_id: The ID of the cart to checkout.
        discount_code: An optional discount code to apply.
        user_id: The ID of the user performing the checkout.

    Returns:
        A summary of the checkout process, including final price and discount applied.
    """
    if not cart_id:
        return "Error: Cart ID is required."

    cart = CARTS.get(cart_id)
    if not cart:
        return f"Error: Cart {cart_id} not found."

    if not user_id:
        return "Error: User ID is required for checkout."

    if cart["user_id"] != user_id:
        return f"Error: User {user_id} is not authorized to checkout cart {cart_id}."

    if cart["status"] == "processed":
        return f"Error: Cart {cart_id} has already been processed."

    total = cart["total"]
    applied_discount = 0.0
    discount_msg = "No discount applied."

    if discount_code:
        code = discount_code.upper()
        if code not in DISCOUNT_CODES:
            return f"Error: Invalid discount code {discount_code}."
        if DISCOUNT_CODES[code]["redeemed"]:
            return f"Error: Discount code {discount_code} has already been redeemed."

        # Calculate discount (e.g., "50%" -> 0.5)
        discount_percent = float(DISCOUNT_CODES[code]["discount"].strip("%")) / 100.0
        applied_discount = total * discount_percent
        final_total = total - applied_discount
        discount_msg = f"Discount {code} applied: -${applied_discount:.2f}"

        # Mark as redeemed
        DISCOUNT_CODES[code]["redeemed"] = True
        REDEEMED_BY[code] = user_id

    else:
        final_total = total

    final_total = max(0, final_total)
    cart["status"] = "processed"

    return (
        f"Checkout successful for cart {cart_id}!\n"
        f"Original Total: ${total:.2f}\n"
        f"Discount: {discount_msg}\n"
        f"Final Total: ${final_total:.2f}\n"
        f"Order processed for user {user_id}."
    )


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        api_key="AIzaSyD-mock-key-value-12345",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI shopping assistant for a retail store. You can help users with their shopping queries and redeem discount codes.",
    tools=[redeem_discount_code, process_cart_checkout, get_weather, get_current_time],
)

app = App(
    root_agent=root_agent,
    name="app",
)
