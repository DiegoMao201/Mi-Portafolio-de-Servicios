import postgres from 'postgres';

// La base de datos es opcional: sin DATABASE_URL el sitio funciona completo
// (el chat no persiste y los leads llegan solo por correo).
let _sql: ReturnType<typeof postgres> | null = null;

export function db() {
  if (!process.env.DATABASE_URL) return null;
  if (!_sql) {
    _sql = postgres(process.env.DATABASE_URL, {
      max: 5,
      idle_timeout: 30,
      connect_timeout: 10,
    });
  }
  return _sql;
}

export type LeadInput = {
  nombre?: string;
  empresa?: string;
  telefono?: string;
  email?: string;
  canal: 'chat' | 'formulario';
  mensaje?: string;
  proceso_dolor?: string;
  sistemas_actuales?: string;
  urgencia?: string;
  calificacion?: number;
  resumen_agente?: string;
  origen_url?: string;
  ip_hash?: string;
  conversation_id?: number | null;
};

export async function saveLead(lead: LeadInput): Promise<number | null> {
  const sql = db();
  if (!sql) return null;
  try {
    const rows = await sql`
      INSERT INTO web.leads (nombre, empresa, telefono, email, canal, mensaje,
        proceso_dolor, sistemas_actuales, urgencia, calificacion, resumen_agente,
        origen_url, ip_hash, conversation_id)
      VALUES (${lead.nombre ?? null}, ${lead.empresa ?? null}, ${lead.telefono ?? null},
        ${lead.email ?? null}, ${lead.canal}, ${lead.mensaje ?? null},
        ${lead.proceso_dolor ?? null}, ${lead.sistemas_actuales ?? null},
        ${lead.urgencia ?? null}, ${lead.calificacion ?? null}, ${lead.resumen_agente ?? null},
        ${lead.origen_url ?? null}, ${lead.ip_hash ?? null}, ${lead.conversation_id ?? null})
      RETURNING id`;
    return rows[0]?.id ?? null;
  } catch (e) {
    console.error('[db] saveLead falló:', e);
    return null;
  }
}

export async function monthSpendUSD(): Promise<number> {
  const sql = db();
  if (!sql) return 0;
  try {
    const rows = await sql`
      SELECT COALESCE(SUM(costo_usd), 0)::float AS total
      FROM web.conversations
      WHERE created_at >= date_trunc('month', now())`;
    return rows[0]?.total ?? 0;
  } catch {
    return 0;
  }
}

export async function logConversation(args: {
  session_id: string; ip_hash: string; modelo: string;
  tokens_in: number; tokens_out: number; costo_usd: number;
  mensajes: { rol: string; contenido: string }[];
}): Promise<number | null> {
  const sql = db();
  if (!sql) return null;
  try {
    const rows = await sql`
      INSERT INTO web.conversations (session_id, ip_hash, modelo, tokens_in, tokens_out, costo_usd)
      VALUES (${args.session_id}, ${args.ip_hash}, ${args.modelo},
              ${args.tokens_in}, ${args.tokens_out}, ${args.costo_usd})
      RETURNING id`;
    const id = rows[0]?.id ?? null;
    if (id) {
      for (const m of args.mensajes) {
        await sql`INSERT INTO web.messages (conversation_id, rol, contenido)
                  VALUES (${id}, ${m.rol}, ${m.contenido})`;
      }
    }
    return id;
  } catch (e) {
    console.error('[db] logConversation falló:', e);
    return null;
  }
}

export type Metrica = { clave: string; etiqueta: string; valor: number; unidad: string | null; nota: string };

export async function getMetricas(): Promise<Metrica[] | null> {
  const sql = db();
  if (!sql) return null;
  try {
    const rows = await sql`SELECT clave, etiqueta, valor::float AS valor, unidad, nota FROM web.metricas ORDER BY clave`;
    return rows.length ? (rows as unknown as Metrica[]) : null;
  } catch {
    return null;
  }
}
