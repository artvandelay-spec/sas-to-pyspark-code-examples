# Databricks notebook source
# MAGIC %md
# MAGIC # Case 002: Filtering Data and Selecting Columns (KEEP option)
# MAGIC
# MAGIC Translation of [`contents/case-002.md`](../contents/case-002.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars (keep = code make model type msrp);
# MAGIC     set datalib.cars_data;
# MAGIC     if make = 'Audi';
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

df_result = (
    df_cars_data
    .select("code", "make", "model", "type", "msrp")
    .filter(F.col("make") == "Audi")
)

display(df_result)
