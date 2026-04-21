# Databricks notebook source
# MAGIC %md
# MAGIC # Case 011: Append Datasets with Different Columns (FORCE / NOWARN)
# MAGIC
# MAGIC Translation of [`contents/case-011.md`](../contents/case-011.md).
# MAGIC `unionByName(..., allowMissingColumns=True)` is the PySpark equivalent of
# MAGIC `proc append ... force nowarn;` — missing columns are filled with `null`.
# MAGIC
# MAGIC **SAS original (abridged):**
# MAGIC ```sas
# MAGIC data all_cars; set audi_cars bmw_cars; run;
# MAGIC proc append base = all_cars data = mercedes_cars force nowarn; run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

audi_cars = (
    df_cars_data.select("code", "make", "model", "type", "origin", "msrp")
    .filter((F.col("make") == "Audi") & (F.col("msrp") > 50000))
)

bmw_cars = (
    df_cars_data.select(
        "code", "make", "model", "origin", "msrp", "cylinders", "horsepower"
    )
    .filter((F.col("make") == "BMW") & (F.col("msrp") > 50000))
)

mercedes_cars = (
    df_cars_data.select("code", "make", "model", "msrp", "horsepower")
    .filter((F.col("make") == "Mercedes-Benz") & (F.col("msrp") > 50000))
)

all_cars = (
    audi_cars
    .unionByName(bmw_cars, allowMissingColumns=True)
    .unionByName(mercedes_cars, allowMissingColumns=True)
)

display(all_cars)
