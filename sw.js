const CACHE="g2b-schoolspelen-v6";
const ASSETS=["./","./index.html","./clips/groei.mp4","./clips/feest.mp4","./clips/ziggy-hop.mp4"];
["sam","sunny","ziggy","keesje"].forEach(function(d){
 const n={sam:12,sunny:12,ziggy:9,keesje:6}[d];
 for(let i=0;i<n;i++)ASSETS.push("./"+d+"/p"+i+".jpg");
});
self.addEventListener("install",function(e){
 e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ASSETS);}).then(function(){return self.skipWaiting();}));
});
self.addEventListener("activate",function(e){
 e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));
});
self.addEventListener("fetch",function(e){
 e.respondWith(caches.match(e.request).then(function(r){return r||fetch(e.request);}));
});
