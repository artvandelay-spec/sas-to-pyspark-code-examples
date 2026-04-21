# Databricks notebook source
# MAGIC %md
# MAGIC # Case 005: Delete Rows from Dataset with a Condition
# MAGIC
# MAGIC Translation of [`contents/case-005.md`](../contents/case-005.md). SAS
# MAGIC `if ... then delete;` becomes the inverse `filter()` predicate in Spark.
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars (keep = code make model type msrp enginesize cylinders);
# MAGIC     set datalib.cars_data;
# MAGIC     if msrp < 100000 then delete;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

df_result = (
    df_cars_data
    .select("code", "make", "model", "type", "msrp", "enginesize", "cylinders")
    .filter(F.col("msrp") >= 100000)
)

display(df_result)
