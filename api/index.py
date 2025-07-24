from flask import Flask, jsonify, request
import random

app = Flask(__name__)

def letter_to_number(char):
    return str(ord(char.upper()) - 55)  # A=10, B=11, ..., Z=35

def calculate_check_digits(country_code, bban):
    rearranged = bban + country_code + "00"
    numeric_string = ''.join(letter_to_number(c) if c.isalpha() else c for c in rearranged)
    mod_result = int(numeric_string) % 97
    check_digits = 98 - mod_result
    return f"{check_digits:02d}"

def generate_iban(country="DE", bank_code="12345678", account_length=10):
    account_number = ''.join(str(random.randint(0, 9)) for _ in range(account_length))
    bban = bank_code + account_number
    check_digits = calculate_check_digits(country, bban)
    iban = f"{country}{check_digits}{bban}"
    return iban

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the IBAN Generator API"}), 200

@app.route("/generate", methods=["GET"])
def generate():
    country = request.args.get("country", "DE").upper()
    bank_code = request.args.get("bank", "12345678")
    account_length = int(request.args.get("length", 10))
    iban = generate_iban(country, bank_code, account_length)
    return jsonify({"iban": iban}), 200
