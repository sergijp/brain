// Захисний проксі: пропускає тільки POST на точний шлях вебхука до локального n8n, усе інше — 404.
import http from 'node:http';
import fs from 'node:fs';
const sec = Object.fromEntries(fs.readFileSync(process.env.HOME + '/tv-hook/secrets.env', 'utf8').split('\n').filter(l => l.includes('=')).map(l => l.split(/=(.*)/s).slice(0, 2)));
const ALLOWED = '/webhook/tv-' + sec.PATH_SECRET;
http.createServer((req, res) => {
  if (req.method !== 'POST' || req.url.split('?')[0] !== ALLOWED) { res.writeHead(404); return res.end('not found'); }
  const chunks = []; let size = 0;
  req.on('data', c => { size += c.length; if (size > 20000) { req.destroy(); } else chunks.push(c); });
  req.on('end', () => {
    const p = http.request({ host: '127.0.0.1', port: 5679, path: req.url, method: 'POST', headers: { 'content-type': req.headers['content-type'] || 'text/plain', 'content-length': Buffer.concat(chunks).length } }, r => { res.writeHead(r.statusCode || 200); r.pipe(res); });
    p.on('error', () => { res.writeHead(502); res.end('upstream'); });
    p.end(Buffer.concat(chunks));
  });
}).listen(5680, '127.0.0.1', () => console.log('proxy on 5680'));
