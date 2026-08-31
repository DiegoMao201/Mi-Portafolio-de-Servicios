-- Esquema web para datovatenexuspro.com
-- Correr una sola vez: psql "$DATABASE_URL" -f migrations/001_init.sql

CREATE SCHEMA IF NOT EXISTS web;

CREATE TABLE IF NOT EXISTS web.leads (
  id              bigserial PRIMARY KEY,
  created_at      timestamptz NOT NULL DEFAULT now(),
  nombre          text,
  empresa         text,
  telefono        text,
  email           text,
  canal           text,
  mensaje         text,
  proceso_dolor   text,
  sistemas_actuales text,
  urgencia        text,
  calificacion    smallint,
  resumen_agente  text,
  origen_url      text,
  utm             jsonb,
  ip_hash         text,
  conversation_id bigint,
  notificado_at   timestamptz
);

CREATE TABLE IF NOT EXISTS web.conversations (
  id          bigserial PRIMARY KEY,
  created_at  timestamptz NOT NULL DEFAULT now(),
  session_id  text NOT NULL,
  ip_hash     text,
  modelo      text,
  tokens_in   integer DEFAULT 0,
  tokens_out  integer DEFAULT 0,
  costo_usd   numeric(10,5) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS web.messages (
  id              bigserial PRIMARY KEY,
  conversation_id bigint NOT NULL REFERENCES web.conversations(id) ON DELETE CASCADE,
  rol             text NOT NULL,
  contenido       text NOT NULL,
  created_at      timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS web.pages (
  slug        text PRIMARY KEY,
  servicio    text NOT NULL,
  industria   text,
  ciudad      text,
  h1          text NOT NULL,
  intro       text NOT NULL,
  bloques     jsonb NOT NULL,
  activo      boolean NOT NULL DEFAULT true,
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS web.metricas (
  clave       text PRIMARY KEY,
  etiqueta    text NOT NULL,
  valor       numeric NOT NULL,
  unidad      text,
  nota        text NOT NULL,
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS web.eventos (
  id          bigserial PRIMARY KEY,
  created_at  timestamptz NOT NULL DEFAULT now(),
  session_id  text,
  tipo        text NOT NULL,
  ruta        text,
  meta        jsonb
);

CREATE INDEX IF NOT EXISTS leads_created_idx ON web.leads (created_at DESC);
CREATE INDEX IF NOT EXISTS eventos_created_idx ON web.eventos (created_at DESC);
CREATE INDEX IF NOT EXISTS pages_activo_idx ON web.pages (activo, servicio);

-- Semilla de la consola del hero: TODAS las cifras deben ser verificables.
-- Ajustar 'anios_operando' al dato real antes de publicar.
INSERT INTO web.metricas (clave, etiqueta, valor, unidad, nota) VALUES
  ('clientes_gestionados', 'Clientes en sistemas propios', 434, NULL, 'Base de clientes de Bigotes y Paticas administrada por sistemas construidos por Diego'),
  ('pedidos_procesados', 'Pedidos procesados', 1456, NULL, 'Pedidos históricos gestionados por la plataforma de Bigotes y Paticas'),
  ('skus_sincronizados', 'Productos sincronizados', 467, NULL, 'Catálogo publicado y sincronizado automáticamente con Meta'),
  ('urls_indexables', 'URLs indexables generadas', 1027, NULL, 'Sitemap de un e-commerce construido y posicionado por Diego'),
  ('decision_ms', 'Latencia de decisión', 40, 'ms', 'Orden de magnitud de los motores de decisión en tiempo real que Diego opera')
ON CONFLICT (clave) DO NOTHING;
