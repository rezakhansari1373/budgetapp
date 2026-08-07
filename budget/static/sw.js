const CACHE = 'budget-v1';

self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE));
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function (event) {
  const req = event.request;
  if (req.method !== 'GET' || !req.url.startsWith(self.location.origin)) return;
  if (req.url.includes('/export_transactions/')) return;

  event.respondWith(
    fetch(req)
      .then(function (res) {
        if (res && res.status === 200 && (req.mode === 'navigate' || req.destination === 'style' || req.destination === 'script' || req.destination === 'image')) {
          const clone = res.clone();
          caches.open(CACHE).then(function (cache) { cache.put(req, clone); });
        }
        return res;
      })
      .catch(function () {
        return caches.match(req).then(function (cached) {
          if (cached) return cached;
          if (req.mode === 'navigate') return caches.match('/login/');
          return new Response('', { status: 503, statusText: 'Offline' });
        });
      })
  );
});
