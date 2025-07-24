from flask import Flask, request, jsonify
import random
import math

app = Flask(__name__)

# Comprehensive IBAN formats with correct BBAN structures
IBAN_FORMATS = {
    "AL": {"length": 28, "bban": lambda: "0" + generate_numeric(3) + generate_numeric(4) + generate_alphanum(16)},
    "AD": {"length": 24, "bban": lambda: generate_numeric(4) + generate_numeric(4) + generate_alphanum(12)},
    "AT": {"length": 20, "bban": lambda: generate_numeric(5) + generate_numeric(11)},
    "AZ": {"length": 28, "bban": lambda: generate_alpha(4) + generate_alphanum(20)},
    "BH": {"length": 22, "bban": lambda: generate_alpha(4) + generate_alphanum(14)},
    "BE": {"length": 16, "bban": lambda: generate_numeric(3) + generate_numeric(7) + generate_numeric(2)},
    "BA": {"length": 20, "bban": lambda: generate_numeric(3) + generate_numeric(3) + generate_numeric(8) + generate_numeric(2)},
    "BR": {"length": 29, "bban": lambda: generate_numeric(8) + generate_numeric(5) + generate_numeric(10) + generate_alpha(1) + generate_alphanum(1)},
    "BG": {"length": 22, "bban": lambda: generate_alpha(4) + generate_numeric(4) + generate_numeric(2) + generate_alphanum(8)},
    "CR": {"length": 21, "bban": lambda: generate_numeric(4) + generate_numeric(14)},
    "HR": {"length": 21, "bban": lambda: generate_numeric(7) + generate_numeric(10)},
    "CY": {"length": 28, "bban": lambda: generate_numeric(3) + generate_numeric(5) + generate_alphanum(16)},
    "CZ": {"length": 24, "bban": lambda: generate_numeric(4) + generate_numeric(6) + generate_numeric(10)},
    "DK": {"length": 18, "bban": lambda: generate_numeric(4) + generate_numeric(9) + generate_numeric(1)},
    "DO": {"length": 28, "bban": lambda: generate_alpha(4) + generate_numeric(20)},
    "EE": {"length": 20, "bban": lambda: generate_numeric(2) + generate_numeric(2) + generate_numeric(11) + generate_numeric(1)},
    "FI": {"length": 18, "bban": lambda: generate_numeric(3) + generate_numeric(4) + generate_numeric(2) + generate_numeric(3) + generate_numeric(1)},
    "FR": {"length": 27, "bban": lambda: generate_numeric(5) + generate_numeric(5) + generate_alphanum(11) + generate_numeric(2)},
    "GE": {"length": 22, "bban": lambda: generate_alpha(2) + generate_numeric(16)},
    "DE": {"length": 22, "bban": lambda: generate_numeric(8) + generate_numeric(10)},
    "GI": {"length": 23, "bban": lambda: generate_alpha(4) + generate_alphanum(15)},
    "GR": {"length": 27, "bban": lambda: generate_numeric(3) + generate_numeric(4) + generate_alphanum(16)},
    "GL": {"length": 18, "bban": lambda: generate_numeric(4) + generate_numeric(9) + generate_numeric(1)},
    "HU": {"length": 28, "bban": lambda: generate_numeric(3) + generate_numeric(4) + generate_numeric(1) + generate_numeric(15) + generate_numeric(1)},
    "IS": {"length": 26, "bban": lambda: generate_numeric(4) + generate_numeric(2) + generate_numeric(6) + generate_numeric(10)},
    "IE": {"length": 22, "bban": lambda: generate_alpha(4) + generate_numeric(6) + generate_numeric(8)},
    "IL": {"length": 23, "bban": lambda: generate_numeric(3) + generate_numeric(3) + generate_numeric(13)},
    "IT": {"length": 27, "bban": lambda: generate_alpha(1) + generate_numeric(5) + generate_numeric(5) + generate_alphanum(12)},
    "JO": {"length": 30, "bban": lambda: generate_alpha(4) + generate_numeric(4) + generate_alphanum(18)},
    "KZ": {"length": 20, "bban": lambda: generate_numeric(3) + generate_alphanum(13)},
    "XK": {"length": 20, "bban": lambda: generate_numeric(4) + generate_numeric(10) + generate_numeric(2)},
    "KW": {"length": 30, "bban": lambda: generate_alpha(4) + generate_alphanum(22)},
    "LV": {"length": 21, "bban": lambda: generate_alpha(4) + generate_alphanum(13)},
    "LB": {"length": 28, "bban": lambda: generate_numeric(4) + generate_alphanum(20)},
    "LI": {"length": 21, "bban": lambda: generate_numeric(5) + generate_alphanum(12)},
    "LT": {"length": 20, "bban": lambda: generate_numeric(5) + generate_numeric(11)},
    "LU": {"length": 20, "bban": lambda: generate_numeric(3) + generate_alphanum(13)},
    "MK": {"length": 19, "bban": lambda: generate_numeric(3) + generate_alphanum(10) + generate_numeric(2)},
    "MT": {"length": 31, "bban": lambda: generate_alpha(4) + generate_numeric(5) + generate_alphanum(18)},
    "MR": {"length": 27, "bban": lambda: generate_numeric(5) + generate_numeric(5) + generate_numeric(11) + generate_numeric(2)},
    "MU": {"length": 30, "bban": lambda: generate_alpha(4) + generate_numeric(2) + generate_numeric(2) + generate_numeric(12) + generate_numeric(3) + generate_alpha(3)},
    "MD": {"length": 24, "bban": lambda: generate_alphanum(2) + generate_alphanum(18)},
    "MC": {"length": 27, "bban": lambda: generate_numeric(5) + generate_numeric(5) + generate_alphanum(11) + generate_numeric(2)},
    "ME": {"length": 22, "bban": lambda: generate_numeric(3) + generate_numeric(13) + generate_numeric(2)},
    "NL": {"length": 18, "bban": lambda: generate_alpha(4) + generate_numeric(10)},
    "NO": {"length": 15, "bban": lambda: generate_numeric(4) + generate_numeric(6) + generate_numeric(1)},
    "PK": {"length": 24, "bban": lambda: generate_alpha(4) + generate_alphanum(16)},
    "PS": {"length": 29, "bban": lambda: generate_alpha(4) + generate_alphanum(21)},
    "PL": {"length": 28, "bban": lambda: generate_numeric(8) + generate_numeric(16)},
    "PT": {"length": 25, "bban": lambda: generate_numeric(4) + generate_numeric(4) + generate_numeric(11) + generate_numeric(2)},
    "QA": {"length": 29, "bban": lambda: generate_alpha(4) + generate_alphanum(21)},
    "RO": {"length": 24, "bban": lambda: generate_alpha(4) + generate_alphanum(16)},
    "SM": {"length": 27, "bban": lambda: generate_alpha(1) + generate_numeric(5) + generate_numeric(5) + generate_alphanum(12)},
    "SA": {"length": 24, "bban": lambda: generate_numeric(2) + generate_alphanum(18)},
    "RS": {"length": 22, "bban": lambda: generate_numeric(3) + generate_numeric(13) + generate_numeric(2)},
    "SK": {"length": 24, "bban": lambda: generate_numeric(4) + generate_numeric(6) + generate_numeric(10)},
    "SI": {"length": 19, "bban": lambda: generate_numeric(5) + generate_numeric(8) + generate_numeric(2)},
    "ES": {"length": 24, "bban": lambda: generate_numeric(4) + generate_numeric(4) + generate_numeric(1) + generate_numeric(1) + generate_numeric(10)},
    "SE": {"length": 24, "bban": lambda: generate_numeric(3) + generate_numeric(16) + generate_numeric(1)},
    "CH": {"length": 21, "bban": lambda: generate_numeric(5) + generate_alphanum(12)},
    "TN": {"length": 24, "bban": lambda: generate_numeric(2) + generate_numeric(3) + generate_numeric(13) + generate_numeric(2)},
    "TR": {"length": 26, "bban": lambda: generate_numeric(5) + generate_alphanum(1) + generate_alphanum(16)},
    "AE": {"length": 23, "bban": lambda: generate_numeric(3) + generate_numeric(16)},
    "GB": {"length": 22, "bban": lambda: generate_alpha(4) + generate_numeric(6) + generate_numeric(8)},
    "VA": {"length": 22, "bban": lambda: generate_numeric(3) + generate_numeric(15)},
    "VG": {"length": 24, "bban": lambda: generate_alpha(4) + generate_numeric(16)}
}

def generate_numeric(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_alpha(length):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

def generate_alphanum(length):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(chars) for _ in range(length))

def letter_to_number(c):
    return str(ord(c.upper()) - 55) if c.isalpha() else c

def calculate_check_digits(country, bban):
    # Prepare the string for checksum calculation
    temp_iban = bban + country + "00"
    # Convert letters to numbers
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    # Compute MOD 97
    mod = 0
    for i in range(0, len(numeric_str), 7):
        chunk = numeric_str[i:i+7]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Fully Valid IBAN Generator API!",
        "usage": "/generate?country=DE",
        "supported_countries": list(IBAN_FORMATS.keys())
    })

@app.route("/generate")
def generate_iban():
    country = request.args.get("country", "").upper()

    if country not in IBAN_FORMATS:
        return jsonify({
            "error": f"Unsupported country code: {country}",
            "supported_countries": list(IBAN_FORMATS.keys())
        }), 400

    # Generate BBAN according to country's format
    bban = IBAN_FORMATS[country]["bban"]()
    
    # Calculate check digits
    check_digits = calculate_check_digits(country, bban)
    
    # Construct IBAN
    iban = f"{country}{check_digits}{bban}"

    # Verify length
    if len(iban) != IBAN_FORMATS[country]["length"]:
        return jsonify({
            "error": f"Generated IBAN length mismatch for {country}",
            "expected_length": IBAN_FORMATS[country]["length"],
            "actual_length": len(iban)
        }), 500

    return jsonify({
        "iban": iban,
        "country": country,
        "valid": True,
        "length": len(iban)
    })

if __name__ == "__main__":
    app.run(debug=True)
