from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Country-specific IBAN structure
IBAN_FORMATS = {
    "DE": {"length": 22, "bank_code_len": 8, "account_len": 10},
    "GB": {"length": 22, "bank_code_len": 10, "account_len": 8},  # Sort + Acc
    "NL": {"length": 18, "bank_code_len": 4, "account_len": 10},
    "ES": {"length": 24, "bank_code_len": 8, "account_len": 12},
    "FR": {"length": 27, "bank_code_len": 10, "account_len": 13},
    "BD": {"length": 28, "bank_code_len": 4, "account_len": 22}
}

def letter_to_number(char):
    return str(ord(char.upper()) - 55)

def calculate_check_digits(country_code, bban):
    rearranged = bban + country_code + "00"
    numeric_string = ''.join(letter_to_number(c) if c.isalpha() else c for c in rearranged)
    mod_result = int(numeric_string) % 97
    check_digits = 98 - mod_result
    return f"{check_digits:02d}"

def generate_random_numeric(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_iban(country_code):
    country_code = country_code.upper()

    if country_code not in IBAN_FORMATS:
        return None, f"Unsupported or invalid country code '{country_code}'"

    fmt = IBAN_FORMATS[country_code]
    bank_code = generate_random_numeric(fmt["bank_code_len"])
    account_number = generate_random_numeric(fmt["account_len"])
    bban = bank_code + account_number
    check_digits = calculate_check_digits(country_code, bban)
    iban = f"{country_code}{check_digits}{bban}"
    
    # Final check
    if len(iban) != fmt["length"]:
        return None, f"Generated IBAN length mismatch for {country_code}"

    return iban, None

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Advanced IBAN Generator API",
        "usage": "/generate?country=DE"
    })

@app.route("/generate", methods=["GET"])
def generate():
    country = request.args.get("country", "").upper()

    if not country:
        return jsonify({"error": "Missing required 'country' parameter"}), 400

    iban, error = generate_iban(country)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"iban": iban})
