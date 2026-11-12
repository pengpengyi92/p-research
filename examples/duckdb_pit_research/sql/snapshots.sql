-- Choose known membership, then known revision per session, then latest sessions.
WITH membership_versions AS (
    SELECT d.decision_id, d.decision_at, m.symbol, m.membership_id, m.is_member,
           row_number() OVER (PARTITION BY d.decision_id, m.symbol
                             ORDER BY m.effective_at DESC, m.revision DESC) AS mr
    FROM decisions d JOIN memberships m ON m.effective_at <= d.decision_at
    AND (__MEMBERSHIP_GUARD__)
), active AS (
    SELECT * FROM membership_versions WHERE mr = 1 AND is_member
), known_versions AS (
    SELECT a.decision_id, a.decision_at, a.symbol, a.membership_id,
           f.feature_id, f.session, f.revision, f.close_cents, f.available_at,
           row_number() OVER (PARTITION BY a.decision_id, a.symbol, f.session
                             ORDER BY f.revision DESC) AS vr
    FROM active a LEFT JOIN __FEATURE_TABLE__ f ON f.symbol = a.symbol
       AND f.event_at <= a.decision_at AND (__FEATURE_GUARD__)
), sessions AS (
    SELECT *, row_number() OVER (PARTITION BY decision_id, symbol ORDER BY __SESSION_ORDER__) AS sr
    FROM known_versions WHERE vr = 1
), paired AS (
    SELECT decision_id, symbol, membership_id, decision_at,
           max(feature_id) FILTER (WHERE sr = 1) AS current_id,
           max(feature_id) FILTER (WHERE sr = 2) AS previous_id,
           max(close_cents) FILTER (WHERE sr = 1) AS current_close_cents,
           max(close_cents) FILTER (WHERE sr = 2) AS previous_close_cents,
           max(available_at) FILTER (WHERE sr = 1) AS current_available_at,
           max(available_at) FILTER (WHERE sr = 2) AS previous_available_at
    FROM sessions GROUP BY decision_id, symbol, membership_id, decision_at
)
SELECT decision_id, symbol, membership_id, CAST(decision_at AS VARCHAR) AS decision_at,
       current_id, previous_id, current_close_cents, previous_close_cents,
       CAST(current_available_at AS VARCHAR) AS current_available_at,
       CAST(previous_available_at AS VARCHAR) AS previous_available_at,
       CASE WHEN previous_id IS NULL THEN 'INSUFFICIENT_HISTORY'
               WHEN current_close_cents IS NULL OR previous_close_cents IS NULL THEN 'MISSING_VALUE'
               ELSE 'READY' END AS status,
          CASE WHEN previous_id IS NOT NULL AND current_close_cents IS NOT NULL AND previous_close_cents IS NOT NULL
               THEN CAST(current_close_cents - previous_close_cents AS DOUBLE) / previous_close_cents
               ELSE NULL END AS signal
FROM paired ORDER BY decision_id, symbol;
