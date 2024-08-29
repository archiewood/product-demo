---
title: Product Dashboard
---


```sql monthly_active_users
select 
  date_trunc('month',session_date) as month,
  count(distinct user_id) as monthly_active_users
from sessions
group by all
order by month
```



```sql users_by_platform
select 
    platform,
    'Platform' as label,
    count(distinct user_id) as users,
    count(distinct user_id) / sum(count(distinct user_id)) over () as pct_users
from users
group by all
```


```sql users_by_country
select 
    country,
    count(distinct user_id) as users
from users
group by all
```

```sql monthly_cohort_retention
with abs as(
  select 
      date_trunc('month',session_date) as month,
      date_trunc('month',join_date) as cohort,
      date_diff('month', join_date, session_date) as cohort_age,
      cohort::varchar as cohort_label,
      count(distinct users.user_id) as users
  from sessions
  left join users on sessions.user_id = users.user_id
  group by all
  order by cohort, month
)
select 
    month,
    cohort,
    cohort_age,
    cohort_label,
    users * 1.0 / first_value(users) over (partition by cohort order by cohort_age) as retention
from abs
```

<Grid cols=2>

<AreaChart
  data={monthly_active_users}
  x=month
  y=monthly_active_users
  title='Monthly Active Users'
/>

<LineChart
  data={monthly_cohort_retention} 
  x=cohort_age
  y=retention
  yFmt=pct0
  yMin=0
  yMax=1
  series=cohort_label
  title='Monthly Cohort Retention'
/>

</Grid>


<AreaMap
  data={users_by_country}
  geoJsonUrl=https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson
  geoId=iso_a2
  areaCol=country
  value=users
  startingZoom=5
  title='Users by Country'
/>



```sql funnel
with onboarding_steps as (
  select
    user_id,
    step,
    completion_date
  from product.onboarding
)
select
  step,
  count(distinct user_id) as users,
  round(count(distinct user_id) / first_value(count(distinct user_id)) over (order by users desc),3) as pct_users
from onboarding_steps
group by step
order by users desc
```

<Grid cols=2>

<BarChart
  data={users_by_platform}
  x=label
  y=pct_users
  yMax=1.1
  yGridlines=false
  yAxisLabels=false
  yFmt=pct0
  series=platform
  title='Users by Platform'
  swapXY
  labels
/>

<FunnelChart
  data={funnel}
  nameCol=step
  valueCol=pct_users
  valueFmt=pct1
  title='Onboarding Funnel'
/>

</Grid>

