from sqlalchemy import create_engine
import os
import dotenv

USERNAME = "junmailk0591"
PASSWORD = os.environ.get("NEON_PRODUCTION_PASSWORD")
HOST = "ep-divine-voice-71352132-pooler.us-east-2.aws.neon.tech"
DATABASE = "volunteer_management"

conn_str = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?sslmode=require'

engine = create_engine(conn_str)