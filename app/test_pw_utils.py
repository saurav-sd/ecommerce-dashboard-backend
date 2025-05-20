from app.core.security import verify_password, hash_password

# Test password
plain = "my_secure_password"

# Hash the password
hashed = hash_password(plain)
print("Hashed password:", hashed)

# Verify the password
is_valid = verify_password(plain, hashed)
print("Password is valid:", is_valid)

# Try a wrong password
is_invalid = verify_password("wrong_password", hashed)
print("Wrong password is valid:", is_invalid)
