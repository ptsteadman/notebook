"""
Generate random passwords with lowercase, uppercase, and digits.

"""

import string
import secrets

class PasswordGenerator:
    def __init__(self):
        pass

    def generate_password(self, length: int):
        """
        Generate a password with at least one character of each type.
        
        Args:
            length: Length of the password (minimum 3)
            
        Returns:
            A random password with at least one lowercase, uppercase, and digit
        """
        if length < 3:
            raise ValueError("Password length must be at least 3 to include all character types")
        
        # Step 1: Ensure one character of each type
        password_chars = [
            secrets.choice(string.ascii_lowercase),   # One lowercase
            secrets.choice(string.ascii_uppercase),   # One uppercase  
            secrets.choice(string.digits)             # One digit
        ]
        
        # Step 2: Fill remaining positions with random characters from all types
        all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        remaining_length = length - 3
        
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(all_chars))
        
        # Step 3: Shuffle the password to ensure randomness
        # This is crucial - without shuffling, the first 3 characters would always be in the same order
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
        
        return ''.join(password_chars)


def demo():
    """Demo the password generator."""
    generator = PasswordGenerator()
    
    print("=== Password Generator Demo ===\n")
    
    # Generate passwords of different lengths
    for length in [8, 12, 16]:
        password = generator.generate_password(length)
        print(f"Password ({length} chars): {password}")
        
        # Verify it has at least one of each type
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        print(f"  ✓ Has lowercase: {has_lower}")
        print(f"  ✓ Has uppercase: {has_upper}")
        print(f"  ✓ Has digit: {has_digit}")
        print()


if __name__ == "__main__":
    demo()

