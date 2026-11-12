-- Ex-post labels are isolated from snapshot construction and portfolio selection.
SELECT d.decision_id, s.symbol,
       CASE WHEN entry.available_at <= ? AND exit_price.available_at <= ?
            THEN CAST(exit_price.open_cents - entry.open_cents AS DOUBLE) / entry.open_cents
            ELSE NULL END AS forward_return
FROM decisions d CROSS JOIN symbols s
LEFT JOIN market_opens entry ON entry.symbol = s.symbol AND entry.event_at = d.fill_at
LEFT JOIN market_opens exit_price ON exit_price.symbol = s.symbol AND exit_price.event_at = d.exit_at
ORDER BY d.decision_id, s.symbol;
