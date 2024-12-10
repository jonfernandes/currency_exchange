import streamlit as st
from dotenv import load_dotenv
import requests
import os
import json


# Streamlit application
def main():
    st.title("Holiday Currency Converter")
    EXCHANGE_API = os.getenv("EXCHANGE_API", "Your API key here if not using an env file")
    # Input amount in GBP
    AMOUNT = st.number_input("Enter amount in GBP:", min_value=0.0, value=0.0, step=0.01)

    # Currency options
    currency_options = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "INR": "Indian Rupee",
        "EGP": "Egyptian Pound",
        "SGD": "Singapore Dollar",
        "CAD": "Canadian Dollar"
    }
    
    # Dropdown menu for selecting target currency
    TARGET = st.selectbox("Select currency to convert to:", list(currency_options.keys()))
    print(f"TARGET: {TARGET}")
    print(f"AMOUNT: {AMOUNT}")
    # Convert and display the result
    if int(AMOUNT) > 0:
        try:
            BASE = "GBP"
            url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API}/pair/{BASE}/{TARGET}/{AMOUNT}"
            exchange_response = json.loads(requests.get(url).text)
            conversion_result = exchange_response["conversion_result"]
            print(f"conversion_result {conversion_result}")
            st.success(f"{AMOUNT} GBP is equal to {conversion_result} {TARGET}")
        except Exception as e:
            st.error(f"Error while converting currency: {str(e)}")

if __name__ == "__main__":
    main()