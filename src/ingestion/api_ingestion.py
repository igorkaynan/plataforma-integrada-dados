import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

URL = "https://jsonplaceholder.typicode.com/users"

def extrair_dados_api():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    return response.json()

def transformar_dados(dados):
    registros = []

    for item in dados:
        registros.append({
            "usuario_id": item["id"],
            "nome": item["name"],
            "email": item["email"],
            "cidade": item["address"]["city"],
            "empresa": item["company"]["name"]
        })

    return pd.DataFrame(registros)

def salvar_raw(df):
    caminho = BASE_DIR / "data" / "raw" / "usuarios_api.csv"
    df.to_csv(caminho, index=False)
    return caminho

if __name__ == "__main__":
    print("Iniciando ingestão da API...")

    dados = extrair_dados_api()
    df = transformar_dados(dados)
    caminho = salvar_raw(df)

    print(df.head())
    print(f"\nArquivo salvo em: {caminho}")
    print("Ingestão concluída com sucesso.")