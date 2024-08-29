---
title: Product Dashboard
---


```sql onboarding
select * from product.onboarding
```

```sql sessions
from product.sessions
```

```sql users
from product.users
```

```sql monthly_active_users
select 
    date_trunc('month',session_date) as month,
    count(distinct user_id) as monthly_active_users
from sessions
group by all
```

<AreaChart
  data={monthly_active_users}
  x=month
  y=monthly_active_users
  title='Monthly Active Users'
/>

```sql users_by_platform
select 
    platform,
    count(distinct user_id) as users
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
```


<LineChart
  data={monthly_cohort_retention} 
  x=cohort_age
  y=users
  series=cohort_label
/>


<AreaMap
  data={users_by_country}
  geoJsonUrl=https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson
  geoId=iso_a2
  areaCol=country
  value=users
  startingZoom=4
/>


