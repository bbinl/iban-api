from flask import Flask, request, jsonify
import random
import math
from collections import defaultdict

app = Flask(__name__)

# Country-specific data structures
country_data = {
    "DE": {
        "length": 22,
        "bank_code_length": 8,
        "account_length": 10,
        "bank_codes": ["50010517", "10000000", "20000000", "30000000"]
    },
    "GB": {
        "length": 22,
        "bank_codes": ["BARC", "LOYD", "NWBK"],
        "sort_codes": ["200318", "200326", "200353", "200378"],
        "account_length": 8
    },
    "NL": {
        "length": 18,
        "bank_codes": ["ABNA", "INGB", "RABO"],
        "account_length": 10
    }
}

def generate_numeric(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_alpha(length):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

def letter_to_number(c):
    return str(ord(c.upper()) - 55) if c.isalpha() else c

def calculate_check_digits(country, bban):
    temp_iban = bban + country + "00"
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    
    mod = 0
    for i in range(0, len(numeric_str), 7):
        chunk = numeric_str[i:i+7]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"

def generate_de():
    data = country_data["DE"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number

def generate_gb():
    data = country_data["GB"]
    # For GB, BBAN typically consists of bank code (alpha), sort code (numeric), and account number (numeric)
    bank_code = random.choice(data["bank_codes"])
    sort_code = random.choice(data["sort_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number

def generate_nl():
    data = country_data["NL"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number

COUNTRY_GENERATORS = {
    "DE": {"length": 22, "generator": generate_de},
    "GB": {"length": 22, "generator": generate_gb},
    "NL": {"length": 18, "generator": generate_nl}
}

@app.route("/")
def home():
    return jsonify({
        "message": "Enhanced IBAN Generator with Realistic Bank Details",
        "usage": "/generate?country=DE",
        "supported_countries": list(COUNTRY_GENERATORS.keys())
    })

@app.route("/generate")
def generate_iban():
    country = request.args.get("country", "").upper()

    if country not in COUNTRY_GENERATORS:
        return jsonify({
            "error": f"Unsupported country code: {country}",
            "supported_countries": list(COUNTRY_GENERATORS.keys())
        }), 400

    # Generate BBAN with country-specific structure
    bban = COUNTRY_GENERATORS[country]["generator"]()
    check_digits = calculate_check_digits(country, bban)
    iban = f"{country}{check_digits}{bban}"

    # Verify length
    if len(iban) != COUNTRY_GENERATORS[country]["length"]:
        return jsonify({
            "error": f"Generated IBAN length mismatch for {country}",
            "expected_length": COUNTRY_GENERATORS[country]["length"],
            "actual_length": len(iban)
        }), 500

    return jsonify({
        "iban": iban,
        "country": country,
        "valid": True,
        "length": len(iban),
        "details": {
            "bban": bban,
            "check_digits": check_digits
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
