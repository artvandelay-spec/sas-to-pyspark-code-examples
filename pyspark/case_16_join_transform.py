# Databricks notebook source
# MAGIC %md
# MAGIC # Case 016: Join Filtered Datasets and Transform Columns (IF / IF-ELSE)
# MAGIC
# MAGIC Translation of [`contents/case-016.md`](../contents/case-016.md).
# MAGIC
# MAGIC Returns information about Porsche cars with `horsepower < 400` that are
# MAGIC available in at least one PC racing sim (ACC / FH5 / PC2 / iR / rF2) but
# MAGIC NOT in Gran Turismo 7. Boolean 1/0 flags are rendered as "Yes"/"No".

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

df_porsche_cars = df_cars_data.filter(
    (F.col("make") == "Porsche") & (F.col("horsepower") < 400)
)

pc_only_expr = (
    (F.col("acc_available") == 1)
    | (F.col("fh5_available") == 1)
    | (F.col("pc2_available") == 1)
    | (F.col("ir_available") == 1)
    | (F.col("rf2_available") == 1)
) & (F.col("gt7_available") == 0)

df_only_pc_gaming = df_gaming_data.filter(pc_only_expr)

porsche_only_pc_cars = (
    df_porsche_cars.alias("pc")
    .join(
        df_only_pc_gaming.alias("opg"),
        F.col("pc.code") == F.col("opg.code"),
        "inner",
    )
)

flag_cols = [
    "acc_available", "fh5_available", "pc2_available", "ir_available", "rf2_available",
]

for col_name in flag_cols:
    porsche_only_pc_cars = porsche_only_pc_cars.withColumn(
        f"{col_name}_flag",
        F.when(F.col(col_name) == 1, F.lit("Yes")).otherwise(F.lit("No")),
    )

result = porsche_only_pc_cars.select(
    F.col("pc.code").alias("code"),
    "make", "model", "type", "horsepower",
    *[f"{c}_flag" for c in flag_cols],
)

display(result)
