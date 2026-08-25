CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS transcripts CASCADE;
DROP TABLE IF EXISTS chunks CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS uploads CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE uploads (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES users(id),
    object_key text NOT NULL UNIQUE,
    content_hash text,
    file_size_bytes bigint NOT NULL CHECK (file_size_bytes > 0),
    duration_seconds integer CHECK (duration_seconds > 0),
    status text NOT NULL CHECK (status IN ('pending', 'uploading', 'ready', 'deleted')),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id uuid NOT NULL REFERENCES uploads(id),
    user_id uuid NOT NULL REFERENCES users(id),
    status text NOT NULL CHECK (status IN ('queued', 'processing', 'retrying', 'completed', 'failed')),
    total_chunks integer NOT NULL DEFAULT 0 CHECK (total_chunks >= 0),
    completed_chunks integer NOT NULL DEFAULT 0 CHECK (completed_chunks >= 0),
    provider_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (completed_chunks <= total_chunks)
);

CREATE TABLE chunks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    chunk_index integer NOT NULL CHECK (chunk_index >= 0),
    start_ms integer NOT NULL CHECK (start_ms >= 0),
    end_ms integer NOT NULL CHECK (end_ms > start_ms),
    status text NOT NULL CHECK (status IN ('queued', 'processing', 'retryable', 'done', 'failed')),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    next_retry_at timestamptz,
    text text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (job_id, chunk_index)
);

CREATE TABLE transcripts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id uuid NOT NULL UNIQUE REFERENCES jobs(id) ON DELETE CASCADE,
    storage_kind text NOT NULL CHECK (storage_kind IN ('postgres', 'object', 'hybrid')),
    text_body text,
    object_key text,
    byte_size bigint,
    checksum text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (
        (storage_kind = 'postgres' AND text_body IS NOT NULL)
        OR (storage_kind = 'object' AND object_key IS NOT NULL)
        OR (storage_kind = 'hybrid' AND object_key IS NOT NULL)
    )
);

-- Baseline indexes tied to known access patterns.
CREATE INDEX idx_uploads_user_created
ON uploads(user_id, created_at DESC);

CREATE INDEX idx_jobs_user_created
ON jobs(user_id, created_at DESC);

CREATE INDEX idx_chunks_job_index
ON chunks(job_id, chunk_index);

CREATE INDEX idx_chunks_retryable
ON chunks(next_retry_at)
WHERE status = 'retryable';

-- Optional lab index: uncomment after testing JSONB queries.
-- CREATE INDEX idx_jobs_provider_metadata_gin
-- ON jobs USING GIN(provider_metadata);
