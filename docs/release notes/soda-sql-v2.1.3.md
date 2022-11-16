# Soda SQL 2.1.3: Gamling
2022-01-14


* Core: Change invalid keys message to a warning instead of error (#656)
* Core: submit a utc timestamp when creating scan (#651)
* Core: Remove explicit permission setting on yml files created (#642)
* Core: Fix SodaOTLPExporter constructor. Fixes #627 (#639)
* Core: Do not export non-soda spans in console and OTLP exporters. Fixes #627 (#632)
* Core: Fix exit code when running scans (#623)
* dbt: Add telemetry for ingest command (#655)
* dbt: Raise error if parsed results contain only null failures (#654)
* dbt: Resolve key access error when sources are not present in manifest (#646)
* dbt: Get artifacts from dbt Cloud via job_id (#647)
* BigQuery: Fix the create command (#653)
* SQLserver: Add encrypt, and trust_server_certificate options (#643)

Refer to the <a href="https://github.com/sodadata/soda-sql/blob/main/CHANGELOG.md" target="_blank">Soda SQL Changelog</a> for details.