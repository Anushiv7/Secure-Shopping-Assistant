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
    tools=[redeem_discount_code, get_weather, get_current_time],
)

app = App(
    root_agent=root_agent,
    name="app",
)
