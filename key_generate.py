import random
import string
import fileinput

# Generate a random SECRET_KEY
secret_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for _ in range(50))

# Path to your .env file
env_file = '.env'

# Update the value of SECRET_KEY in the .env file
with fileinput.FileInput(env_file, inplace=True) as file:
    for line in file:
        if line.startswith('SECRET_KEY='):
            print(f'SECRET_KEY={secret_key}')
        else:
            print(line.strip())
    print("secret key generated in your .env")