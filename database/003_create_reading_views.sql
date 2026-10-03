-- Pivot views for reporting.
-- One row per source + block_ts, component values as columns.

CREATE OR REPLACE VIEW vw_pqm_readings AS
SELECT
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts,
    MAX(r.value) FILTER (WHERE sc.component_key = 'total_active_power') AS total_active_power
FROM tb_pqm_readings r
JOIN tb_source_components sc ON sc.id = r.src_component_id
JOIN tb_data_sources ds ON ds.id = sc.source_id
WHERE r.is_deleted = FALSE
  AND ds.category = 'PQM'
GROUP BY
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts;

CREATE OR REPLACE VIEW vw_wms_readings AS
SELECT
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts,
    MAX(r.value) FILTER (WHERE sc.component_key = 'dni_wm2') AS dni_wm2,
    MAX(r.value) FILTER (WHERE sc.component_key = 'front_soil_sensor_1') AS front_soil_sensor_1,
    MAX(r.value) FILTER (WHERE sc.component_key = 'front_soil_sensor_2') AS front_soil_sensor_2,
    MAX(r.value) FILTER (WHERE sc.component_key = 'front_tr_loss_sensor_1') AS front_tr_loss_sensor_1,
    MAX(r.value) FILTER (WHERE sc.component_key = 'front_tr_loss_sensor_2') AS front_tr_loss_sensor_2,
    MAX(r.value) FILTER (WHERE sc.component_key = 'ghi_w') AS ghi_w,
    MAX(r.value) FILTER (WHERE sc.component_key = 'module_temperature_1') AS module_temperature_1,
    MAX(r.value) FILTER (WHERE sc.component_key = 'poa1_w') AS poa1_w,
    MAX(r.value) FILTER (WHERE sc.component_key = 'poa2_w') AS poa2_w,
    MAX(r.value) FILTER (WHERE sc.component_key = 'wind_direction') AS wind_direction,
    MAX(r.value) FILTER (WHERE sc.component_key = 'wind_speed') AS wind_speed
FROM tb_wms_readings r
JOIN tb_source_components sc ON sc.id = r.src_component_id
JOIN tb_data_sources ds ON ds.id = sc.source_id
WHERE r.is_deleted = FALSE
  AND ds.category = 'WMS'
GROUP BY
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts;

CREATE OR REPLACE VIEW vw_sacu_readings AS
SELECT
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts,
    MAX(r.value) FILTER (WHERE sc.component_key = 'sacu_dc_curr') AS sacu_dc_curr,
    MAX(r.value) FILTER (WHERE sc.component_key = 'sacu_active_power') AS sacu_active_power,
    MAX(r.value) FILTER (WHERE sc.component_key = 'sacu_plant_status_2') AS sacu_plant_status_2,
    MAX(r.value) FILTER (WHERE sc.component_key = 'sacu_inv_efficiency') AS sacu_inv_efficiency
FROM tb_sacu_readings r
JOIN tb_source_components sc ON sc.id = r.src_component_id
JOIN tb_data_sources ds ON ds.id = sc.source_id
WHERE r.is_deleted = FALSE
  AND ds.category = 'SACU'
GROUP BY
    ds.source_code,
    ds.source_name,
    ds.category,
    r.block_ts;

-- Usage examples:
-- SELECT * FROM vw_pqm_readings WHERE block_ts::date = CURRENT_DATE ORDER BY source_code, block_ts;
-- SELECT * FROM vw_wms_readings WHERE block_ts::date = CURRENT_DATE ORDER BY source_code, block_ts;
-- SELECT * FROM vw_sacu_readings WHERE block_ts::date = CURRENT_DATE ORDER BY source_code, block_ts;
