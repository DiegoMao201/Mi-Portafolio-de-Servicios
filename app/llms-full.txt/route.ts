import { llmsCompleto } from '@/lib/llms';

export const dynamic = 'force-static';
export function GET() {
  return new Response(llmsCompleto(), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
