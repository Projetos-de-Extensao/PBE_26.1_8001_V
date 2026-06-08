import requests

print("--- Iniciando teste de upload via script Python ---")

# 1. Autenticar como Aluno
login_url = "http://127.0.0.1:8001/api/token/"
credentials = {
    "username": "aluno01",
    "password": "senha123"
}
print(f"1. Fazendo login com o usuário '{credentials['username']}'...")
response = requests.post(login_url, json=credentials)

if response.status_code != 200:
    print("Falha ao obter o token. O servidor está rodando?")
    exit()

token = response.json()["access"]
print("Sucesso! Token JWT obtido.")

# 2. Fazer o Upload do documento
upload_url = "http://127.0.0.1:8001/api/documentos/"
headers = {
    "Authorization": f"Bearer {token}"
}
data = {
    "solicitacao": 1,
    "nome": "Termo de Compromisso de Estágio - TCE",
    "tipo": "TCE"
}

# Criamos um arquivo fictício na memória para o upload
files = {
    "arquivo": ("tce_teste.pdf", b"Conteudo simulado do documento de estagio.", "application/pdf")
}

print(f"2. Enviando documento para a solicitação #{data['solicitacao']}...")
upload_response = requests.post(upload_url, headers=headers, data=data, files=files)

print("\n--- Resultado do Upload ---")
print(f"Status Code: {upload_response.status_code}")
print("Response JSON:")
import json
print(json.dumps(upload_response.json(), indent=4, ensure_ascii=False))
