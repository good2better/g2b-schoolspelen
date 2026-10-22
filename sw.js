const CACHE="g2b-schoolspelen-v26";
// Klein precache: de app zelf is meteen klaar. Clips & boekplaatjes
// cachen lazy bij eerste gebruik (install bleef anders ~13 MB blokkeren).
const ASSETS=["./","./index.html","./jufjet.png","./meestermo.png"];
const LAZY=/\.(mp4|jpg|jpeg|png|webp|gif|wav)$/;
self.addEventListener("install",function(e){
 e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ASSETS);}).then(function(){return self.skipWaiting();}));
});
self.addEventListener("activate",function(e){
 e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));
});
self.addEventListener("fetch",function(e){
 e.respondWith(caches.match(e.request).then(function(r){
  if(r)return r;
  return fetch(e.request).then(function(resp){
   if(e.request.method==="GET"&&resp.ok&&new URL(e.request.url).origin===location.origin&&LAZY.test(e.request.url)){
    var kopie=resp.clone();caches.open(CACHE).then(function(c){c.put(e.request,kopie);});
   }
   return resp;
  });
 }));
});
