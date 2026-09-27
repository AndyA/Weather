-- CREATE OR REPLACE VIEW v_windy AS
-- FROM read_json ('/data/weather/logs/windy/**/*.jsonl');
-- 
-- CREATE OR REPLACE VIEW v_dense AS
-- SELECT
--   time,
--   last_value(c order by time ignore nulls) over (order by time) AS c,
--   last_value(s order by time ignore nulls) over (order by time) AS s,
--   last_value(g order by time ignore nulls) over (order by time) AS g,
--   last_value(t order by time ignore nulls) over (order by time) AS t,
--   last_value(r order by time ignore nulls) over (order by time) AS r,
--   last_value(p order by time ignore nulls) over (order by time) AS p,
--   last_value(h order by time ignore nulls) over (order by time) AS h,
--   last_value(b order by time ignore nulls) over (order by time) AS b,
-- from v_windy;

CREATE OR REPLACE TABLE v_dense AS
FROM read_json ('tmp/windy.jsonl');


CREATE OR REPLACE VIEW v_rich AS
SELECT
  *,
  cos(radians(c)) * s AS speed_n,
  sin(radians(c)) * s AS speed_e,
  (t - 32) * 5 / 9 AS temp
FROM V_DENSE;


CREATE OR REPLACE VIEW v_minute AS
SELECT
  date_trunc('minute', time) AS ts, 
  min(s) AS min_s, max(s) AS max_s, avg(s) AS avg_s,
  min(g) AS min_g, max(g) AS max_g, avg(g) AS avg_g,
  min(r) AS min_r, max(r) AS max_r, avg(r) AS avg_r,
  min(p) AS min_p, max(p) AS max_p, avg(p) AS avg_p,
  min(h) AS min_h, max(h) AS max_h, avg(h) AS avg_h,
  min(b) AS min_b, max(b) AS max_b, avg(b) AS avg_b,
  min(speed_n) AS min_speed_n, max(speed_n) AS max_speed_n, avg(speed_n) AS avg_speed_n,
  min(speed_e) AS min_speed_e, max(speed_e) AS max_speed_e, avg(speed_e) AS avg_speed_e,
  min(temp) AS min_temp, max(temp) AS max_temp, avg(temp) AS avg_temp
FROM v_rich
GROUP BY ts;

CREATE OR REPLACE VIEW v_hour AS
SELECT
  date_trunc('hour', time) AS ts,
  min(s) AS min_s, max(s) AS max_s, avg(s) AS avg_s,
  min(g) AS min_g, max(g) AS max_g, avg(g) AS avg_g,
  min(r) AS min_r, max(r) AS max_r, avg(r) AS avg_r,
  min(p) AS min_p, max(p) AS max_p, avg(p) AS avg_p,
  min(h) AS min_h, max(h) AS max_h, avg(h) AS avg_h,
  min(b) AS min_b, max(b) AS max_b, avg(b) AS avg_b,
  min(speed_n) AS min_speed_n, max(speed_n) AS max_speed_n, avg(speed_n) AS avg_speed_n,
  min(speed_e) AS min_speed_e, max(speed_e) AS max_speed_e, avg(speed_e) AS avg_speed_e,
  min(temp) AS min_temp, max(temp) AS max_temp, avg(temp) AS avg_temp
FROM v_rich
GROUP BY ts;
