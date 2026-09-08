from pyspark.sql import SparkSession, functions as F
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("DataQuality")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

BASE_DIR = Path(__file__).resolve().parents[2]

clientes = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BASE_DIR / "data" / "silver" / "clientes.csv"))
)

vendas = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(BASE_DIR / "data" / "silver" / "vendas.csv"))
)

resultados = []

def check(nome, condicao):
    status = "PASS" if condicao else "FAIL"
    resultados.append((nome, status))
    print(f"[{status}] {nome}")

check(
    "cliente_id não pode ser nulo",
    clientes.filter(F.col("cliente_id").isNull()).count() == 0
)

check(
    "email não pode ser nulo",
    clientes.filter(F.col("email").isNull()).count() == 0
)

check(
    "cliente_id deve ser único",
    clientes.count() == clientes.select("cliente_id").distinct().count()
)

check(
    "venda_id não pode ser nulo",
    vendas.filter(F.col("venda_id").isNull()).count() == 0
)

check(
    "venda_id deve ser único",
    vendas.count() == vendas.select("venda_id").distinct().count()
)

check(
    "quantidade deve ser positiva",
    vendas.filter(F.col("quantidade") <= 0).count() == 0
)

check(
    "valor_unitario deve ser positivo",
    vendas.filter(F.col("valor_unitario") <= 0).count() == 0
)

check(
    "valor_total deve ser positivo",
    vendas.filter(F.col("valor_total") <= 0).count() == 0
)

print("\n=== DATA QUALITY ===")

for nome, status in resultados:
    print(f"{status:4} | {nome}")

falhas = [item for item in resultados if item[1] == "FAIL"]

if falhas:
    raise ValueError(
        f"{len(falhas)} teste(s) de qualidade falharam."
    )

print("\nTodos os testes de qualidade passaram!")

spark.stop()
