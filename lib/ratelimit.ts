import { createHash } from 'crypto';

// Límite en memoria: suficiente para una sola instancia detrás de Coolify.
const buckets = new Map<string, { count: number; reset: number }>();

export function ipHash(ip: string): string {
  return createHash('sha256').update(ip + (process.env.SITE_URL || 'datovate')).digest('hex').slice(0, 16);
}

export function allow(key: string, max: number, windowMs: number): boolean {
  const now = Date.now();
  const b = buckets.get(key);
  if (!b || b.reset < now) {
    buckets.set(key, { count: 1, reset: now + windowMs });
    return true;
  }
  if (b.count >= max) return false;
  b.count += 1;
  return true;
}

export function clientIp(req: Request): string {
  const fwd = req.headers.get('x-forwarded-for');
  return (fwd ? fwd.split(',')[0].trim() : '') || req.headers.get('x-real-ip') || '0.0.0.0';
}
