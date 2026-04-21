# Databricks notebook source
# MAGIC %md
# MAGIC # Case 013: Create a Row Number by Group
# MAGIC
# MAGIC Translation of [`contents/case-013.md`](../contents/case-013.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars_rownum_group;
# MAGIC     set cars;
# MAGIC     by make;
# MAGIC     rownum + 1;
# MAGIC     if first.make then rownum = 1;
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

window_spec = Window.partitionBy("make").orderBy("model")
cars_rownum = cars.withColumn("rownum", F.row_number().over(window_spec))

display(cars_rownum)
