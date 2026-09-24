CREATE OR REPLACE VIEW v_windy AS FROM read_json ('sample.jsonl');

CREATE OR REPLACE VIEW v_dense AS
SELECT
  time,
  last_value ( b order by time ignore nulls ) over ( order by time ) as b
FROM v_windy;

-- INTERNAL Error:
-- Attempted to access index 1048640 within vector of size 1048640

from v_dense limit 3;
