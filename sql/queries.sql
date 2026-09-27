-- CREATE OR REPLACE VIEW v_windy AS
-- FROM read_json('/data/weather/logs/windy/**/*.jsonl');
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
FROM read_json('tmp/windy.jsonl');

CREATE OR REPLACE VIEW v_rich AS
SELECT
  *,
  cos(radians(c)) * s AS sn,
  sin(radians(c)) * s AS se,
  (t - 32) * 5 / 9 AS tp
FROM v_dense;

CREATE OR REPLACE VIEW v_minute AS
SELECT
  date_trunc('minute', time) AS ts, 
  min(s)  AS ls,  max(s)  AS hs,  avg(s)  AS as,
  min(g)  AS lg,  max(g)  AS hg,  avg(g)  AS ag,
  min(r)  AS lr,  max(r)  AS hr,  avg(r)  AS ar,
  min(p)  AS lp,  max(p)  AS hp,  avg(p)  AS ap,
  min(h)  AS lh,  max(h)  AS hh,  avg(h)  AS ah,
  min(b)  AS lb,  max(b)  AS hb,  avg(b)  AS ab,
  min(sn) AS lsn, max(sn) AS hsn, avg(sn) AS asn,
  min(se) AS lse, max(se) AS hse, avg(se) AS ase,
  min(tp) AS ltp, max(tp) AS htp, avg(tp) AS atp
FROM v_rich
GROUP BY ts;

CREATE OR REPLACE VIEW v_hour AS
SELECT
  date_trunc('hour', time) AS ts, 
  min(s)  AS ls,  max(s)  AS hs,  avg(s)  AS as,
  min(g)  AS lg,  max(g)  AS hg,  avg(g)  AS ag,
  min(r)  AS lr,  max(r)  AS hr,  avg(r)  AS ar,
  min(p)  AS lp,  max(p)  AS hp,  avg(p)  AS ap,
  min(h)  AS lh,  max(h)  AS hh,  avg(h)  AS ah,
  min(b)  AS lb,  max(b)  AS hb,  avg(b)  AS ab,
  min(sn) AS lsn, max(sn) AS hsn, avg(sn) AS asn,
  min(se) AS lse, max(se) AS hse, avg(se) AS ase,
  min(tp) AS ltp, max(tp) AS htp, avg(tp) AS atp
FROM v_rich
GROUP BY ts;

CREATE OR REPLACE VIEW v_day AS
SELECT
  date_trunc('day', time) AS ts, 
  min(s)  AS ls,  max(s)  AS hs,  avg(s)  AS as,
  min(g)  AS lg,  max(g)  AS hg,  avg(g)  AS ag,
  min(r)  AS lr,  max(r)  AS hr,  avg(r)  AS ar,
  min(p)  AS lp,  max(p)  AS hp,  avg(p)  AS ap,
  min(h)  AS lh,  max(h)  AS hh,  avg(h)  AS ah,
  min(b)  AS lb,  max(b)  AS hb,  avg(b)  AS ab,
  min(sn) AS lsn, max(sn) AS hsn, avg(sn) AS asn,
  min(se) AS lse, max(se) AS hse, avg(se) AS ase,
  min(tp) AS ltp, max(tp) AS htp, avg(tp) AS atp
FROM v_rich
GROUP BY ts;
