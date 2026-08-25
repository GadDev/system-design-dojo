-- Week 3 URL shortener lab
-- PostgreSQL reference schema.

CREATE TABLE IF NOT EXISTS links (
    id UUID PRIMARY KEY,
    user_id UUID NULL,
    short_code VARCHAR(16) NOT NULL UNIQUE,
    target_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NULL,
    deleted_at TIMESTAMPTZ NULL
);

-- The UNIQUE constraint on short_code creates the critical lookup index.
-- Explicitly show the expected access path:
--
-- SELECT target_url, expires_at, deleted_at
-- FROM links
-- WHERE short_code = $1;

CREATE INDEX IF NOT EXISTS idx_links_user_created
ON links (user_id, created_at DESC)
WHERE user_id IS NOT NULL;

-- Optional operational query:
--
-- Find expired rows for archival/cleanup.
CREATE INDEX IF NOT EXISTS idx_links_expires_at
ON links (expires_at)
WHERE expires_at IS NOT NULL AND deleted_at IS NULL;

-- Correctness reminder:
-- Expiration cleanup may be asynchronous.
-- Redirect logic must still check expires_at at read time.
