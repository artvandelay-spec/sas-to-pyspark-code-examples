# Databricks notebook source
# MAGIC %md
# MAGIC # Case 001: Adding New Columns to a Dataset
# MAGIC
# MAGIC Translation of [`contents/case-001.md`](../contents/case-001.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC data cars;
# MAGIC     set datalib.cars_data (obs = 5);
# MAGIC     length car_category $10;
# MAGIC     car_category = 'Luxury';
# MAGIC     engine_modifications = 'Stock';
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

df_cars = (
    df_cars_data
    .withColumn("car_category", F.lit("Luxury"))
    .withColumn("engine_modifications", F.lit("Stock"))
    .limit(5)
)

display(df_cars)
