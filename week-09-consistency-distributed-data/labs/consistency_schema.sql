-- PostgreSQL reference schema for Week 9.

CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    status text NOT NULL CHECK (status IN (
        'CREATED','QUEUED','PROCESSING','MERGING','COMPLETED','FAILED','CANCELLED'
    )),
    version bigint NOT NULL DEFAULT 0,
    expected_chunks integer NOT NULL CHECK (expected_chunks >= 0),
    completed_chunks integer NOT NULL DEFAULT 0 CHECK (completed_chunks >= 0),
    final_artifact_key text,
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (completed_chunks <= expected_chunks)
);

CREATE TABLE chunks (
    id uuid PRIMARY KEY,
    job_id uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    chunk_index integer NOT NULL,
    pipeline_version integer NOT NULL,
    status text NOT NULL CHECK (status IN ('PENDING','RUNNING','RETRYING','SUCCEEDED','FAILED','CANCELLED')),
    version bigint NOT NULL DEFAULT 0,
    artifact_key text,
    artifact_checksum text,
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(job_id, chunk_index, pipeline_version),
    CHECK (status <> 'SUCCEEDED' OR artifact_key IS NOT NULL)
);

CREATE TABLE outbox_events (
    event_id uuid PRIMARY KEY,
    aggregate_type text NOT NULL,
    aggregate_id uuid NOT NULL,
    aggregate_version bigint NOT NULL,
    event_type text NOT NULL,
    schema_version integer NOT NULL,
    payload jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    published_at timestamptz
);

CREATE INDEX outbox_unpublished_idx
ON outbox_events(created_at)
WHERE published_at IS NULL;

CREATE TABLE processed_events (
    consumer_name text NOT NULL,
    event_id uuid NOT NULL,
    processed_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (consumer_name, event_id)
);

-- Example optimistic transition:
-- UPDATE jobs
-- SET status='CANCELLED', version=version+1, updated_at=now()
-- WHERE id=:id AND version=:expected_version AND status IN ('CREATED','QUEUED','PROCESSING');

-- Example atomic merge claim:
-- UPDATE jobs
-- SET status='MERGING', version=version+1, updated_at=now()
-- WHERE id=:id
--   AND status='PROCESSING'
--   AND completed_chunks=expected_chunks;
