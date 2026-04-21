# Databricks notebook source
# MAGIC %md
# MAGIC # Case 012: Create a Row Number in a Dataset
# MAGIC
# MAGIC Translation of [`contents/case-012.md`](../contents/case-012.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars_rownum;
# MAGIC     set cars;
# MAGIC     rownum + 1;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

cars = (
    df_cars_data
    .select("code", "make", "model", "type", "origin")
    .filter((F.col("origin") == "Europe") & (F.col("type") == "Sports"))
)

# An unpartitioned window requires an orderBy. Using a literal keeps insertion
# order stable for a single-partition DataFrame (matches SAS `rownum + 1`
# semantics). For large, multi-partition inputs pick a real ordering column.
window_spec = Window.orderBy(F.lit(1))
cars_rownum = cars.withColumn("rownum", F.row_number().over(window_spec))

display(cars_rownum)
