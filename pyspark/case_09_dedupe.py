# Databricks notebook source
# MAGIC %md
# MAGIC # Case 009: Delete Duplicates (PROC SORT NODUPKEY)
# MAGIC
# MAGIC Translation of [`contents/case-009.md`](../contents/case-009.md).
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC proc sort data = cars nodupkey out = cars_distinct dupout = cars_duplicates_rep;
# MAGIC     by origin make;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

from pyspark.sql import functions as F

base = df_cars_data.select("make", "origin")

# Option 1: distinct() on all selected columns.
df_distinct = base.distinct().orderBy(F.col("origin").asc(), F.col("make").asc())
display(df_distinct)

# COMMAND ----------

# Option 2: dropDuplicates() on an explicit subset of columns.
df_dedup = base.dropDuplicates(["make", "origin"]).orderBy(
    F.col("origin").asc(), F.col("make").asc()
)
display(df_dedup)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recovering the `dupout` dataset
# MAGIC
# MAGIC SAS's `dupout =` writes every row that was considered a duplicate. We can
# MAGIC reproduce that by counting rows per key and keeping groups with `count > 1`.

# COMMAND ----------

window_cols = ["make", "origin"]

df_with_counts = base.groupBy(*window_cols).count()
df_duplicates_rep = (
    base.join(df_with_counts, on=window_cols, how="inner")
        .filter(F.col("count") > 1)
        .drop("count")
)
display(df_duplicates_rep)
