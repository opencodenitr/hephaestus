import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    IP_ADDRESS = os.getenv("IP_ADDRESS")
    PORT = int(os.getenv("PORT"))