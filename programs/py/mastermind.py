import random
import unittest
from typing import List
import collections

"""
enter in 
"""

COLORS = {
    "R",
    "Y",
    "O",
    "G",
    "B",
    "P",
}

def generate_secret():
    return [random.choice(list(COLORS)) for _ in range(4)]


def validate(secret: List[str], guess: List[str]):
    black_indices = set()
    for i, (s, g) in enumerate(zip(secret, guess)):
        if s == g:
            black_indices.add(i)
    secrets_counts = collections.Counter(secret)
    guesses_counts = collections.Counter(guess)
    for i in black_indices:
        secrets_counts[secret[i]] -= 1
        guesses_counts[guess[i]] -= 1
    whites = 0
    for color in secrets_counts.keys():
        whites += min(secrets_counts[color], guesses_counts[color])
    return len(black_indices), whites 


validate(["R", "B", "B", "B"],
         ["R", "R", "R", "R",])

SECRET = generate_secret()

while True:
    guess = input(f"Enter in four characters from {", ".join(COLORS)}: ")
    print(validate(SECRET, list(guess)))



"""
secrets_count
{
R: 2
B: 2
}

set(2)

secrets_count after subtracting matches:
{
R: 2
B: 1
}


{
R: 1
B: 2
}




"""
print(validate(["R", "R", "B", "B"],
               ["B", "B", "B", "R",])) # 1, 2