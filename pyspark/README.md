# PySpark / Databricks translations

Databricks-compatible PySpark notebooks that translate every SAS example from
the [`contents/`](../contents) directory. Each file is written in the
**Databricks notebook source format** (plain `.py` with
`# Databricks notebook source` as the first line and `# COMMAND ----------`
as cell separators), so you can import the folder directly as a Databricks
Repo / Workspace and run each notebook as-is.

## Contents

| # | Notebook | Translates |
| --- | --- | --- |
| — | [`00_setup_load_data.py`](./00_setup_load_data.py) | Shared data-load notebook (used by every case via `%run`) |
| 1 | [`case_01_add_column.py`](./case_01_add_column.py) | [case-001](../contents/case-001.md) – Adding new columns |
| 2 | [`case_02_filter_keep.py`](./case_02_filter_keep.py) | [case-002](../contents/case-002.md) – Filter + KEEP |
| 3 | [`case_03_filter_drop.py`](./case_03_filter_drop.py) | [case-003](../contents/case-003.md) – Filter + DROP |
| 4 | [`case_04_count_by_group_top10.py`](./case_04_count_by_group_top10.py) | [case-004](../contents/case-004.md) – Count by group, top 10 |
| 5 | [`case_05_delete_rows.py`](./case_05_delete_rows.py) | [case-005](../contents/case-005.md) – Delete rows with condition |
| 6 | [`case_06_statistics.py`](./case_06_statistics.py) | [case-006](../contents/case-006.md) – PROC MEANS / PROC FREQ |
| 7 | [`case_07_metadata.py`](./case_07_metadata.py) | [case-007](../contents/case-007.md) – PROC CONTENTS |
| 8 | [`case_08_order_top_n.py`](./case_08_order_top_n.py) | [case-008](../contents/case-008.md) – PROC SORT BY / KEY |
| 9 | [`case_09_dedupe.py`](./case_09_dedupe.py) | [case-009](../contents/case-009.md) – NODUPKEY |
| 10 | [`case_10_append_same_schema.py`](./case_10_append_same_schema.py) | [case-010](../contents/case-010.md) – PROC APPEND |
| 11 | [`case_11_append_different_schema.py`](./case_11_append_different_schema.py) | [case-011](../contents/case-011.md) – PROC APPEND FORCE/NOWARN |
| 12 | [`case_12_rownum.py`](./case_12_rownum.py) | [case-012](../contents/case-012.md) – rownum |
| 13 | [`case_13_rownum_by_group.py`](./case_13_rownum_by_group.py) | [case-013](../contents/case-013.md) – rownum by group |
| 14 | [`case_14_sql.py`](./case_14_sql.py) | [case-014](../contents/case-014.md) – PROC SQL |
| 15 | [`case_15_join_count.py`](./case_15_join_count.py) | [case-015](../contents/case-015.md) – Join + count |
| 16 | [`case_16_join_transform.py`](./case_16_join_transform.py) | [case-016](../contents/case-016.md) – Join + IF/ELSE transform |
| 17 | [`case_17_categorize_count.py`](./case_17_categorize_count.py) | [case-017](../contents/case-017.md) – SELECT-WHEN categorize |

## Databricks setup

1. **Cluster / runtime.** Any cluster on Databricks Runtime 11.3 LTS or later
   (PySpark 3.3+, Python 3.9+) works — including serverless SQL warehouses for
   `%sql` cells and all-purpose compute for notebook execution. No external
   libraries are required: `spark`, `dbutils`, `display`, and `%sql` are all
   provided by Databricks.

2. **Upload the data.** Copy the three files from [`../data/`](../data) to a
   location the cluster can read from. Recommended options, in order of
   preference:

   | Storage option | Path pattern |
   | --- | --- |
   | Unity Catalog Volume (recommended) | `/Volumes/<catalog>/<schema>/<volume>/sas_migration/` |
   | Workspace Files (import the repo) | `/Workspace/Repos/<user>/<repo>/data/` |
   | Legacy DBFS | `/FileStore/sas_migration/` or `dbfs:/FileStore/sas_migration/` |

3. **Import the notebooks.** Either:
   - **Repos / Git folders** (preferred): add this repository to Databricks
     Repos. The `.py` files will appear as native Databricks notebooks.
   - **File import**: in the workspace, right-click a folder →
     *Import* → select these `.py` files. Databricks auto-detects the source
     format from the `# Databricks notebook source` header.

4. **Configure the data path.** Open `00_setup_load_data.py` and set the
   `data_path` widget at the top of the notebook (default:
   `/Volumes/main/default/sas_migration`). Every case notebook runs
   `%run ./00_setup_load_data` first, so setting the widget once applies
   everywhere.

5. **Run any case notebook.** Each case is self-contained after the `%run`
   include: attach it to a cluster and click *Run all*.

## Conventions

- Pipe-delimited CSVs are read with `header=True`, `inferSchema=True`,
  `delimiter="|"` to match the original SAS numeric / string datatypes.
- Functions are imported as `from pyspark.sql import functions as F`
  (Databricks recommended short alias; the `fn` alias used in the markdown
  guides works identically).
- Results are rendered with Databricks-native `display()` instead of `.show()`
  so you get the interactive table / chart UI for free. `.show()` still works
  if you prefer plain-text output.
- Widgets (`dbutils.widgets`) are used for parameters — never hard-coded paths
  or values — so the notebooks can be scheduled as Databricks Jobs.
- The `%sql` cell in `case_14_sql.py` demonstrates the Databricks-idiomatic
  alternative to `spark.sql(...)` when you want syntax highlighting and the
  SQL results explorer.
