/* Afinador — Oficina Pernambuco | Cache offline de publicação.
 * Publique os arquivos juntos. Ao modificar qualquer recurso, regenere os hashes
 * e o identificador RELEASE (consulte o Manual Técnico). Não use skipWaiting:
 * uma atualização aguarda o fechamento das janelas da versão anterior.
 */
'use strict';
const RELEASE = "af6a330fcd8840f8cc74aba0";
const ASSETS = Object.freeze({
  "index.html": "ced36a9441fe1539a8661c8fb202c91cf9b95384878c0ef9b060d79f38d603e6",
  "manifest.webmanifest": "52cb25fe695960a82432fbd7f91efbb1ec43555013954d3a03434582295e12ab",
  "favicon.ico": "02581884f7cb2e69ba8d47386abf0ee33fbf1073ade3d3e8e0daf0c36848b357",
  "icons/icon-192.png": "b8c1a16d6dec1a6ee89ab960470e17d0db01db5720491eef91dec90fb4279835",
  "icons/icon-512.png": "2b0286c777b7d28bb91ec735b71d38a10a6d9bc972ea93afd514a41bfcd648f6",
  "icons/icon-maskable.png": "0b3f9a06929714463a6ec9cc188fd71e8bc3e1287372d15dce5142efceed2c9d"
});

const PREFIX = 'afinador-offline:' + self.registration.scope + ':';
const CACHE = PREFIX + RELEASE;
const scope = new URL(self.registration.scope);
const urls = new Map(Object.entries(ASSETS).map(([path, hash]) => [new URL(path, scope).href, hash]));
const index = new URL('index.html', scope).href;

async function verifiedFetch(url, expected) {
  const response = await fetch(url, {cache:'reload', credentials:'same-origin', redirect:'error'});
  if (!response.ok || response.status !== 200 || response.type === 'opaque') throw Error('Recurso offline indisponível: ' + url);
  const bytes = await response.clone().arrayBuffer();
  const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), x=>x.toString(16).padStart(2,'0')).join('');
  if (hash !== expected) throw Error('Publicação incompleta ou recurso divergente: ' + url);
  return response;
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    // Antes de escrever, verificar TODOS os recursos, inclusive o HTML. Uma
    // publicação incompleta não substitui a cópia ativa anterior.
    const entries = await Promise.all(Array.from(urls, async ([url, hash]) => [url, await verifiedFetch(url, hash)]));
    const existed = await caches.has(CACHE);
    const cache = await caches.open(CACHE);
    try {
      for (const [url, response] of entries) await cache.put(url, response);
    } catch (error) {
      if (!existed) await caches.delete(CACHE);
      throw error;
    }
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    // Somente caches pertencentes a esta aplicação e a este escopo.
    for (const name of await caches.keys()) {
      if (name.startsWith(PREFIX) && name !== CACHE) await caches.delete(name);
    }
    // Sem recarga forçada, sem tocar em IndexedDB/localStorage.
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== scope.origin) return;
  let key;
  if (req.mode === 'navigate') {
    if (url.pathname !== scope.pathname && url.pathname !== new URL(index).pathname) return;
    key = index;
  } else {
    if (!urls.has(url.href)) return;
    key = url.href;
  }
  event.respondWith((async () => {
    try {
      const cache = await caches.open(CACHE);
      const saved = await cache.match(key);
      if (saved) return saved;
      // Recuperação de recurso removido, sem misturar publicações.
      const response = await verifiedFetch(key, urls.get(key));
      await cache.put(key, response.clone());
      return response;
    } catch (error) {
      return new Response('Cópia offline indisponível. Conecte-se à internet e reabra o Afinador.', {
        status:503, headers:{'Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store'}
      });
    }
  })());
});
