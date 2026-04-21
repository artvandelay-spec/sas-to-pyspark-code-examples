# Databricks notebook source
# MAGIC %md
# MAGIC # Case 008: Order Data and Get Top N (PROC SORT BY / KEY)
# MAGIC
# MAGIC Translation of [`contents/case-008.md`](../contents/case-008.md). Both
# MAGIC SAS `by` and `key` forms collapse to `orderBy()` in Spark.
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC proc sort data = cars out = cars_mpg_city_by;
# MAGIC     by descending mpg_city descending mpg_highway;
# MAGIC run;
# MAGIC proc sort data = cars out = cars_mpg_highway_key;
# MAGIC     key mpg_highway / descending;
# MAGIC     key mpg_city / descending;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

base = df_cars_data.select("code", "make", "model", "mpg_city", "mpg_highway")

df_cars_mpg_city_by = base.orderBy(
    F.col("mpg_city").desc(), F.col("mpg_highway").desc()
).limit(25)

df_cars_mpg_highway_key = base.orderBy(
    F.col("mpg_highway").desc(), F.col("mpg_city").desc()
).limit(25)

display(df_cars_mpg_city_by)

# COMMAND ----------

display(df_cars_mpg_highway_key)
