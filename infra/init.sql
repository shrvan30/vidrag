-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS vector;

-- =========================
-- VIDEOS TABLE (UPDATED)
-- =========================
CREATE TABLE IF NOT EXISTS videos (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_id  VARCHAR(20) UNIQUE,        -- 🔥 NEW (IMPORTANT)
  url_hash    VARCHAR(64) UNIQUE,
  source_url  TEXT,
  title       TEXT,
  duration_s  INTEGER,
  processed   BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMP DEFAULT NOW()
);

-- =========================
-- JOBS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS jobs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID REFERENCES videos(id),
  status      VARCHAR(20) DEFAULT 'pending',
  progress    FLOAT DEFAULT 0,
  error       TEXT,
  error_stage VARCHAR(50),
  created_at  TIMESTAMP DEFAULT NOW(),
  updated_at  TIMESTAMP DEFAULT NOW()
);

-- Auto update timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_jobs_timestamp
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- =========================
-- CHUNKS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS chunks (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID REFERENCES videos(id),
  chunk_index INTEGER NOT NULL,
  text        TEXT NOT NULL,
  start_s     FLOAT,
  end_s       FLOAT,
  embedding   VECTOR(384),
  source_type VARCHAR(20) DEFAULT 'speech'
);

-- Prevent duplicate chunks
ALTER TABLE chunks
ADD CONSTRAINT unique_chunk UNIQUE (video_id, chunk_index);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX idx_chunks_video_id ON chunks(video_id);
CREATE INDEX idx_jobs_video_id ON jobs(video_id);
CREATE INDEX idx_jobs_status ON jobs(status);

-- =========================
-- VECTOR INDEX
-- =========================
CREATE INDEX idx_chunks_embedding
ON chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- =========================
-- FULL TEXT SEARCH
-- =========================
ALTER TABLE chunks ADD COLUMN IF NOT EXISTS tsv tsvector;
CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON chunks USING GIN(tsv);