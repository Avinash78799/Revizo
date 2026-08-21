# NEET-PG Platform: Staging Execution & Operator Runbook

This document defines the exact step-by-step procedure for staging operators to spin up the live environment, execute database migrations, verify PostgreSQL Row-Level Security (RLS), test pgvector and distributed Redis rate limiting, and complete the final reality gate.

---

## 1. Prerequisites

Ensure the following are installed and verified on the staging host:
- Docker Desktop or Docker Engine ($\ge 24.0.0$) with Docker Compose V2
- Python 3.11+ / 3.12+ with virtual environment configured
- PostgreSQL Client (`psql`, `pg_dump`, `pg_isready`)
- OpenSSL (for token generation)

---

## 2. Environment Configuration

1. Copy `.env.example` to `.env.staging` in the `backend/` directory:
   ```bash
   cp backend/.env.example backend/.env.staging
   ```
2. Populate the required environment variables with secure, randomly generated secrets:
   ```bash
   export POSTGRES_USER="neetpg_staging_admin"
   export POSTGRES_PASSWORD=$(openssl rand -hex 24)
   export POSTGRES_DB="neetpg_staging"
   export REDIS_PASSWORD=$(openssl rand -hex 24)
   export STAGING_SECRET_KEY=$(openssl rand -hex 32)
   ```

---

## 3. Docker Startup & Health Checks

1. Start staging containers in detached mode:
   ```bash
   docker compose -f backend/docker-compose.staging.yml up -d
   ```
2. Verify container statuses:
   ```bash
   docker compose -f backend/docker-compose.staging.yml ps
   ```
3. Check container health probes:
   ```bash
   docker inspect --format='{{json .State.Health.Status}}' neetpg-postgres-staging
   docker inspect --format='{{json .State.Health.Status}}' neetpg-redis-staging
   docker inspect --format='{{json .State.Health.Status}}' neetpg-api-staging
   ```

---

## 4. Database Migrations (Authoritative Schema Creation)

1. Set the migration database URL:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
   ```
2. Execute Alembic migrations to head:
   ```bash
   cd backend
   alembic upgrade head
   ```
3. Verify current revision:
   ```bash
   alembic current
   ```
4. Test downgrade/rollback support:
   ```bash
   alembic downgrade -1
   alembic upgrade head
   ```

---

## 5. Live PostgreSQL Row-Level Security (RLS) Execution

1. Apply PostgreSQL RLS policies from `database/rls_policies.sql`:
   ```bash
   PGPASSWORD="${POSTGRES_PASSWORD}" psql -h localhost -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -f ../database/rls_policies.sql
   ```
2. Run the real PostgreSQL RLS test suite:
   ```bash
   export POSTGRES_TEST_DATABASE_URL="${DATABASE_URL}"
   pytest tests/integration/test_postgres_rls.py -v
   ```
   *Expected Result*: `PASSED` (0 skipped, 0 failed).

---

## 6. pgvector Reality Verification

1. Verify the `vector` extension is active:
   ```sql
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```
2. Test vector embedding insertion and cosine distance calculation ($1536$ dimensions):
   ```sql
   INSERT INTO concepts (id, topic_id, name, embedding)
   VALUES ('test-concept-vector', 'test-topic', 'Vector Test', '[0.01, 0.02, ...]');
   
   SELECT name, embedding <=> '[0.01, 0.02, ...]' AS cosine_distance 
   FROM concepts 
   ORDER BY cosine_distance LIMIT 1;
   ```

---

## 7. Distributed Redis Rate Limiting Verification

1. Run multiple worker instances against Redis:
   ```bash
   export REDIS_URL="redis://:${REDIS_PASSWORD}@localhost:6379/0"
   pytest tests/unit/ -k "rate_limit" -v
   ```
2. Verify rate limit counters increment and expire in Redis:
   ```bash
   docker exec -it neetpg-redis-staging redis-cli -a "${REDIS_PASSWORD}" KEYS "ratelimit:*"
   ```

---

## 8. Real Backup & Restore Verification

1. Create live snapshot:
   ```bash
   python scripts/db_backup_restore.py --action backup --db-url "${DATABASE_URL}" --output staging_backup.sql
   ```
2. Calculate SHA-256 digest:
   ```bash
   sha256sum staging_backup.sql
   ```
3. Restore into clean test database:
   ```bash
   python scripts/db_backup_restore.py --action restore --db-url "${RESTORE_DATABASE_URL}" --input staging_backup.sql
   ```
4. Confirm restored table rows and migration revision.

---

## 9. Concurrency & Performance Suite

Execute high-concurrency load testing against PostgreSQL + Redis:
```bash
pytest tests/integration/test_concurrency_and_performance.py -v
```

---

## 10. Security Regression Suite

Execute the 12 complete security suites:
```bash
pytest tests/security/ tests/unit/test_security.py -v
```

---

## 11. Full Regression Suite

Execute all tests across integration, security, and unit suites:
```bash
pytest tests -v
```

---

## 12. Rollback & Shutdown Procedure

1. To tear down staging containers without data loss:
   ```bash
   docker compose -f backend/docker-compose.staging.yml down
   ```
2. To completely purge staging volumes for clean re-test:
   ```bash
   docker compose -f backend/docker-compose.staging.yml down -v
   ```

---

## 13. Evidence to Capture for Milestone Review

Before requesting gate signoff, capture:
- `docker ps` container table
- `psql` PostgreSQL version (`SELECT version();`) and pgvector version (`SELECT extversion FROM pg_extension WHERE extname = 'vector';`)
- `alembic current` output
- `pytest tests/integration/test_postgres_rls.py` terminal output showing `PASSED`
- Backup SHA-256 checksum and restore log
- Full pytest summary (`XX passed, 0 failed, 0 skipped`)

---

## 14. Exact GO / NO-GO Criteria

The staging reality gate may transition from `BLOCKED` to `PASSED` **only if**:
- `test_postgres_rls.py` executed live and returned `PASSED` (not skipped).
- Alembic migrations cleanly upgraded to head.
- pgvector cosine similarity queries executed.
- Redis shared rate limiting tested across multiple processes.
- Backup created, restored, and validated.
- All 100 backend tests and 16 frontend routes passed without errors.

```
Final Platform Status remains:
STATUS = CONTROLLED BETA / CONTENT LIMITED
NOT: STATUS = MEDICALLY VERIFIED PRODUCTION
until genuine medical content review is completed by qualified doctors.
```
