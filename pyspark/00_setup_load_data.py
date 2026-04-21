# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup & Load Data
# MAGIC
# MAGIC Shared setup notebook for the SAS → PySpark migration examples. Run this
# MAGIC once per session (or `%run` it from any case notebook) to create the three
# MAGIC DataFrames used throughout the guide:
# MAGIC
# MAGIC - `df_cars_data`   (from `cars_data.txt`)
# MAGIC - `df_custom_data` (from `customization_data.txt`)
# MAGIC - `df_gaming_data` (from `gaming_data.txt`)
# MAGIC
# MAGIC ## How to run on Databricks
# MAGIC 1. Upload the three `.txt` files from this repo's `data/` folder to a
# MAGIC    Databricks location you can read from. Any of the following work:
# MAGIC    - A Unity Catalog **Volume** (recommended):
# MAGIC      `/Volumes/<catalog>/<schema>/<volume>/sas_migration/`
# MAGIC    - **Workspace Files** alongside this notebook (import the whole repo).
# MAGIC    - Legacy **DBFS**: `/FileStore/sas_migration/`.
# MAGIC 2. Attach this notebook to a cluster with Databricks Runtime 12.2 LTS or
# MAGIC    newer (PySpark 3.x, Python 3.9+). Both classic and serverless clusters
# MAGIC    work — no extra libraries are required; `spark` is pre-initialized.
# MAGIC 3. Set the `data_path` widget below (default: `/Volumes/main/default/sas_migration`).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parameterize the data location with a widget

# COMMAND ----------

dbutils.widgets.text("data_path", "/Volumes/main/default/sas_migration", "Data directory")
data_path = dbutils.widgets.get("data_path").rstrip("/")
print(f"Reading input files from: {data_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load the three datasets
# MAGIC
# MAGIC The files are pipe-delimited with a header row. `inferSchema=True` is used
# MAGIC so that numeric columns (e.g. `msrp`, `horsepower`) come back as integer
# MAGIC / double rather than string — which mirrors the SAS dataset types.

# COMMAND ----------

df_cars_data = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("delimiter", "|")
    .load(f"{data_path}/cars_data.txt")
)

df_custom_data = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("delimiter", "|")
    .load(f"{data_path}/customization_data.txt")
)

df_gaming_data = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("delimiter", "|")
    .load(f"{data_path}/gaming_data.txt")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sanity checks

# COMMAND ----------

df_cars_data.printSchema()
df_custom_data.printSchema()
df_gaming_data.printSchema()

# COMMAND ----------

display(df_cars_data.limit(5))
display(df_custom_data.limit(5))
display(df_gaming_data.limit(5))
