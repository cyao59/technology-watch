
### request table without compute many giga
SELECT
    *
FROM
    `project-id.dataset-id.table_name` 
TABLESAMPLE SYSTEM (1 PERCENT)