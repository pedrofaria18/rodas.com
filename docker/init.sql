
-- Cria tabela de documentos html
CREATE TABLE html_documents (
    id          SERIAL       PRIMARY KEY,
    url_hash    CHAR(32)     NOT NULL UNIQUE,
    html_hash   CHAR(32)     NOT NULL UNIQUE,
    url         VARCHAR(255) NOT NULL,
    html        TEXT         NOT NULL,
    visit_count INTEGER      NOT NULL DEFAULT 1,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Cria índice para buscas de documentos via hash
CREATE UNIQUE INDEX idx_url_hash  ON html_documents (url_hash);
CREATE UNIQUE INDEX idx_html_hash ON html_documents (html_hash);
