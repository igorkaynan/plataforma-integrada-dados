from pyspark.sql import SparkSession, functions as F
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("GoldLayer")
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

cliente_360 = (
    vendas
    .groupBy("cliente_id")
    .agg(
        F.countDistinct("venda_id").alias("total_compras"),
        F.round(F.sum("valor_total"), 2).alias("receita_total"),
        F.round(F.avg("valor_total"), 2).alias("ticket_medio"),
        F.max("data_venda").alias("ultima_compra")
    )
    .join(clientes, "cliente_id", "left")
    .withColumn(
        "segmento",
        F.when(F.col("receita_total") >= 4000, "VIP")
         .when(F.col("receita_total") >= 1000, "Regular")
         .otherwise("Ocasional")
    )
)

performance_produtos = (
    vendas
    .groupBy("produto")
    .agg(
        F.sum("quantidade").alias("unidades_vendidas"),
        F.countDistinct("venda_id").alias("total_vendas"),
        F.round(F.sum("valor_total"), 2).alias("receita_total"),
        F.countDistinct("cliente_id").alias("clientes_unicos")
    )
    .orderBy(F.desc("receita_total"))
)

print("\n=== CLIENTE 360 ===")
cliente_360.show(truncate=False)

print("\n=== PERFORMANCE DE PRODUTOS ===")
performance_produtos.show(truncate=False)

cliente_360.toPandas().to_csv(
    BASE_DIR / "data" / "gold" / "cliente_360.csv",
    index=False
)

performance_produtos.toPandas().to_csv(
    BASE_DIR / "data" / "gold" / "performance_produtos.csv",
    index=False
)

print("\nGOLD criada com sucesso!")

spark.stop()
