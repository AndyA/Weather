CREATE OR REPLACE VIEW v_windy AS
FROM read_json ('/data/weather/logs/windy/**/*.jsonl');

CREATE OR REPLACE VIEW v_dense AS
SELECT
  time,
  last_value ( c order by time ignore nulls ) over ( order by time ) as c,
  last_value ( s order by time ignore nulls ) over ( order by time ) as s,
  last_value ( g order by time ignore nulls ) over ( order by time ) as g,
  last_value ( t order by time ignore nulls ) over ( order by time ) as t,
  last_value ( r order by time ignore nulls ) over ( order by time ) as r,
  last_value ( p order by time ignore nulls ) over ( order by time ) as p,
  last_value ( h order by time ignore nulls ) over ( order by time ) as h,
  last_value ( b order by time ignore nulls ) over ( order by time ) as b,
from v_windy;

create or replace view v_rich as
select
  *,
  cos(radians (c)) * s as speed_n,
  sin(radians (c)) * s as speed_e,
  (t - 32) * 100 / (212 - 32) as temp
from
  v_dense;


CREATE
OR REPLACE VIEW v_minute AS
SELECT
  date_trunc('minute', time) as ts, 
  min(s) as min_s, max(s) as max_s, avg(s) as avg_s,
  min(g) as min_g, max(g) as max_g, avg(g) as avg_g,
  min(r) as min_r, max(r) as max_r, avg(r) as avg_r,
  min(p) as min_p, max(p) as max_p, avg(p) as avg_p,
  min(h) as min_h, max(h) as max_h, avg(h) as avg_h,
  min(b) as min_b, max(b) as max_b, avg(b) as avg_b,
  min(speed_n) as min_speed_n, max(speed_n) as max_speed_n, avg(speed_n) as avg_speed_n,
  min(speed_e) as min_speed_e, max(speed_e) as max_speed_e, avg(speed_e) as avg_speed_e,
  min(temp) as min_temp, max(temp) as max_temp, avg(temp) as avg_temp
FROM
  v_rich
GROUP BY
  ts;

CREATE
OR REPLACE VIEW v_hour AS
SELECT
  date_trunc('hour', time) as ts,
  min(s) as min_s, max(s) as max_s, avg(s) as avg_s,
  min(g) as min_g, max(g) as max_g, avg(g) as avg_g,
  min(r) as min_r, max(r) as max_r, avg(r) as avg_r,
  min(p) as min_p, max(p) as max_p, avg(p) as avg_p,
  min(h) as min_h, max(h) as max_h, avg(h) as avg_h,
  min(b) as min_b, max(b) as max_b, avg(b) as avg_b,
  min(speed_n) as min_speed_n, max(speed_n) as max_speed_n, avg(speed_n) as avg_speed_n,
  min(speed_e) as min_speed_e, max(speed_e) as max_speed_e, avg(speed_e) as avg_speed_e,
  min(temp) as min_temp, max(temp) as max_temp, avg(temp) as avg_temp
FROM
  v_rich
GROUP BY
  ts;
