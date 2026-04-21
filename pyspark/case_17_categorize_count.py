# Databricks notebook source
# MAGIC %md
# MAGIC # Case 017: Categorize & Count Group Data (SELECT-WHEN)
# MAGIC
# MAGIC Translation of [`contents/case-017.md`](../contents/case-017.md).
# MAGIC SAS `SELECT-WHEN` maps cleanly to chained `F.when(...).otherwise(...)`.
# MAGIC
# MAGIC Category rules (on `total_availability` = sum of the 6 game flags):
# MAGIC - `0`  → `NOT AVAILABLE`
# MAGIC - `1`  → `SINGLE`
# MAGIC - `2..5` → `MEDIUM`
# MAGIC - `6`  → `FULL`
# MAGIC - else → `NO DATA`

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

availability_cols = [
    "gt7_available", "acc_available", "fh5_available",
    "pc2_available", "ir_available", "rf2_available",
]

total_availability = sum(F.col(c) for c in availability_cols)

df_gaming = df_gaming_data.withColumn(
    "total_availability", total_availability
).withColumn(
    "availability_category",
    F.when(F.col("total_availability") == 0, F.lit("NOT AVAILABLE"))
     .when(F.col("total_availability") == 1, F.lit("SINGLE"))
     .when(
         (F.col("total_availability") >= 2) & (F.col("total_availability") <= 5),
         F.lit("MEDIUM"),
     )
     .when(F.col("total_availability") == 6, F.lit("FULL"))
     .otherwise(F.lit("NO DATA")),
)

df_gaming_total_by_cat = (
    df_gaming.groupBy("availability_category")
    .count()
    .withColumnRenamed("count", "total")
    .orderBy(F.col("availability_category").asc())
)

display(df_gaming_total_by_cat)
