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
    "FR": {
        "length": 27,
        "bank_code_length": 5,
        "branch_code_length": 5,
        "account_length": 11,
        "key_length": 2
    },
    "NL": {
        "length": 18,
        "bank_codes": ["ABNA", "INGB", "RABO"],
        "account_length": 10
    },
    "ES": {
        "length": 24,
        "bank_code_length": 4,
        "branch_code_length": 4,
        "check_digits_length": 2,
        "account_length": 10
    },
    "IT": {
        "length": 27,
        "check_char": True,
        "bank_code_length": 5,
        "branch_code_length": 5,
        "account_length": 12
    },
    "CH": {
        "length": 21,
        "bank_code_length": 5,
        "account_length": 12
    },
    "BE": {
        "length": 16,
        "bank_code_length": 3,
        "account_length": 7,
        "check_digits_length": 2
    },
    "AT": {
        "length": 20,
        "bank_code_length": 5,
        "account_length": 11
    },
    "PL": {
        "length": 28,
        "bank_code_length": 8,
        "account_length": 16
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
    bank_code = random.choice(data["bank_codes"])
    sort_code = random.choice(data["sort_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + sort_code + account_number

def generate_fr():
    data = country_data["FR"]
    bank_code = generate_numeric(data["bank_code_length"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_numeric(data["account_length"])
    key = generate_numeric(data["key_length"])
    return bank_code + branch_code + account_number + key

def generate_nl():
    data = country_data["NL"]
    bank_code = random.choice(data["bank_codes"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number

def generate_es():
    data = country_data["ES"]
    bank_code = generate_numeric(data["bank_code_length"])
    branch_code = generate_numeric(data["branch_code_length"])
    check_digits = generate_numeric(data["check_digits_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + branch_code + check_digits + account_number

def generate_it():
    data = country_data["IT"]
    bank_code = generate_numeric(data["bank_code_length"])
    branch_code = generate_numeric(data["branch_code_length"])
    account_number = generate_alphanum(data["account_length"])
    
    # Calculate Italian check character (CIN)
    cin_map = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
    digit_map = {0:1, 1:0, 2:5, 3:7, 4:9, 5:13, 6:15, 7:17, 8:19, 9:21}
    
    even_sum = sum(int(bank_code[i]) + int(branch_code[i]) for i in range(1, 5, 2))
    odd_sum = sum(digit_map[int(bank_code[i])] + digit_map[int(branch_code[i])] for i in range(0, 5, 2))
    total = (odd_sum + even_sum) % 26
    cin = cin_map[total]
    
    return cin + bank_code + branch_code + account_number

def generate_ch():
    data = country_data["CH"]
    bank_code = generate_numeric(data["bank_code_length"])
    account_number = generate_alphanum(data["account_length"])
    return bank_code + account_number

def generate_be():
    data = country_data["BE"]
    bank_code = generate_numeric(data["bank_code_length"])
    account_number = generate_numeric(data["account_length"])
    
    # Calculate Belgian check digits
    base = bank_code + account_number
    check = 97 - (int(base) % 97)
    check_digits = f"{check:02d}"
    
    return bank_code + account_number + check_digits

def generate_at():
    data = country_data["AT"]
    bank_code = generate_numeric(data["bank_code_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number

def generate_pl():
    data = country_data["PL"]
    bank_code = generate_numeric(data["bank_code_length"])
    account_number = generate_numeric(data["account_length"])
    return bank_code + account_number

COUNTRY_GENERATORS = {
    "DE": {"length": 22, "generator": generate_de},
    "GB": {"length": 22, "generator": generate_gb},
    "FR": {"length": 27, "generator": generate_fr},
    "NL": {"length": 18, "generator": generate_nl},
    "ES": {"length": 24, "generator": generate_es},
    "IT": {"length": 27, "generator": generate_it},
    "CH": {"length": 21, "generator": generate_ch},
    "BE": {"length": 16, "generator": generate_be},
    "AT": {"length": 20, "generator": generate_at},
    "PL": {"length": 28, "generator": generate_pl}
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
