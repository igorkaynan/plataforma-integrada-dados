import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

ETAPAS = [
    (
        "Ingestão da API",
        BASE_DIR / "src" / "ingestion" / "api_ingestion.py"
    ),
    (
        "Camada Bronze",
        BASE_DIR / "src" / "bronze" / "carregar_bronze.py"
    ),
    (
        "Camada Silver",
        BASE_DIR / "src" / "silver" / "processar_silver.py"
    ),
    (
        "Camada Gold",
        BASE_DIR / "src" / "gold" / "criar_gold.py"
    ),
    (
        "Data Quality",
        BASE_DIR / "src" / "quality" / "data_quality.py"
    )
]

def executar_etapa(nome, script):
    print("\n" + "=" * 60)
    print(f"Executando: {nome}")
    print("=" * 60)

    subprocess.run(
        [sys.executable, str(script)],
        check=True,
        cwd=BASE_DIR
    )

def main():
    print("\nINICIANDO PIPELINE DE DADOS")

    for nome, script in ETAPAS:
        executar_etapa(nome, script)

    print("\n" + "=" * 60)
    print("PIPELINE EXECUTADO COM SUCESSO")
    print("=" * 60)

if __name__ == "__main__":
    main()