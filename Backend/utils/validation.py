import re

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", str(email)))

def validate_mobile(mobile):
    return bool(re.match(r"^(?:\+91|0)?[6-9]\d{9}$", str(mobile).strip()))

def validate_password(password):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$", str(password).strip()))
