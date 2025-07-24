from flask import Flask, request, jsonify
import random
import math

app = Flask(__name__)

# Country-specific BBAN generators with realistic structures
def generate_de():
    # Germany: 8 digit bank code + 10 digit account number
    bank_code = generate_numeric(8)
    account_number = generate_numeric(10)
    return bank_code + account_number

def generate_gb():
    # UK: 4 char bank code + 6 digit sort code + 8 digit account
    bank_code = generate_alpha(4)
    sort_code = generate_numeric(2) + "-" + generate_numeric(2) + "-" + generate_numeric(2)
    account_number = generate_numeric(8)
    return bank_code + sort_code.replace("-", "") + account_number

def generate_fr():
    # France: 5 digit bank code + 5 digit branch + 11 digit account + 2 digit key
    bank_code = generate_numeric(5)
    branch_code = generate_numeric(5)
    account_number = generate_numeric(11)
    key = generate_numeric(2)
    return bank_code + branch_code + account_number + key

def generate_nl():
    # Netherlands: 4 char bank code + 10 digit account
    bank_code = generate_alpha(4)
    account_number = generate_numeric(10)
    return bank_code + account_number

def generate_es():
    # Spain: 4 digit bank + 4 digit branch + 2 digit check + 10 digit account
    bank_code = generate_numeric(4)
    branch_code = generate_numeric(4)
    check_digits = generate_numeric(2)
    account_number = generate_numeric(10)
    return bank_code + branch_code + check_digits + account_number

def generate_it():
    # Italy: 1 char check + 5 digit ABIs + 5 digit CAB + 12 char account
    check_char = generate_alpha(1)
    abi = generate_numeric(5)
    cab = generate_numeric(5)
    account = generate_alphanum(12)
    return check_char + abi + cab + account

def generate_ch():
    # Switzerland: 5 digits + 12 alphanum
    bank_code = generate_numeric(5)
    account_number = generate_alphanum(12)
    return bank_code + account_number

def generate_be():
    # Belgium: 3 digit bank + 7 digit account + 2 digit check
    bank_code = generate_numeric(3)
    account_number = generate_numeric(7)
    check_digits = generate_numeric(2)
    return bank_code + account_number + check_digits

# Country-specific generators mapping
COUNTRY_GENERATORS = {
    "DE": {"length": 22, "generator": generate_de},
    "GB": {"length": 22, "generator": generate_gb},
    "FR": {"length": 27, "generator": generate_fr},
    "NL": {"length": 18, "generator": generate_nl},
    "ES": {"length": 24, "generator": generate_es},
    "IT": {"length": 27, "generator": generate_it},
    "CH": {"length": 21, "generator": generate_ch},
    "BE": {"length": 16, "generator": generate_be},
    # Add more countries as needed
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
    temp_iban = bban + country + "00"
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    
    mod = 0
    for i in range(0, len(numeric_str), 7):
        chunk = numeric_str[i:i+7]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"

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
