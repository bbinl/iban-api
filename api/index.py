from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Real format-based IBAN lengths and structures
IBAN_FORMATS = {
    "DE": {"length": 22, "bban": lambda: generate_numeric(18)},  # 8 (bank) + 10 (account)
    "GB": {"length": 22, "bban": lambda: generate_alpha(4) + generate_numeric(14)},  # bank code + sort + acc
    "NL": {"length": 18, "bban": lambda: generate_alpha(4) + generate_numeric(10)},
    "ES": {"length": 24, "bban": lambda: generate_numeric(20)},  # bank + branch + control + acc
    "FR": {"length": 27, "bban": lambda: generate_numeric(23) + generate_alpha(2)},  # bank + branch + acc + key
    "BD": {"length": 28, "bban": lambda: "BRAC" + generate_numeric(24)}  # Example fixed bank code
}

def generate_numeric(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_alpha(length):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

def letter_to_number(c):
    return str(ord(c.upper()) - 55) if c.isalpha() else c

def calculate_check_digits(country, bban):
    rearranged = bban + country + "00"
    numeric = ''.join(letter_to_number(c) for c in rearranged)
    mod = int(numeric) % 97
    return f"{98 - mod:02d}"

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Fully Valid IBAN Generator API!",
        "usage": "/generate?country=DE"
    })

@app.route("/generate")
def generate_iban():
    country = request.args.get("country", "").upper()

    if country not in IBAN_FORMATS:
        return jsonify({"error": f"Unsupported or invalid country code: {country}"}), 400

    bban = IBAN_FORMATS[country]["bban"]()
    check_digits = calculate_check_digits(country, bban)
    iban = f"{country}{check_digits}{bban}"

    if len(iban) != IBAN_FORMATS[country]["length"]:
        return jsonify({"error": f"IBAN length mismatch for {country}"}), 500

    return jsonify({"iban": iban})
