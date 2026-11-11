#!/usr/bin/env python3
"""Génère index.html : le lecteur mobile de la série (playlist, reprise, voix off seule).

    python3 outils/make_index.py

La page lit les fichiers du dépôt en chemins relatifs (videos/, voix-off/), donc elle
fonctionne telle quelle sur GitHub Pages ou en local (dossier ouvert dans le navigateur).
"""
import json, subprocess, yaml
import config

def duree(p):
    try:
        return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                                     "-of","csv=p=0",str(p)],capture_output=True,text=True).stdout)
    except Exception:
        return 0.0

eps=[]
for n in range(1,62):
    y=config.EPISODES_DIR/f"ep{n:02d}.yaml"
    if not y.exists(): continue
    d=yaml.safe_load(y.read_text(encoding="utf-8"))
    mp4=config.ROOT/"videos"/f"ep{n:02d}.mp4"
    eps.append({"n":n,"t":d.get("title",""),"s":d.get("source",""),
                "c":d.get("chapter","").split("—")[0].strip(),
                "d":round(duree(mp4)) if mp4.exists() else 0,
                "k":" ".join(d.get("subtitle","").split(" · "))})

HTML = """<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#070A16">
<title>Biologie &amp; Embryologie — 61 épisodes</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#070A16;color:#E9EDF7;
 padding-bottom:env(safe-area-inset-bottom)}
header{position:sticky;top:0;z-index:20;background:rgba(7,10,22,.92);backdrop-filter:blur(12px);
 border-bottom:1px solid rgba(255,255,255,.08)}
#player{width:100%;background:#000;display:block;aspect-ratio:9/16;max-height:62vh;object-fit:contain}
#player.audio{aspect-ratio:auto;height:64px}
.bar{padding:10px 14px;display:flex;gap:10px;align-items:center}
.bar .now{flex:1;min-width:0}
.bar .now b{display:block;font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar .now i{font-style:normal;font-size:12px;color:#8FA2C2}
.btn{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);color:#CFE2FF;
 border-radius:10px;padding:8px 11px;font-size:13px;font-weight:600;cursor:pointer}
.btn.on{background:#4DA3FF;color:#06101F;border-color:#4DA3FF}
.wrap{padding:14px 14px 40px;max-width:760px;margin:0 auto}
h1{font-size:21px;font-weight:800;letter-spacing:-.02em;margin-bottom:4px}
h1 span{color:#4DA3FF}
.sub{font-size:13px;color:#8FA2C2;margin-bottom:12px}
#q{width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.12);
 background:rgba(255,255,255,.05);color:#E9EDF7;font-size:16px;margin-bottom:14px}
.part{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#CFE2FF;font-weight:700;
 margin:18px 0 8px;padding:8px 12px;border-radius:9px;
 background:linear-gradient(90deg,rgba(77,163,255,.22),rgba(77,163,255,0))}
.ep{display:flex;gap:12px;align-items:center;padding:11px 12px;border-radius:13px;cursor:pointer;
 border:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.035);margin-bottom:8px}
.ep:active{background:rgba(77,163,255,.16)}
.ep.cur{border-color:#4DA3FF;background:rgba(77,163,255,.14)}
.ep .n{font-weight:800;font-size:13px;color:#06101F;background:#4DA3FF;border-radius:8px;
 padding:5px 8px;min-width:38px;text-align:center}
.ep.seen .n{background:#2C3A55;color:#9FB0CE}
.ep .m{flex:1;min-width:0}
.ep .m b{display:block;font-size:14.5px;font-weight:600;line-height:1.25}
.ep .m i{font-style:normal;font-size:12px;color:#8FA2C2}
.ep .d{font-size:12.5px;color:#FFD166;font-weight:700;white-space:nowrap}
.prog{height:3px;border-radius:2px;background:rgba(255,255,255,.1);margin-top:5px;overflow:hidden}
.prog>i{display:block;height:100%;background:#4DA3FF}
footer{color:#6F80A0;font-size:12px;text-align:center;padding:26px 14px}
</style></head><body>
<header>
 <video id="player" controls playsinline preload="metadata"></video>
 <div class="bar">
   <div class="now"><b id="nowT">Choisis un épisode</b><i id="nowS">61 épisodes · tout le syllabus</i></div>
   <button class="btn" id="audio" title="Voix off seule">🎧</button>
   <button class="btn" id="next">Suivant ›</button>
 </div>
</header>
<div class="wrap">
 <h1>Biologie &amp; Embryologie générale<br><span>la série en 61 épisodes</span></h1>
 <p class="sub">WMEDE1152 · UCLouvain · BA1 — reprend automatiquement où tu t'es arrêté.</p>
 <input id="q" placeholder="Chercher (méiose, placenta, ATP…)" autocomplete="off">
 <div id="list"></div>
</div>
<footer>Les vidéos sont lues depuis ce dépôt · 🎧 = voix off seule (léger en data)</footer>
<script>
const EPS = __DATA__;
const L=localStorage, list=document.getElementById('list'), v=document.getElementById('player');
let cur=null, audio=false;
const mmss=s=>s?Math.floor(s/60)+" min "+String(Math.round(s%60)).padStart(2,"0"):"";
const pad=n=>String(n).padStart(2,"0");
function render(f=""){
 list.innerHTML=""; let part="";
 const q=f.toLowerCase();
 for(const e of EPS){
  const hay=(e.n+" "+e.t+" "+e.k+" "+e.s).toLowerCase();
  if(q && !hay.includes(q)) continue;
  const p = e.n<=42 ? "Partie I — des molécules aux cellules" : "Partie II — des cellules à l'organisme";
  if(p!==part && !q){part=p;const h=document.createElement('div');h.className='part';h.textContent=p;list.appendChild(h);}
  const t=+(L.getItem('t'+e.n)||0), pc=e.d?Math.min(100,t/e.d*100):0;
  const d=document.createElement('div');
  d.className='ep'+(cur===e.n?' cur':'')+(pc>90?' seen':'');
  d.innerHTML=`<div class="n">${e.n}</div><div class="m"><b>${e.t}</b><i>${e.s}</i>
   ${pc>1?`<div class="prog"><i style="width:${pc}%"></i></div>`:''}</div><div class="d">${mmss(e.d)}</div>`;
  d.onclick=()=>play(e.n);
  list.appendChild(d);
 }
}
function play(n,seek=true){
 const e=EPS.find(x=>x.n===n); if(!e) return;
 cur=n; L.setItem('last',n);
 v.src=(audio?'voix-off/ep'+pad(n)+'.m4a':'videos/ep'+pad(n)+'.mp4');
 v.classList.toggle('audio',audio);
 const t=+(L.getItem('t'+n)||0);
 v.onloadedmetadata=()=>{ if(seek && t>5 && t<v.duration-15) v.currentTime=t; v.play().catch(()=>{}); };
 document.getElementById('nowT').textContent='Ép. '+n+' · '+e.t;
 document.getElementById('nowS').textContent=e.s;
 render(document.getElementById('q').value);
 window.scrollTo({top:0,behavior:'smooth'});
}
v.ontimeupdate=()=>{ if(cur&&v.currentTime>3) L.setItem('t'+cur,Math.floor(v.currentTime)); };
v.onended=()=>{ if(cur<61) play(cur+1); };
document.getElementById('next').onclick=()=>play((cur||0)+1<=61?(cur||0)+1:1);
document.getElementById('audio').onclick=e=>{
 audio=!audio; e.target.classList.toggle('on',audio);
 if(cur){const t=v.currentTime;play(cur,false);v.onloadedmetadata=()=>{v.currentTime=t;v.play().catch(()=>{});};}
};
document.getElementById('q').oninput=e=>render(e.target.value);
render();
const last=+(L.getItem('last')||0);
if(last){cur=last;const e=EPS.find(x=>x.n===last);
 document.getElementById('nowT').textContent='Reprendre : ép. '+last+' · '+e.t;
 document.getElementById('nowS').textContent=e.s+' · appuie pour lancer';
 v.src='videos/ep'+pad(last)+'.mp4';
 v.onloadedmetadata=()=>{const t=+(L.getItem('t'+last)||0); if(t>5&&t<v.duration-15) v.currentTime=t;};
 render();}
</script></body></html>"""

out = HTML.replace("__DATA__", json.dumps(eps, ensure_ascii=False))
(config.ROOT/"index.html").write_text(out, encoding="utf-8")
print(f"index.html écrit — {len(eps)} épisodes, {sum(e['d'] for e in eps)//60} min")
