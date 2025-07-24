from flask import Flask, request, jsonify
import random
import math
from collections import defaultdict
import re

app = Flask(__name__)

# Enhanced country data with more comprehensive information
country_data = {
    "AD": {"length": 24, "structure": "F04F04A12", "bank_code_length": 4, "branch_code_length": 4, "account_length": 12},
    "AL": {"length": 28, "structure": "F08A16", "bank_code_length": 8, "account_length": 16},
    "AT": {"length": 20, "structure": "F05N11", "bank_code_length": 5, "account_length": 11},
    "AZ": {"length": 28, "structure": "F04A20", "bank_code_length": 4, "account_length": 20},
    "BA": {"length": 20, "structure": "F03N03N08N02", "bank_code_length": 3, "branch_code_length": 3, "account_length": 8, "check_digits_length": 2},
    "BE": {"length": 16, "structure": "F03N07N02", "bank_code_length": 3, "account_length": 7, "check_digits_length": 2},
    "BG": {"length": 22, "structure": "F04A04N08", "bank_code_length": 4, "branch_code_length": 4, "account_length": 8},
    "BH": {"length": 22, "structure": "F04A14", "bank_code_length": 4, "account_length": 14},
    "BR": {"length": 29, "structure": "F08N05N10A01", "bank_code_length": 8, "branch_code_length": 5, "account_length": 10, "account_type": 1},
    "CH": {"length": 21, "structure": "F05A12", "bank_code_length": 5, "account_length": 12},
    "CR": {"length": 21, "structure": "F04N14", "bank_code_length": 4, "account_length": 14},
    "CY": {"length": 28, "structure": "F03N05A16", "bank_code_length": 3, "branch_code_length": 5, "account_length": 16},
    "CZ": {"length": 24, "structure": "F04N06N10", "bank_code_length": 4, "account_prefix": 6, "account_length": 10},
    "DE": {"length": 22, "structure": "F08N10", "bank_code_length": 8, "account_length": 10},
    "DK": {"length": 18, "structure": "F04N10", "bank_code_length": 4, "account_length": 10},
    "DO": {"length": 28, "structure": "F04N20", "bank_code_length": 4, "account_length": 20},
    "EE": {"length": 20, "structure": "F02N02N11N01", "bank_code_length": 2, "branch_code_length": 2, "account_length": 11, "check_digit_length": 1},
    "ES": {"length": 24, "structure": "F04N04N02N10", "bank_code_length": 4, "branch_code_length": 4, "check_digits_length": 2, "account_length": 10},
    "FI": {"length": 18, "structure": "F06N07N01", "bank_code_length": 6, "account_length": 7, "check_digit_length": 1},
    "FO": {"length": 18, "structure": "F04N09N01", "bank_code_length": 4, "account_length": 9, "check_digit_length": 1},
    "FR": {"length": 27, "structure": "F05N05A11N02", "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "key_length": 2},
    "GB": {"length": 22, "structure": "F04N06N08", "bank_code_length": 4, "sort_code_length": 6, "account_length": 8},
    "GE": {"length": 22, "structure": "F02N16", "bank_code_length": 2, "account_length": 16},
    "GI": {"length": 23, "structure": "F04A15", "bank_code_length": 4, "account_length": 15},
    "GL": {"length": 18, "structure": "F04N10", "bank_code_length": 4, "account_length": 10},
    "GR": {"length": 27, "structure": "F03N04A16", "bank_code_length": 3, "branch_code_length": 4, "account_length": 16},
    "GT": {"length": 28, "structure": "F04A20", "bank_code_length": 4, "account_length": 20},
    "HR": {"length": 21, "structure": "F07N10", "bank_code_length": 7, "account_length": 10},
    "HU": {"length": 28, "structure": "F03N04N01N15N01", "bank_code_length": 3, "branch_code_length": 4, "check_digit_length": 1, "account_length": 15, "national_check_digit": 1},
    "IE": {"length": 22, "structure": "F04N06N08", "bank_code_length": 4, "branch_code_length": 6, "account_length": 8},
    "IL": {"length": 23, "structure": "F03N03N13", "bank_code_length": 3, "branch_code_length": 3, "account_length": 13},
    "IS": {"length": 26, "structure": "F04N02N06N10", "bank_code_length": 4, "branch_code_length": 2, "account_length": 6, "identification_number": 10},
    "IT": {"length": 27, "structure": "A01F05N05A12", "check_char": True, "bank_code_length": 5, "branch_code_length": 5, "account_length": 12},
    "KW": {"length": 30, "structure": "F04A22", "bank_code_length": 4, "account_length": 22},
    "KZ": {"length": 20, "structure": "F03N13", "bank_code_length": 3, "account_length": 13},
    "LB": {"length": 28, "structure": "F04A20", "bank_code_length": 4, "account_length": 20},
    "LI": {"length": 21, "structure": "F05A12", "bank_code_length": 5, "account_length": 12},
    "LT": {"length": 20, "structure": "F05N11", "bank_code_length": 5, "account_length": 11},
    "LU": {"length": 20, "structure": "F03A13", "bank_code_length": 3, "account_length": 13},
    "LV": {"length": 21, "structure": "F04A13", "bank_code_length": 4, "account_length": 13},
    "MC": {"length": 27, "structure": "F05N05A11N02", "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "key_length": 2},
    "MD": {"length": 24, "structure": "F02A18", "bank_code_length": 2, "account_length": 18},
    "ME": {"length": 22, "structure": "F03N13N02", "bank_code_length": 3, "account_length": 13, "check_digits_length": 2},
    "MK": {"length": 19, "structure": "F03A10N02", "bank_code_length": 3, "account_length": 10, "check_digits_length": 2},
    "MR": {"length": 27, "structure": "F05N05N11N02", "bank_code_length": 5, "branch_code_length": 5, "account_length": 11, "check_digits_length": 2},
    "MT": {"length": 31, "structure": "F04A05N18", "bank_code_length": 4, "branch_code_length": 5, "account_length": 18},
    "MU": {"length": 30, "structure": "F04N02N02N12N03N03", "bank_code_length": 4, "branch_code_length": 2, "account_length": 12, "currency_code": 3, "account_type": 3},
    "NL": {"length": 18, "structure": "F04N10", "bank_code_length": 4, "account_length": 10},
    "NO": {"length": 15, "structure": "F04N06N01", "bank_code_length": 4, "account_length": 6, "check_digit_length": 1},
    "PK": {"length": 24, "structure": "F04A16", "bank_code_length": 4, "account_length": 16},
    "PL": {"length": 28, "structure": "F08N16", "bank_code_length": 8, "account_length": 16},
    "PS": {"length": 29, "structure": "F04A21", "bank_code_length": 4, "account_length": 21},
    "PT": {"length": 25, "structure": "F04N04N11N02", "bank_code_length": 4, "branch_code_length": 4, "account_length": 11, "check_digits_length": 2},
    "QA": {"length": 29, "structure": "F04A21", "bank_code_length": 4, "account_length": 21},
    "RO": {"length": 24, "structure": "F04A16", "bank_code_length": 4, "account_length": 16},
    "RS": {"length": 22, "structure": "F03N13N02", "bank_code_length": 3, "account_length": 13, "check_digits_length": 2},
    "SA": {"length": 24, "structure": "F02N18", "bank_code_length": 2, "account_length": 18},
    "SC": {"length": 31, "structure": "F04N02N02N16N03", "bank_code_length": 4, "branch_code_length": 2, "account_length": 16, "currency_code": 3},
    "SE": {"length": 24, "structure": "F03N17", "bank_code_length": 3, "account_length": 17},
    "SI": {"length": 19, "structure": "F05N08N02", "bank_code_length": 5, "account_length": 8, "check_digits_length": 2},
    "SK": {"length": 24, "structure": "F04N06N10", "bank_code_length": 4, "account_prefix": 6, "account_length": 10},
    "SM": {"length": 27, "structure": "A01F05N05A12", "check_char": True, "bank_code_length": 5, "branch_code_length": 5, "account_length": 12},
    "ST": {"length": 25, "structure": "F04N04N11N02", "bank_code_length": 4, "branch_code_length": 4, "account_length": 11, "check_digits_length": 2},
    "SV": {"length": 28, "structure": "F04A20", "bank_code_length": 4, "account_length": 20},
    "TL": {"length": 23, "structure": "F03N14N02", "bank_code_length": 3, "account_length": 14, "check_digits_length": 2},
    "TN": {"length": 24, "structure": "F02N03N13N02", "bank_code_length": 2, "branch_code_length": 3, "account_length": 13, "check_digits_length": 2},
    "TR": {"length": 26, "structure": "F05N01A16", "bank_code_length": 5, "reserved": 1, "account_length": 16},
    "UA": {"length": 29, "structure": "F06A19", "bank_code_length": 6, "account_length": 19},
    "VA": {"length": 22, "structure": "F03N15", "bank_code_length": 3, "account_length": 15},
    "VG": {"length": 24, "structure": "F04A16", "bank_code_length": 4, "account_length": 16},
    "XK": {"length": 20, "structure": "F04N10N02", "bank_code_length": 4, "account_length": 10, "check_digits_length": 2}
}

# Predefined bank codes and other country-specific data
country_specific_data = {
    "GB": {
        "bank_codes": ["BARC", "LOYD", "NWBK", "HSBC", "RBOS", "ABBY"],
        "sort_codes": ["200318", "200326", "200353", "200378", "200380", "200384", "200395", "200401", "200404"]
    },
    "NL": {
        "bank_codes": ["ABNA", "INGB", "RABO", "SNSB", "ASNB", "FRBK", "KNAB", "RBRB", "TRUI", "FVLB"],
        "account_numbers": ["3767744449", "8849764685", "1679475908", "7568468658", "7356737620"]
    },
    "DE": {
        "bank_codes": ["50010517", "10000000", "20000000", "30000000", "40000000", "50000000"]
    },
    "FR": {
        "bank_codes": ["30002", "30003", "30006", "30056", "30066", "30123"]
    },
    "IT": {
        "bank_codes": ["03002", "03225", "03359", "03440", "03515", "03601"]
    },
    "ES": {
        "bank_codes": ["2100", "2095", "0081", "2080", "0182", "0487", "0075", "3190", "2038", "1465"]
    }
}

def generate_numeric(length):
    """Generate a random numeric string of given length"""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_alpha(length):
    """Generate a random alphabetic string of given length"""
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

def generate_alphanum(length):
    """Generate a random alphanumeric string of given length"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def letter_to_number(c):
    """Convert letter to number (A=10, B=11, ..., Z=35)"""
    return str(ord(c.upper()) - 55) if c.isalpha() else c

def calculate_check_digits(country, bban):
    """Calculate IBAN check digits using mod-97 algorithm"""
    temp_iban = bban + country + "00"
    numeric_str = ''.join(letter_to_number(c) for c in temp_iban)
    
    mod = 0
    for i in range(0, len(numeric_str), 7):
        chunk = numeric_str[i:i+7]
        mod = (mod * (10 ** len(chunk)) + int(chunk)) % 97
    check_digits = 98 - mod
    return f"{check_digits:02d}"

def generate_iban_for_country(country_code):
    """Generate IBAN for a specific country with proper structure"""
    if country_code not in country_data:
        raise ValueError(f"Unsupported country code: {country_code}")
    
    country_info = country_data[country_code]
    
    # Get country-specific data if available
    specific_data = country_specific_data.get(country_code, {})
    
    # Generate BBAN according to country structure
    bban_parts = []
    structure_parts = re.findall(r'([FAN])(\d+)', country_info["structure"])
    
    for part_type, part_length in structure_parts:
        part_length = int(part_length)
        
        if part_type == 'F':  # Fixed format (bank/branch codes)
            if country_code in specific_data and "bank_codes" in specific_data:
                # Use predefined bank codes if available
                bban_parts.append(random.choice(specific_data["bank_codes"]))
            else:
                # Generate random numeric
                bban_parts.append(generate_numeric(part_length))
        
        elif part_type == 'N':  # Numeric
            bban_parts.append(generate_numeric(part_length))
        
        elif part_type == 'A':  # Alphanumeric
            # Special handling for Italian check character
            if country_code == "IT" and len(bban_parts) == 0:
                # Generate Italian check character (CIN)
                # This will be calculated after generating other parts
                placeholder = "X"
                bban_parts.append(placeholder)
            else:
                bban_parts.append(generate_alphanum(part_length))
    
    # Special handling for countries with complex validation
    if country_code == "IT":
        # Calculate Italian check character (CIN)
        bank_code = bban_parts[1]  # F05 part
        branch_code = bban_parts[2]  # N05 part
        account_number = bban_parts[3]  # A12 part
        
        cin_map = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
        digit_map = {0:1, 1:0, 2:5, 3:7, 4:9, 5:13, 6:15, 7:17, 8:19, 9:21}
        
        # Calculate sums for CIN
        even_sum = sum(int(bank_code[i]) + int(branch_code[i]) for i in range(1, 5, 2))
        odd_sum = sum(digit_map[int(bank_code[i])] + digit_map[int(branch_code[i])] for i in range(0, 5, 2))
        
        # Add account number digits to sums (adjusted for alphanumeric)
        for char in account_number:
            if char.isdigit():
                odd_sum += digit_map[int(char)]
            else: # Alphabetic character
                odd_sum += digit_map[ord(char.upper()) - 55] # A=10, B=11, etc.
                
        total = (odd_sum + even_sum) % 26
        cin = cin_map[total]
        bban_parts[0] = cin
    
    elif country_code == "BE":
        # Belgian check digits
        bank_code = bban_parts[0]
        account_number = bban_parts[1]
        base = bank_code + account_number
        check = 97 - (int(base) % 97)
        bban_parts.append(f"{check:02d}")
    
    elif country_code == "NO":
        # Norwegian check digit
        account_base = bban_parts[0] + bban_parts[1]
        weights = [5,4,3,2,7,6,5,4,3,2]
        total = sum(int(account_base[i]) * weights[i] for i in range(10))
        check_digit = (11 - (total % 11)) % 11
        if check_digit == 10:
            # Try again with a different account number
            return generate_iban_for_country(country_code)
        bban_parts.append(str(check_digit))
    
    bban = ''.join(bban_parts)
    
    # Calculate IBAN check digits
    check_digits = calculate_check_digits(country_code, bban)
    iban = f"{country_code}{check_digits}{bban}"
    
    # Verify length
    if len(iban) != country_info["length"]:
        raise ValueError(f"Generated IBAN length mismatch for {country_code}")
    
    return iban, bban, check_digits

@app.route("/")
def home():
    return jsonify({
        "message": "Enhanced IBAN Generator API",
        "usage": "/generate?country=DE&count=5",
        "supported_countries": list(country_data.keys())
    })

@app.route("/generate")
def generate_ibans():
    country = request.args.get("country", "").upper()
    count = int(request.args.get("count", 1))
    
    if count < 1 or count > 100:
        return jsonify({
            "error": "Count must be between 1 and 100"
        }), 400
    
    if country not in country_data:
        return jsonify({
            "error": f"Unsupported country code: {country}",
            "supported_countries": list(country_data.keys())
        }), 400
    
    results = []
    for _ in range(count):
        try:
            iban, bban, check_digits = generate_iban_for_country(country)
            results.append({
                "iban": iban,
                "bban": bban,
                "check_digits": check_digits,
                "country": country,
                "length": len(iban),
                "valid": True
            })
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 500
    
    return jsonify({
        "count": len(results),
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)
