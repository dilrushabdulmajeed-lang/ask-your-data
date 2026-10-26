-- Read-only ClickHouse user for the agent. Guardrails enforced by the database, not the prompt:
--   readonly = 1          -> no INSERT/ALTER/DROP and no changing settings
--   max_execution_time    -> long-running queries are killed
--   max_result_rows       -> huge result sets are cut off
CREATE SETTINGS PROFILE OR REPLACE agent_profile SETTINGS
    readonly = 1,
    max_execution_time = 15,
    max_result_rows = 1000,
    result_overflow_mode = 'break',
    max_memory_usage = 2000000000;

CREATE USER OR REPLACE agent_reader IDENTIFIED WITH sha256_password BY '{password}'
    SETTINGS PROFILE agent_profile;

-- Only business tables; no access to the alert log or other databases.
GRANT SELECT ON analytics.ads_daily TO agent_reader;
GRANT SELECT ON analytics.campaigns TO agent_reader;
GRANT SELECT ON analytics.ads_performance TO agent_reader;
GRANT SELECT ON analytics.ecom_events TO agent_reader;
GRANT SELECT ON analytics.ecom_orders TO agent_reader;
GRANT SELECT ON analytics.ecom_users TO agent_reader;
GRANT SELECT ON analytics.ecom_products TO agent_reader;
GRANT SELECT ON analytics.ecom_rfm TO agent_reader;
GRANT SELECT ON analytics.ab_checkout_experiment TO agent_reader;
