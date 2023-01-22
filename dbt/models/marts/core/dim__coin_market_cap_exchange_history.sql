with stg_landing_coin_market_cap_data as (
    select 
        id,
        name,
        cmc_rank,
        usd_price,
        datetime_fetched,
        row_number() over (partition by id, format_datetime('%Y-%m-%d', datetime_fetched) order by datetime_fetched desc) as instance_number
    from {{ ref('stg_landing__coin_market_cap') }}
),

final as (
    select
        format_datetime('%Y-%m-%d', datetime_fetched) as Date,
        id as Id,
        name as Currency_Name,
        cmc_rank as Coin_Market_Cap_Rank,
        usd_price as USD_Exchange_Price
    from stg_landing_coin_market_cap_data
    where instance_number = 1
)

select *
from final
