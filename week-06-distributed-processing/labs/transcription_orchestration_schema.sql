-- Week 6 reference schema: parent/child distributed transcription workflow.
-- PostgreSQL-oriented educational schema.

CREATE TYPE job_status AS ENUM (
  'created', 'preparing', 'processing', 'merging',
  'completed', 'cancelling', 'cancelled', 'failed'
);

CREATE TYPE chunk_status AS ENUM (
  'pending', 'running', 'retryable', 'succeeded', 'failed', 'cancelled'
);

CREATE TABLE jobs (
  id uuid PRIMARY KEY,
  upload_id uuid NOT NULL,
  status job_status NOT NULL DEFAULT 'created',
  desired_state job_status,
  pipeline_version integer NOT NULL,
  expected_chunks integer NOT NULL DEFAULT 0 CHECK (expected_chunks >= 0),
  completed_chunks integer NOT NULL DEFAULT 0 CHECK (completed_chunks >= 0),
  failed_chunks integer NOT NULL DEFAULT 0 CHECK (failed_chunks >= 0),
  merge_started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (completed_chunks <= expected_chunks),
  CHECK (failed_chunks <= expected_chunks)
);

CREATE TABLE chunks (
  id uuid PRIMARY KEY,
  job_id uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  chunk_index integer NOT NULL CHECK (chunk_index >= 0),
  start_ms bigint NOT NULL CHECK (start_ms >= 0),
  end_ms bigint NOT NULL CHECK (end_ms > start_ms),
  pipeline_version integer NOT NULL,
  status chunk_status NOT NULL DEFAULT 'pending',
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  worker_id text,
  output_uri text,
  output_checksum text,
  started_at timestamptz,
  finished_at timestamptz,
  UNIQUE(job_id, chunk_index, pipeline_version)
);

CREATE INDEX chunks_ready_idx
  ON chunks(job_id, chunk_index)
  WHERE status IN ('pending', 'retryable');

CREATE INDEX chunks_parent_status_idx
  ON chunks(job_id, status);

-- Example merge claim: only one caller can transition the parent.
-- Run only after child completion evidence has been reconciled.
--
-- UPDATE jobs
-- SET status = 'merging', merge_started_at = now()
-- WHERE id = :job_id
--   AND status = 'processing'
--   AND completed_chunks = expected_chunks;
