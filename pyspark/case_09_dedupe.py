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
# MAGIC SAS's `dupout =` writes only the rows that were *removed* by NODUPKEY —
# MAGIC that is, every row except the first one within each BY-group. We
# MAGIC reproduce that with `row_number()` over a window partitioned by the
# MAGIC NODUPKEY columns and keep rows with `rn > 1`.

# COMMAND ----------

from pyspark.sql.window import Window

window_cols = ["origin", "make"]
dupout_window = Window.partitionBy(*window_cols).orderBy(F.lit(1))

df_duplicates_rep = (
    base.withColumn("rn", F.row_number().over(dupout_window))
        .filter(F.col("rn") > 1)
        .drop("rn")
)
display(df_duplicates_rep)
