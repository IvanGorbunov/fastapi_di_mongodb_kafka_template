import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SPIDEY_NAMES = os.environ.get("SPIDEY_NAMES", "").split(",")
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
    SPIDERWEB_TOPIC = os.environ.get("SPIDERWEB_TOPIC", "")
    MY_NAME = os.environ.get("MY_NAME", "")
