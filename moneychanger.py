import streamlit as st
import os
from dotenv import load_dotenv
import openai
import requests
import json

from openai import OpenAI
from langsmith import traceable

# Load environment variables from .env file
load_dotenv()

# Amazon Currency Converter API URL (replace with the actual API URL if needed)
EXCHANGE_API = "https://api.exchangerate-api.com/v4/latest/USD"
EXCHANGERATE_API_KEY = os.getenv("EXCHANGE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "streamlit-moneychanger"
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o"


endpoint = os.environ["ENDPOINT"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
# Streamlit app title
st.title("Multilingual Money Changer")

# Text input for user to enter data or currency
user_input = st.text_input("Enter the amount and currency. Non-english languages supported. (e.g., '100 USD to EUR' or '100 US money to England money'):")

tools = [
    {
        "type": "function",
        "function": {
            "name" : "get_currency_exchange",
            "description" : "Convert a given amount of money from one currency to another. Each currency will have a three letter code",
            "parameters": {
                "type": "object",
                "properties": {
                  "base": {
                      "type": "string",
                      "description": "The base or original currency"
                  },
                "target": {
                    "type": "string",
                    "description": "The target or converted currency"
                },
                "amount": {
                    "type": "string",
                    "description": "The amount of money to convert from the base currency"
                }
                }
            },
            "required": ["base", "target", "amount"]
        }
    }
]

@traceable
def get_exchange_rate(base: str, target: str, amount: str) -> dict:
    """Return conversion result from exchangerate-api.com"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    exchange_response = json.loads(requests.get(url).text)
    return f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}'

@traceable(
    metadata={"model_name": MODEL_NAME, "model_provider": MODEL_PROVIDER}
)
def call_llm(text, tools=None):
    try:
        completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": text}],
        tools=tools,
        )
    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return completion

@traceable
def run_moneychanger(user_input=None, tools=None):
    completion = call_llm(user_input, tools)
    print(f"--> {completion.choices[0].finish_reason}")
    if completion.choices[0].finish_reason == "tool_calls":
        response_arguments = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
        base = response_arguments['base']
        target = response_arguments['target']
        amount = response_arguments['amount']
        st.write(get_exchange_rate(base, target, amount))
    elif completion.choices[0].finish_reason == "stop":
        st.write(f"(Function calling not used): {completion.choices[0].message.content}")
    else:
        st.write("NotImplemented")


# Button to submit the input
if st.button("Submit"):
    if user_input:
        run_moneychanger(user_input, tools)
    else:
        st.write("Please enter a value.")