-- CMRE migration 0001: pgvector extension + embedding indexes
--
-- Apply with:
--   psql "$CMRE_DATABASE_URL" -f db_migrations/0001_pgvector.sql
--
-- This migration is idempotent. Re-running it is safe.

CREATE EXTENSION IF NOT EXISTS vector;

-- Note: today's schema stores embeddings as JSON for portability.
-- When migrating to native vector columns, run:
--
--   ALTER TABLE claims
--     ADD COLUMN embedding_vec vector(384);
--
--   UPDATE claims
--     SET embedding_vec = embedding::vector
--     WHERE embedding IS NOT NULL;
--
--   ALTER TABLE claims DROP COLUMN embedding;
--
--   ALTER TABLE claims RENAME COLUMN embedding_vec TO embedding;
--
--   CREATE INDEX IF NOT EXISTS claims_embedding_hnsw
--     ON claims USING hnsw (embedding vector_cosine_ops);

-- For now, a soft index on JSON length helps the planner but doesn't enable
-- vector similarity. Once the migration above runs, replace this comment
-- block with the HNSW indexes for both claims and problem_profiles.

SELECT 'pgvector migration 0001 applied' AS status;
