# Databricks notebook source
# MAGIC %md
# MAGIC # Case 006: Column Statistics (PROC MEANS / PROC FREQ)
# MAGIC
# MAGIC Translation of [`contents/case-006.md`](../contents/case-006.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC proc means data = cars ; output out = output_means; run;
# MAGIC proc freq data = cars; table origin * make / out = output_freq; run;
# MAGIC ```
# MAGIC
# MAGIC `DataFrame.summary()` gives count / mean / stddev / min / percentiles / max
# MAGIC for every column in one call, replacing PROC MEANS. For the cross-tab from
# MAGIC PROC FREQ we use `groupBy().count()` or `crosstab()`.

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

# MAGIC %md
# MAGIC ## Numeric & non-numeric summary (replaces PROC MEANS)

# COMMAND ----------

df_summary = df_cars_data.summary()
display(df_summary)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Frequency crosstab of `origin` × `make` (replaces PROC FREQ)

# COMMAND ----------

from pyspark.sql import functions as F

df_freq = (
    df_cars_data
    .groupBy("origin", "make")
    .agg(F.count("*").alias("frequency"))
    .orderBy("origin", "make")
)
display(df_freq)

# Alternative wide crosstab form:
display(df_cars_data.stat.crosstab("origin", "make"))
