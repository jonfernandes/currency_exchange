import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Title for the Streamlit app
st.title('Currency Converter')

# Input field for the amount in GBP
amount_gbp = st.number_input('Enter amount in GBP:', min_value=0.0, format="%.2f")

# Dropdown for selecting the target currency
target_currency = st.selectbox('Convert to:', ['USD', 'CAD', 'EUR', 'SGD'])

# Button to initiate conversion
if st.button('Submit'):
    if amount_gbp > 0:
        # ExchangeRate-API endpoint and parameters
        api_key = os.getenv("EXCHANGE_API", "Replace with your actual ExchangeRate-API key")
        api_url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP'

        try:
            # Making API request
            response = requests.get(api_url)
            data = response.json()

            # Check if API response is successful
            if response.status_code == 200:
                # Currency conversion
                exchange_rate = data['conversion_rates'].get(target_currency, None)

                if exchange_rate is not None:
                    converted_amount = amount_gbp * exchange_rate
                    st.success(f'{amount_gbp:.2f} GBP is equal to {converted_amount:.2f} {target_currency}.')
                else:
                    st.error('Failed to retrieve exchange rate for the selected currency.')
            else:
                st.error(f"Error from ExchangeRate-API: {data.get('error-type', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Please enter a valid amount in GBP.")