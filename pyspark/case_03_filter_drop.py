# Databricks notebook source
# MAGIC %md
# MAGIC # Case 003: Filtering Data and Dropping Columns (DROP option)
# MAGIC
# MAGIC Translation of [`contents/case-003.md`](../contents/case-003.md). Both
# MAGIC options from the original are shown: `drop()` and an equivalent `select()`.
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars (drop = type origin drivetrain enginesize cylinders horsepower
# MAGIC                   mpg_city mpg_highway weight wheelbase length);
# MAGIC     set datalib.cars_data;
# MAGIC     if make = 'Kia';
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

# MAGIC %md
# MAGIC ## Option 1: drop unwanted columns

# COMMAND ----------

from pyspark.sql import functions as F

drop_cols = [
    "type", "origin", "drivetrain", "enginesize", "cylinders",
    "horsepower", "mpg_city", "mpg_highway", "weight", "wheelbase", "length",
]

df_result_opt1 = (
    df_cars_data
    .drop(*drop_cols)
    .filter(F.col("make") == "Kia")
)

display(df_result_opt1)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Option 2: select only the columns we want

# COMMAND ----------

df_result_opt2 = (
    df_cars_data
    .select("code", "make", "model", "msrp", "invoice")
    .filter(F.col("make") == "Kia")
)

display(df_result_opt2)
