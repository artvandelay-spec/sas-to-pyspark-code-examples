# Databricks notebook source
# MAGIC %md
# MAGIC # Case 015: Join Datasets and Count Results
# MAGIC
# MAGIC Translation of [`contents/case-015.md`](../contents/case-015.md). The
# MAGIC SAS `data _null_; ... put "Number of Observations = " n; run;` pattern
# MAGIC is replaced by `DataFrame.count()` + `print()`.
# MAGIC
# MAGIC **SAS original (abridged):**
# MAGIC ```sas
# MAGIC data cars_color_customized;
# MAGIC     merge cars (in = ca)
# MAGIC           custom (in = cu where = (color_custom = 1));
# MAGIC     by code;
# MAGIC     if ca = cu;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

cars_color_customized = (
    df_cars_data.alias("ca")
    .join(
        df_custom_data.alias("cu"),
        (F.col("ca.code") == F.col("cu.code")) & (F.col("cu.color_custom") == 1),
        "inner",
    )
)

n = cars_color_customized.count()
print(f"Number of Observations = {n}")
