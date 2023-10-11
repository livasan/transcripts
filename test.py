import random
from string import ascii_letters as letters

a = [{} for _ in range(10)]

for i in a:
    i[letters[random.randrange(len(letters))]] = random.random()

print(a)