MERGE analytics.energy_measurements AS target
USING staging.energy_measurements AS source
ON target.reference_date = source.reference_date
AND target.subsystem = source.subsystem
AND target.metric_type = source.metric_type
WHEN MATCHED AND (
    target.value_mwmed != source.value_mwmed
    OR target.source != source.source
) THEN
  UPDATE SET
    value_mwmed = source.value_mwmed,
    source = source.source,
    ingestion_timestamp = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (
    reference_date,
    subsystem,
    metric_type,
    value_mwmed,
    source,
    ingestion_timestamp
  )
  VALUES (
    source.reference_date,
    source.subsystem,
    source.metric_type,
    source.value_mwmed,
    source.source,
    CURRENT_TIMESTAMP()
  );
