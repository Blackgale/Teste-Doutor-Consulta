CREATE TABLE IF NOT EXISTS analytics.energy_measurements (
    reference_date DATE NOT NULL,
    subsystem STRING NOT NULL,
    metric_type STRING NOT NULL,
    value_mwmed NUMERIC NOT NULL,
    source STRING NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL
)
PARTITION BY reference_date
CLUSTER BY subsystem, metric_type;
