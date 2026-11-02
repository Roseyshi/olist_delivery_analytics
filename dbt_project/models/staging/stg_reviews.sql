with ranked as (
    select
        *,
        row_number() over (
            partition by order_id
            order by review_answer_timestamp desc
        ) as rn
    from {{ source('olist', 'order_reviews') }}
)
select
    review_id,
    order_id,
    review_score::int                       as review_score,
    review_creation_date::timestamp         as review_created_at,
    review_answer_timestamp::timestamp      as review_answered_at
from ranked
where rn = 1
