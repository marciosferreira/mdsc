"""Gera o Base64 do credentials.json para uso como GOOGLE_CREDENTIALS_JSON."""
import base64
from pathlib import Path

creds = Path(__file__).parent / "credentials.json"
if not creds.exists():
    print("ERRO: credentials.json não encontrado na raiz do projeto.")
else:
    b64 = base64.b64encode(creds.read_bytes()).decode()
    print("Copie o valor abaixo e cole como GOOGLE_CREDENTIALS_JSON no seu serviço cloud:\n")
    print(b64)
