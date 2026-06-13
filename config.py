# config.py — edite esse arquivo com suas configurações
import os
from dotenv import load_dotenv
load_dotenv()
CAMINHO_CREDENTIALS = "credentials.json"
CAMINHO_TOKEN = "token.json"
FUSO_HORAS = -3  # UTC-3 = Brasília
FONTE_MEMBROS = "sheets" # "sheets" ou "excel"
CAMINHO_EXCEL = "membros.xlsx"
SHEETS_ID= os.getenv("SHEETS_ID")