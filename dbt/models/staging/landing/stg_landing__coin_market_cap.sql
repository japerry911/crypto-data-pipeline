with
    coin_market_cap_raw_data as (
        select * from {{ source("landing", "coin_market_cap") }}
    ),

    final as (
        select
            id as id,
            trim(name) as name,
            cast(cmc_rank as int64) as cmc_rank,
            cast(usd_price as float64) as usd_price,
            parse_datetime("%Y-%m-%d %H:%M:%S", datetime_fetched) as datetime_fetched
        from coin_market_cap_raw_data
    )

select *
from final
