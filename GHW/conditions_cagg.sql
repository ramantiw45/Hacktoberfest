CREATE MATERIALIZED VIEW public.conditions_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS hour,
    device,
    avg(temperature) AS temperature_avg,
    max(temperature) AS temperature_max,
    min(temperature) AS temperature_min,
    avg(humidity) AS humidity_avg,
    max(humidity) AS humidity_max,
    min(humidity) AS humidity_min
FROM public.conditions
GROUP BY hour, device
WITH NO DATA;

CREATE INDEX conditions_hourly_hour_device_idx
    ON public.conditions_hourly (hour DESC, device);

CALL refresh_continuous_aggregate('public.conditions_hourly', NULL, NULL);
