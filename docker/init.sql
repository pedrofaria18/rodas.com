
/* Cria tabela de documentos html */
CREATE TABLE html_document (
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
CREATE UNIQUE INDEX idx_html_doc_url_hash ON html_document (url_hash);
CREATE UNIQUE INDEX idx_html_doc_hash     ON html_document (html_hash);

-- Cria função para atualizar campos de timestamp em updates
CREATE  FUNCTION update_timestamp_html_doc()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at  = now();
    NEW.visit_count = NEW.visit_count + 1;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Cria trigger para atualizar campos de timestamp em updates
CREATE TRIGGER update_timestamp_html_doc
    BEFORE UPDATE
        ON html_document
       FOR EACH ROW
EXECUTE PROCEDURE update_timestamp_html_doc();


/* Cria tabela de falhas de download */
CREATE TABLE failed_download_log (
    id           SERIAL       PRIMARY KEY,
    url_hash     CHAR(32)     NOT NULL,
    url          VARCHAR(255) NOT NULL,
    last_status  TEXT         NOT NULL,
    num_of_tries INTEGER NOT  NULL     DEFAULT 1,
    last_try_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    first_try_at TIMESTAMP    NOT NULL DEFAULT NOW()
);
-- Cria índice para buscas de documentos via hash
CREATE UNIQUE INDEX idx_failed_url_hash ON failed_download_log (url_hash);

-- Cria função para atualizar campos de timestamp em updates
CREATE  FUNCTION update_timestamp_failed()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_try_at  = now();
    NEW.num_of_tries = NEW.num_of_tries + 1;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Cria trigger para atualizar campos de timestamp em updates
CREATE TRIGGER update_timestamp_failed
    BEFORE UPDATE
        ON failed_download_log
       FOR EACH ROW
EXECUTE PROCEDURE update_timestamp_failed();
