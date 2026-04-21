# Databricks notebook source
# MAGIC %md
# MAGIC # Case 010: Append Datasets (PROC APPEND / SET)
# MAGIC
# MAGIC Translation of [`contents/case-010.md`](../contents/case-010.md). The
# MAGIC three datasets share the same schema, so `union()` is the direct
# MAGIC analogue of SAS `set`/`proc append`.
# MAGIC
# MAGIC **SAS original (abridged):**
# MAGIC ```sas
# MAGIC data all_cars; set audi_cars bmw_cars; run;
# MAGIC proc append base = all_cars data = mercedes_cars force; run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

keep_cols = ["code", "make", "model", "type", "origin", "msrp"]
base = df_cars_data.select(*keep_cols)

audi_cars = base.filter((F.col("make") == "Audi") & (F.col("msrp") > 50000))
bmw_cars = base.filter((F.col("make") == "BMW") & (F.col("msrp") > 50000))
mercedes_cars = base.filter(
    (F.col("make") == "Mercedes-Benz") & (F.col("msrp") > 50000)
)

all_cars = audi_cars.union(bmw_cars).union(mercedes_cars)
display(all_cars)
