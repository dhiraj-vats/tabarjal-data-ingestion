-- PQM OPC UA node ids used by /api/v1/pqm/readings/opc-ingest.

UPDATE tb_source_components c
SET
    external_key = 'ns=6;s=Arp.Plc.Eclr/MCR_' || s.source_code || '_TOTAL_ACTIVE_POWER',
    updated_at = NOW()
FROM tb_data_sources s
WHERE s.id = c.source_id
  AND s.category = 'PQM'
  AND c.component_key = 'total_active_power';
