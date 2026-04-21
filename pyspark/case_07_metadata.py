# Databricks notebook source
# MAGIC %md
# MAGIC # Case 007: Get Metadata for a Dataset (PROC CONTENTS)
# MAGIC
# MAGIC Translation of [`contents/case-007.md`](../contents/case-007.md). In
# MAGIC PySpark, `printSchema()` is the visual equivalent; to capture metadata
# MAGIC as a DataFrame we build one from `df.schema.fields`.
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC proc contents data = cars out = cars_metadata order = varnum; run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

df_cars_data.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build a metadata DataFrame (name, datatype, nullable, varnum)

# COMMAND ----------

metadata_rows = [
    (idx + 1, field.name, field.dataType.simpleString(), field.nullable)
    for idx, field in enumerate(df_cars_data.schema.fields)
]

df_metadata = spark.createDataFrame(
    metadata_rows, ["varnum", "name", "datatype", "nullable"]
)

display(df_metadata)
