from pyspark.sql import SparkSession, functions as F
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("SilverLayer")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

BASE_DIR = Path(__file__).resolve().parents[2]

# =========================
# LEITURA DA BRONZE
# =========================

clientes = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "bronze" / "clientes.csv"))
)

vendas = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "bronze" / "vendas.csv"))
)

usuarios_api = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(BASE_DIR / "data" / "bronze" / "usuarios_api.csv"))
)

# =========================
# TRANSFORMAÇÃO CLIENTES
# =========================

clientes_silver = (
    clientes
    .dropDuplicates(["cliente_id"])
    .filter(F.col("cliente_id").isNotNull())
    .filter(F.col("email").isNotNull())
    .withColumn("cliente_id", F.col("cliente_id").cast("int"))
    .withColumn("nome", F.initcap(F.trim("nome")))
    .withColumn("email", F.lower(F.trim("email")))
    .withColumn("cidade", F.initcap(F.trim("cidade")))
    .withColumn("data_cadastro", F.to_date("data_cadastro"))
)

# =========================
# TRANSFORMAÇÃO VENDAS
# =========================

vendas_silver = (
    vendas
    .dropDuplicates(["venda_id"])
    .filter(F.col("venda_id").isNotNull())
    .filter(F.col("cliente_id").isNotNull())
    .withColumn("venda_id", F.col("venda_id").cast("int"))
    .withColumn("cliente_id", F.col("cliente_id").cast("int"))
    .withColumn("quantidade", F.col("quantidade").cast("int"))
    .withColumn("valor_unitario", F.col("valor_unitario").cast("double"))
    .filter(F.col("quantidade") > 0)
    .filter(F.col("valor_unitario") > 0)
    .withColumn("produto", F.initcap(F.trim("produto")))
    .withColumn("data_venda", F.to_date("data_venda"))
    .withColumn(
        "valor_total",
        F.round(F.col("quantidade") * F.col("valor_unitario"), 2)
    )
)

# =========================
# TRANSFORMAÇÃO API
# =========================

usuarios_api_silver = (
    usuarios_api
    .dropDuplicates(["usuario_id"])
    .filter(F.col("usuario_id").isNotNull())
    .filter(F.col("email").isNotNull())
    .withColumn("usuario_id", F.col("usuario_id").cast("int"))
    .withColumn("nome", F.initcap(F.trim("nome")))
    .withColumn("email", F.lower(F.trim("email")))
    .withColumn("cidade", F.initcap(F.trim("cidade")))
    .withColumn("empresa", F.initcap(F.trim("empresa")))
)

# =========================
# VISUALIZAÇÃO
# =========================

print("\n=== CLIENTES SILVER ===")
clientes_silver.show(truncate=False)

print("\n=== VENDAS SILVER ===")
vendas_silver.show(truncate=False)

print("\n=== USUÁRIOS API SILVER ===")
usuarios_api_silver.show(truncate=False)

# =========================
# GRAVAÇÃO DA SILVER
# =========================

clientes_silver.toPandas().to_csv(
    BASE_DIR / "data" / "silver" / "clientes.csv",
    index=False
)

vendas_silver.toPandas().to_csv(
    BASE_DIR / "data" / "silver" / "vendas.csv",
    index=False
)

usuarios_api_silver.toPandas().to_csv(
    BASE_DIR / "data" / "silver" / "usuarios_api.csv",
    index=False
)

print("\nSILVER criada com sucesso!")

spark.stop()