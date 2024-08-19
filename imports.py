import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import time


def init_supabase():
    url: str = "https://sbmxhjnucuhuzyacjpir.supabase.co"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNibXhoam51Y3VodXp5YWNqcGlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNjc2Mzg5MSwiZXhwIjoyMDMyMzM5ODkxfQ.xPXkE1OU9jYlBjOA29uRS7wSGofugzGzJoUguf6m0ZM"
    supabase: Client = create_client(url, key)
    return supabase
