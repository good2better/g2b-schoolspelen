const CACHE="g2b-schoolspelen-v13";
const ASSETS=["./","./index.html","./clips/groei.mp4","./clips/feest.mp4","./clips/ziggy-hop.mp4",
"./clips/balto.mp4","./clips/boerderij.mp4","./clips/dierenhelden.mp4","./clips/gevoelens.mp4","./clips/helden.mp4","./clips/keesje.mp4","./clips/klas.mp4","./clips/kleuren.mp4","./clips/koreaans.mp4","./clips/letters.mp4","./clips/moed.mp4","./clips/moed2.mp4","./clips/sam.mp4","./clips/seizoenen.mp4","./clips/sunny.mp4","./clips/tellen.mp4","./clips/topo.mp4","./clips/verkeer.mp4","./clips/vormen.mp4","./clips/weekdagen.mp4","./clips/ziggy.mp4"];
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
