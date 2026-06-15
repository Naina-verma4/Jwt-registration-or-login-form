import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("DATABASE_URL"))
print(os.getenv("SECRET_KEY"))
print(os.getenv("ALGORITHM"))