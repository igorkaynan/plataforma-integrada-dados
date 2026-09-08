from pyspark.sql import SparkSession
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("PlataformaIntegradaDados")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

BASE_DIR = Path(__file__).resolve().parents[2]

# =========================
# LEITURA RAW
# =========================

clientes = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "raw" / "clientes.csv"))
)

vendas = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "raw" / "vendas.csv"))
)

usuarios_api = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "raw" / "usuarios_api.csv"))
)

# =========================
# VISUALIZAÇÃO
# =========================

print("\n=== CLIENTES ===")
clientes.show(truncate=False)

print("\n=== VENDAS ===")
vendas.show(truncate=False)

print("\n=== USUÁRIOS API ===")
usuarios_api.show(truncate=False)

# =========================
# GRAVAÇÃO BRONZE
# =========================

clientes.toPandas().to_csv(
    BASE_DIR / "data" / "bronze" / "clientes.csv",
    index=False
)

vendas.toPandas().to_csv(
    BASE_DIR / "data" / "bronze" / "vendas.csv",
    index=False
)

usuarios_api.toPandas().to_csv(
    BASE_DIR / "data" / "bronze" / "usuarios_api.csv",
    index=False
)

print("\nBRONZE criada com sucesso!")
print("Arquivos:")
print("data/bronze/clientes.csv")
print("data/bronze/vendas.csv")
print("data/bronze/usuarios_api.csv")

spark.stop()