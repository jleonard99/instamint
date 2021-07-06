with link_cte as (
select
  username1,
  posted_link,
  1 as x,
  case when posted_link_datetime is NULL then 1 else 0 end as y
from
  taggedLinksActivity
group by
  username1,
  posted_link
)
select
  username1,
  sum(x) as x,
  sum(y) as y
from
  link_cte
group by
  username1
  