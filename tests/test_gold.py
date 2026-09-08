import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def test_cliente_360_sem_ids_nulos():
    df = pd.read_csv(
        BASE_DIR / "data" / "gold" / "cliente_360.csv"
    )

    assert df["cliente_id"].isnull().sum() == 0

def test_receita_total_positiva():
    df = pd.read_csv(
        BASE_DIR / "data" / "gold" / "cliente_360.csv"
    )

    assert (df["receita_total"] > 0).all()

def test_segmentos_validos():
    df = pd.read_csv(
        BASE_DIR / "data" / "gold" / "cliente_360.csv"
    )

    segmentos_validos = {
        "VIP",
        "Regular",
        "Ocasional"
    }

    assert set(df["segmento"]).issubset(segmentos_validos)
