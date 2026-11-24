#!/usr/bin/env python3
"""Generate the SHIELD-AI interactive HTML explorer (`shield_ai_explorer.html`).

A SINGLE self-contained file, emitted from the explorer graph of record
(assets/shield-ai-explorer-graph.json): the graph is embedded as a JSON block
inside the page, and a small vanilla-JS viewer renders three linked views:

  * Facet sidebar -- search box + pillar filter + severity filter; live counts
  * Detail pane   -- click any incident/control/gap/exploit/pillar to drill in
                     and navigate to its linked neighbours (drill-down)
  * Graph pane    -- an SVG neighbourhood view of the selected entity, drawn
                     from the graph's derived edges (up to 2 hops)

There is no framework, no build step beyond this generator, and no CDN or
external resource -- the file works offline and over `file://`. Because it is
derived at build time and gated byte-exact (see --check), the viewer can never
drift from the sources that build the graph. The `<` character in the embedded
graph JSON is escaped to \\u003c so it can never terminate the script block.

Usage:
    python3 tools/generate_explorer_html.py --write   # write shield_ai_explorer.html
    python3 tools/generate_explorer_html.py --check   # fail if committed file
                                                      # differs from fresh
    python3 tools/generate_explorer_html.py           # print to stdout
"""
import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GRAPH = os.path.join(ROOT, "assets", "shield-ai-explorer-graph.json")
OUT = os.path.join(ROOT, "shield_ai_explorer.html")

# The viewer template. {GRAPH_DATA} is replaced with the escaped JSON; the rest
# of the file is static and self-contained (vanilla JS + inline CSS).
VIEWER = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SHIELD-AI Explorer</title>
<style>
:root{ --bg:#0f1520; --panel:#16202e; --line:#2a3a52; --ink:#dbe6f4; --mut:#8aa0bd;
  --acc:#5b9cf5; --ok:#3dbb6a; --warn:#e0a63c; --crit:#e05a5a; }
*{box-sizing:border-box; margin:0; padding:0;}
body{font:14px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg); color:var(--ink);}
header{padding:14px 20px; border-bottom:1px solid var(--line); display:flex;
  align-items:baseline; gap:14px; flex-wrap:wrap;}
header h1{font-size:18px; font-weight:700;} header .meta{color:var(--mut); font-size:12px;}
#wrap{display:grid; grid-template-columns:280px 1fr; grid-template-rows:1fr 1fr;
  height:calc(100vh - 57px); gap:10px; padding:10px;}
.panel{background:var(--panel); border:1px solid var(--line); border-radius:8px;
  overflow-y:auto;}
.panel h3{padding:10px 14px; border-bottom:1px solid var(--line); font-size:13px;
  text-transform:uppercase; letter-spacing:.04em; color:var(--mut);}
#sidebar{grid-row:1 / span 2;}
#sidebar .inner{padding:10px 14px;}
#search{width:100%; padding:8px; border-radius:6px; border:1px solid var(--line);
  background:#0b1018; color:var(--ink); margin-bottom:10px;}
.facet-block{margin-bottom:12px;}
.facet-block label{display:block; color:var(--mut); font-size:12px; margin-bottom:4px;}
.facet-block input[type=text]{width:100%; padding:7px; border-radius:6px;
  border:1px solid var(--line); background:#0b1018; color:var(--ink);}
.check{display:flex; align-items:center; gap:8px; padding:3px 0;}
.check span{cursor:default;}
.count{color:var(--mut); font-size:11px;}
#facets .result{display:block; text-align:left; width:100%; padding:6px 8px;
  border-radius:6px; border:none; background:transparent; color:var(--ink);
  cursor:pointer;}
#facets .result:hover{background:#1e2c40;}
#facets .result .n{color:var(--mut); font-size:11px;}
#detail .inner{padding:14px;}
#detail h2{font-size:16px; margin-bottom:6px;}
#detail .kv{display:flex; flex-wrap:wrap; gap:10px 22px; margin:10px 0;}
#detail .kv b{display:block; color:var(--mut); font-size:11px; text-transform:uppercase;}
#detail .chip{display:inline-block; background:#1e2c40; border:1px solid var(--line);
  border-radius:20px; padding:2px 10px; margin:2px 3px; cursor:pointer;}
#detail .chip:hover{border-color:var(--acc);}
#detail p{color:var(--mut); margin-top:8px;}
#graph{height:100%; overflow:hidden;}
#graph svg{width:100%; height:100%;}
.sev-new_gap{color:var(--crit);} .sev-escalation{color:var(--warn);} .sev-evidence{color:var(--mut);}
circle{cursor:pointer;}
.node-label{fill:var(--mut); font-size:10px; pointer-events:none;}
.edge{stroke:var(--line); stroke-width:1;}
.edge.hot{stroke:var(--acc); stroke-width:2;}
text.legend-k{fill:var(--mut); font-size:11px;}
</style>
</head>
<body>
<header>
  <h1>SHIELD-AI Explorer</h1>
  <span class="meta" id="head-meta"></span>
</header>
<div id="wrap">
  <aside id="sidebar" class="panel">
    <h3>Explore</h3>
    <div class="inner">
      <input id="search" type="search" placeholder="Search incidents, controls, gaps&hellip;">
      <div class="facet-block">
        <label>Pillar (controls)</label>
        <div id="pillar-facets"></div>
      </div>
      <div class="facet-block">
        <label>Incident severity</label>
        <div id="sev-facets"></div>
      </div>
      <div class="facet-block">
        <label>People</label>
        <div id="result-list"></div>
      </div>
    </div>
  </aside>
  <section id="detail" class="panel">
    <h3>Detail</h3>
    <div class="inner" id="detail-body"><p style="color:var(--mut)">Select an
      incident, control, gap or exploit on the left, or click a node in the
      graph below.</p></div>
  </section>
  <section id="graph" class="panel">
    <h3>Graph (selected entity &amp; neighbours)</h3>
    <svg id="graph-svg" viewBox="0 0 900 420" preserveAspectRatio="xMidYMid
      meet"></svg>
  </section>
</div>
<script id="graph-data" type="application/json">{GRAPH_DATA}</script>
<script>
'use strict';
const DATA = JSON.parse(document.getElementById('graph-data').textContent);
const doc = (s)=>document.querySelector(s);
const byId = {};
DATA.controls.forEach(c=>byId[c.id]=c);
DATA.incidents.forEach(i=>byId[i.id]=i);
DATA.gaps.forEach(g=>byId[g.id]=g);
DATA.exploits.forEach(e=>byId[e.id]=e);
DATA.pillars.forEach(p=>byId[p.id]=p);

// meta in the header
const m = DATA.meta;
doc('#head-meta').textContent = `${m.control_count} controls \u00b7 ${m.incident_count} incidents \u00b7 ${m.pillar_count} pillars \u00b7 ${m.gap_count} gaps`;

const sevFacets = {'new_gap':'Critical/new','escalation':'Escalation','evidence':'Evidence'};
let ply = null, sev = null, q = '';
let selected = null; // node id of the selected entity

function redrawFacets(){
  // pillar checkboxes
  const pf = doc('#pillar-facets'); pf.innerHTML='';
  DATA.pillars.forEach(p=>{
    const n = p.controls.length;
    const d=document.createElement('div'); d.className='check';
    d.innerHTML=`<input type="checkbox" data-p="${p.id}"><span><b>${p.id}</b> &mdash; ${p.name} <span class="count">(${n})</span></span>`;
    d.querySelector('input').addEventListener('change',(e)=>{ markPillar(p.id,e.target.checked); });
    if(ply===p.id){ d.querySelector('input').checked=true; }
    pf.appendChild(d);
  });
  // severity checkboxes
  const sf = doc('#sev-facets'); sf.innerHTML='';
  Object.entries(sevFacets).forEach(([k,v])=>{
    const n = DATA.incidents.filter(i=>i.severity===k).length;
    const d=document.createElement('div'); d.className='check';
    d.innerHTML=`<input type="checkbox" data-s="${k}"><span>${v} <span class="count">(${n})</span></span>`;
    d.querySelector('input').addEventListener('change',(e)=>{ markSev(k,e.target.checked); });
    if(sev===k){ d.querySelector('input').checked=true; }
    sf.appendChild(d);
  });
}
function markPillar(p,on){ ply=on?p:null; applyFilter(); }
function markSev(s,on){ sev=on?s:null; applyFilter(); }

function matches(item,kind){
  const hay = `${item.id} ${item.title||''} ${kind} ${item.controls?item.controls.join(' '):''}`.toLowerCase();
  if(q && !hay.includes(q)) return false;
  if(kind==='control' && ply && item.pillar!==ply) return false;
  if(kind==='incident' && sev && item.severity!==sev) return false;
  return true;
}
function applyFilter(){
  const list = doc('#result-list'); list.innerHTML='';
  // group matches by type (controls, incidents, gaps)
  const show=(arr,kind,label)=>{
    const hits=arr.filter(i=>matches(i,kind));
    if(!hits.length) return;
    const h=document.createElement('h4'); h.style.cssText='color:var(--mut);font-size:12px;text-transform:uppercase;margin:10px 0 4px;';
    h.textContent=`${label} (${hits.length})`; list.appendChild(h);
    hits.forEach(it=>{
      const b=document.createElement('button'); b.className='result';
      b.dataset.id=it.id; b.dataset.type=kind;
      b.innerHTML=`<b>${it.id}</b> ${(it.title||'').substring(0,44)} <span class="n">${kind}</span>`;
      b.addEventListener('click',()=>select(it.id,kind));
      list.appendChild(b);
    });
  };
  show(DATA.controls,'control','Controls');
  show(DATA.incidents,'incident','Incidents');
  show(DATA.gaps,'gap','Gaps');
  show(DATA.exploits,'exploit','Exploits');
}
doc('#search').addEventListener('input',(e)=>{ q=e.target.value.toLowerCase().trim(); applyFilter(); });

const SEV_CLASS={new_gap:'sev-new_gap',escalation:'sev-escalation',evidence:'sev-evidence'};
function chip(id,kind){ return `<span class="chip" data-type="${kind}" data-id="${id}">${id}</span>`; }
function choose(sel){
  sel.addEventListener('click',(e)=>{
    const c=e.target.closest('.chip,.result');
    if(!c) return;
    e.stopPropagation();
    select(c.dataset.id,c.dataset.type);
  });
}

function select(id,kind){
  selected=id;
  const item=byId[id]||{}; const body=doc('#detail-body');
  let html='<h2>'+(item.title||id)+'</h2>';
  if(kind==='incident'){
    html+=`<div class="kv"><div><b>Severity</b><span class="${SEV_CLASS[item.severity]||''}">${item.severity}</span></div></div>`;
    html+='<div class="kv"><div><b>Controls</b></div></div><div>'+(item.controls||[]).map(c=>chip(c,'control')).join(' ')+'</div>';
    html+='<div class="kv" style="margin-top:10px"><div><b>Gaps</b></div></div><div>'+(item.gap_ids||[]).map(g=>chip(g,'gap')).join(' ')+'</div>';
  } else if(kind==='control'){
    const c=item;
    html+=`<div class="kv"><div><b>Pillar</b>${c.pillar}</div><div><b>Rego</b>${c.rego||'none'}</div></div>`;
    html+='<div class="kv"><div><b>Incidents</b></div></div><div>'+(((c.incidents||[]).map(i=>chip(i,'incident')).join(' '))||'(none)')+'</div>';
    if(c.description) html+=`<p>${c.description}</p>`;
  } else if(kind==='gap'){
    html+=`<div class="kv"><div><b>Severity</b>${item.severity}</div><div><b>Controls</b></div></div><div>${(((item.controls||[]).map(c=>chip(c,'control')).join(' '))||'(none)')}</div>`;
    html+='<div class="kv"><div><b>Incidents</b></div></div><div>'+(((item.incidents||[]).map(i=>chip(i,'incident')).join(' '))||'(none)')+'</div>';
  } else if(kind==='exploit'){
    html+=`<div class="kv"><div><b>Gap</b>${item.id}</div><div><b>File</b>${item.file||''}</div></div>`;
    html+='<div class="kv"><div><b>Controls</b></div></div><div>'+(((item.controls||[]).map(c=>chip(c,'control')).join(' '))||'(none)')+'</div>';
  } else if(kind==='pillar'){
    html+=`<div class="kv"><div><b>Controls (${item.controls.length})</b></div></div><div>`+item.controls.map(c=>chip(c,'control')).join(' ')+'</div>';
  }
  body.innerHTML=html;
  body.querySelectorAll('.chip').forEach(choose);
  drawGraph(id,kind);
}

function drawGraph(rootId,rootKind){
  const svg=doc('#graph-svg'); svg.innerHTML='';
  const NS='http://www.w3.org/2000/svg';
  const mk=(tag,attrs)=>{const el=document.createElementNS(NS,tag);for(const k in attrs)el.setAttribute(k,attrs[k]);return el;};
  // collect 1-hop neighbours from edges
  const nb=new Map(); const edgeSet=new Set();
  DATA.edges.forEach(e=>{
    if(e.from===rootId){ nb.set(e.to,{kind:kindOf(e.to),dir:1}); edgeSet.add(e.from+'->'+e.to); }
    else if(e.to===rootId){ nb.set(e.from,{kind:kindOf(e.from),dir:-1}); edgeSet.add(e.from+'->'+e.to); }
  });
  const kinds=[rootKind]; nb.forEach(v=>kinds.push(v.kind));
  const color={incident:'#e05a5a',control:'#5b9cf5',gap:'#e0a63c',exploit:'#9a6cf0',pillar:'#3dbb6a'};
  const seen=new Set([rootId]); const nodes=[[rootId,300,220,18]]; // center
  let i=0; let removed=new Set();
  nb.forEach((v,id)=>{
    if(removed.has(id))return;
    const ang=(i/Math.max(1,nb.size))*Math.PI*2 - Math.PI/2;
    const r=120; const x=300+Math.cos(ang)*r; const y=220+Math.sin(ang)*r;
    nodes.push([id,x,y,11]); i++;
  });
  // edges first (behind)
  nodes.forEach(n=>{
    if(n[0]===rootId)return;
    if(edgeSet.has(rootId+'->'+n[0])||edgeSet.has(n[0]+'->'+rootId)){
      const e=mk('line',{x1:300,y1:220,x2:n[1],y2:n[2],class:'edge',stroke:'#2a3a52','stroke-width':1});
      svg.appendChild(e);
    }
  });
  nodes.forEach(n=>{
    const id=n[0]; const k=n[3]?kindOf(id):rootKind;
    const c=mk('circle',{cx:n[1],cy:n[2],r:n[3],fill:color[k]||'#888','data-id':id,'data-type':k,'data-cx':n[1],'data-cy':n[2]});
    c.addEventListener('click',()=>{ if(id!==selected) select(id,kindOf(id)); });
    svg.appendChild(c);
    const t=mk('text',{x:n[1],y:n[2]+n[3]+12,class:'node-label','text-anchor':'middle'});
    t.textContent=id; svg.appendChild(t);
  });
  // legend
  let ly=20;
  Object.entries(color).forEach(([k,c])=>{ const n=DATA[k+'s']?DATA[k+'s'].length:0;
    const tb=mk('text',{x:880,y:ly,'text-anchor':'end'}); tb.textContent=`${k}:  `; tb.setAttribute('class','legend-k'); tb.setAttribute('fill',c); svg.appendChild(tb); ly+=18; });
}
function kindOf(id){
  if(id.indexOf('INC')===0)return 'incident';
  if(id.indexOf('G')===0 && id[1]>='0' && id[1]<='9')return 'gap';
  if(id.match(/^(MS|IAM|DS|TP|MIR|GRM|EE)-\d+$/))return 'control';
  return 'exploit';
}

// initial
redrawFacets(); applyFilter();
select('INC-01','incident');
</script>
</body>
</html>
"""


def build_html():
    with open(GRAPH, encoding="utf-8") as f:
        graph = json.load(f)
    # escape embedded JSON so it can never contain a literal </script>
    raw = json.dumps(graph, ensure_ascii=False, sort_keys=False)
    escaped = raw.replace("<", "\\u003c").replace(">", "\\u003e")
    return VIEWER.replace("{GRAPH_DATA}", escaped)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    blob = build_html()

    if args.stats:
        g = json.load(open(GRAPH, encoding="utf-8"))
        print(f"html=shield_ai_explorer.html graph_controls={g['meta']['control_count']} "
              f"graph_incidents={g['meta']['incident_count']} bytes={len(blob)}")
        return 0

    if args.check:
        if os.path.exists(OUT):
            cur = open(OUT, encoding="utf-8").read()
            if cur == blob:
                print("shield_ai_explorer.html fresh.")
                return 0
            print("STALE shield_ai_explorer.html -- run "
                  "python3 tools/generate_explorer_html.py --write",
                  file=sys.stderr)
            return 1
        print("MISSING shield_ai_explorer.html -- run --write", file=sys.stderr)
        return 1

    if args.write:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"wrote {OUT}")
        return 0

    sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())