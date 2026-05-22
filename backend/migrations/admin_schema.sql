-- Admin panel tables for LLM settings, prompts, and logs

CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prompts (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL UNIQUE,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    details TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_action ON logs (action);

-- Default LLM model (display name from admin dropdown)
INSERT INTO settings (key, value)
VALUES ('llm_model', 'Laguna M.1')
ON CONFLICT (key) DO NOTHING;
