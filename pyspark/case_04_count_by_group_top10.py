# Databricks notebook source
# MAGIC %md
# MAGIC # Case 004: Count Rows by Group, Order, and Get Top 10
# MAGIC
# MAGIC Translation of [`contents/case-004.md`](../contents/case-004.md).
# MAGIC
# MAGIC **SAS original (abridged):**
# MAGIC ```sas
# MAGIC data cars (keep = make total);
# MAGIC     set datalib.cars_data;
# MAGIC     by make;
# MAGIC     if first.make then total = 0;
# MAGIC     total + 1;
# MAGIC     if last.make;
# MAGIC run;
# MAGIC proc sort data = cars out = cars_ordered; by descending total; run;
# MAGIC data cars_top10; set cars_ordered (obs = 10); run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

df_top10 = (
    df_cars_data
    .groupBy("make")
    .count()
    .withColumnRenamed("count", "total")
    .orderBy(F.col("total").desc(), F.col("make").asc())
    .limit(10)
)

display(df_top10)
