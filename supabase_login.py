import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_supabase_object():
    url: str = os.environ['SUPABASE_URL']
    key: str = os.environ['SUPABASE_KEY']

    supabase = create_client(url, key)
    return supabase
    # pass
