/* Afinador — Oficina Pernambuco | Cache offline de publicação.
 * Publique os arquivos juntos. Ao modificar qualquer recurso, regenere os hashes
 * e o identificador RELEASE (consulte o Manual Técnico). Não use skipWaiting:
 * uma atualização aguarda o fechamento das janelas da versão anterior.
 */
'use strict';
const RELEASE = "207e3fa93b019e7120b62867";
const ASSETS = Object.freeze({
  "index.html": "92aad1a438becadd6fa7a291e0d48c1ed54af18015aad5e2ac00299b75e95e35",
  "manifest.webmanifest": "e864faf4860c52af1716d22b839cf97be51ba4c7065cbafcea68594363a777ca",
  "favicon.ico": "f3f4a7573e819a7feff4e42d50ea5b4087a1c599484ec93f869b133869fbb75c",
  "icons/icon-192.png": "52c7750241c69785ec8e7ea98aacfdabaf5afc7ce87433790402ef5453e1aa01",
  "icons/icon-512.png": "3039a58999045446e80899f9c1dea98250b1776b487dd334f0f5ff117de7c52d",
  "icons/icon-maskable.png": "662092c7a16a2ecc7e290fb2606bd750224a6e2083ec0ff0ae9815d93ba3d799",
  "favicon.ico?v=f3f4a7573e81": "f3f4a7573e819a7feff4e42d50ea5b4087a1c599484ec93f869b133869fbb75c",
  "icons/icon-192.png?v=52c7750241c6": "52c7750241c69785ec8e7ea98aacfdabaf5afc7ce87433790402ef5453e1aa01",
  "icons/icon-512.png?v=3039a5899904": "3039a58999045446e80899f9c1dea98250b1776b487dd334f0f5ff117de7c52d",
  "icons/icon-maskable.png?v=662092c7a16a": "662092c7a16a2ecc7e290fb2606bd750224a6e2083ec0ff0ae9815d93ba3d799"
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
