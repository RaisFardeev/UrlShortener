#1
SELECT
    user_id,
    SUM(reward) AS total_reward_2022
FROM
    reports
WHERE
    user_id IN (
        SELECT
            user_id
        FROM
            reports
        GROUP BY
            user_id
        HAVING
            MIN(created_at) >= '2021-01-01' AND MIN(created_at) < '2022-01-01'
    )
    AND created_at >= '2022-01-01'
    AND created_at < '2023-01-01'
GROUP BY
    user_id;

#2
SELECT
    r.barcode,
    r.price,
    p.title
FROM
    reports r
JOIN
    pos p
ON
    r.pos_id = p.id
GROUP BY
    p.title, r.barcode, r.price
HAVING
    COUNT(p.title) > 1;