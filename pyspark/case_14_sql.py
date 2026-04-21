# Databricks notebook source
# MAGIC %md
# MAGIC # Case 014: Create a Dataset Using SQL
# MAGIC
# MAGIC Translation of [`contents/case-014.md`](../contents/case-014.md). Two
# MAGIC flavors are shown: `spark.sql(...)` against a temp view, and the more
# MAGIC Databricks-idiomatic `%sql` magic cell.
# MAGIC
# MAGIC **SAS original:**
# MAGIC ```sas
# MAGIC proc sql;
# MAGIC     create table lexus_sedan_cars as
# MAGIC     select code, make, model, type, origin, drivetrain,
# MAGIC            msrp, invoice, horsepower, weight
# MAGIC       from cars
# MAGIC      where make = 'Lexus' and type = 'Sedan' and invoice > 40000;
# MAGIC run;
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./00_setup_load_data

# COMMAND ----------

df_cars_data.createOrReplaceTempView("cars")

sql_query = """
    SELECT code, make, model, type, origin, drivetrain,
           msrp, invoice, horsepower, weight
      FROM cars
     WHERE make = 'Lexus'
       AND type = 'Sedan'
       AND invoice > 40000
"""

lexus_sedan_cars = spark.sql(sql_query)
display(lexus_sedan_cars)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Same query using a `%sql` Databricks magic cell

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT code, make, model, type, origin, drivetrain,
# MAGIC        msrp, invoice, horsepower, weight
# MAGIC   FROM cars
# MAGIC  WHERE make = 'Lexus'
# MAGIC    AND type = 'Sedan'
# MAGIC    AND invoice > 40000
