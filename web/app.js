const realms = ["凡骨", "启灵", "纳气", "筑台", "金丹", "元婴", "化神", "洞虚", "合道", "问鼎", "渡劫", "飞升"];
const factions = ["太玄宗","归墟宫","无量书院","星河盟","苍梧城","玉京阁","扶摇剑庐","九曜天府","玄霜门","赤明观","寒渊楼","青冥山庄","烛龙殿","云梦泽","天机阁","墨麟会","长生台","逐鹿城","听雪楼","万象府"];
const chapters = [
  ["第1章 · 天书残页现世", "太玄界的雨下了三日，像有人在天上洗去旧字。倪扶光在废弃藏书阁中捡到一页烧不尽的金纸，纸上只写着一句话：凡被写入者，命运会沿文字生长。"],
  ["第2章 · 主角被宗门除名", "归墟宫的钟声响过七次，宗门命册上倪扶光的名字被朱笔划去。可所有人都没有发现，被删去的名字正在另一卷天书上重新浮现。"],
  ["第3章 · 旧城秘境开启", "苍梧旧城在月色里露出城门，墙上爬满会呼吸的墨痕。江听雪说，这不是秘境，而是一段被封存的历史。"],
  ["第4章 · 敌对势力围猎", "三十六道剑光封住山路，九曜天府的密探从雾中走出。他们并不想杀人，只想确认主角是否已经成为天书的新主人。"],
  ["第5章 · 战力体系反转", "筑台并非金丹之前的低阶境界，而是所有修行者被人为压低的天花板。真正的修炼，从敢于质疑境界名开始。"],
  ["第6章 · 命盘被人篡改", "人物谱系中多出一个不存在的名字，所有角色都记得他来过，只有他自己不知道是谁把他写进了故事。"],
  ["第7章 · 卧底进入敌宗", "为了找到被藏起的第十三阶境界，倪扶光披上敌宗外门弟子的灰袍，第一次亲手擦掉了自己的来处。"],
  ["第8章 · 飞升真相揭露", "所谓飞升不是离开凡界，而是被天书送进下一卷故事。每一次圆满结局，都是另一个世界的开篇。"]
];
const checks = [
  ["战力一致", "未发现越级崩坏", "通过"],
  ["时间线", "章节 1-8 昼夜顺序稳定", "通过"],
  ["伏笔", "天书残页将在第 12 章回收", "待追踪"],
  ["人物动机", "江听雪隐藏立场需要补强", "建议"]
];
function $(id){return document.getElementById(id)}
function showToast(text="灵感汇聚中…"){const t=$("toast");t.textContent=text;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2200)}
function initReveal(){const io=new IntersectionObserver((entries)=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("visible")})},{threshold:.12});document.querySelectorAll(".reveal").forEach(el=>io.observe(el))}
function initTheme(){const b=$("themeToggle");b.onclick=()=>{document.documentElement.dataset.theme=document.documentElement.dataset.theme==="paper"?"":"paper";showToast(document.documentElement.dataset.theme==="paper"?"纸上显形":"夜幕请笔")}}
function initDestiny(){const map=$("destinyMap");const nodes=[
  ["太玄界",50,43,"core"],["倪扶光",22,24,""],["江听雪",72,26,""],["天书残页",47,12,""],["归墟宫",18,67,""],["九曜天府",76,67,""],["旧城秘境",50,74,""],["第17章",38,55,""],["反派旧神",62,54,""]
];
const lines=`<svg><defs><linearGradient id="g"><stop stop-color="#d6b56d"/><stop offset="1" stop-color="#5cd7ff"/></linearGradient></defs>${nodes.slice(1).map(n=>`<line x1="50%" y1="43%" x2="${n[1]}%" y2="${n[2]}%" stroke="url(#g)" stroke-width="1" opacity=".35"><animate attributeName="opacity" values=".15;.55;.15" dur="3s" repeatCount="indefinite"/></line>`).join("")}</svg>`;
map.innerHTML=lines+nodes.map(n=>`<div class="node ${n[3]}" style="left:calc(${n[1]}% - ${n[3]==='core'?65:45}px);top:calc(${n[2]}% - ${n[3]==='core'?65:45}px)">${n[0]}</div>`).join("");}
function initAudit(){const list=$("auditList");list.innerHTML=checks.map(c=>`<li><span>${c[0]}</span><b>${c[2]}</b></li>`).join("");$("checkWall").innerHTML=checks.map(c=>`<div class="check-item"><strong>${c[0]}</strong><span>${c[1]}</span></div>`).join("")}
function initWorld(){const spiral=$("realmSpiral");spiral.innerHTML=realms.map((r,i)=>`<div class="realm-step" style="--i:${i%6}">${String(i+1).padStart(2,"0")} · ${r}</div>`).join("");const tiles=["山","泽","城","宗","林","荒","海","塔","关","殿","原","岭","书","月"];$("asciiMap").innerHTML=Array.from({length:126},(_,i)=>`<div class="tile">${tiles[(i*7+i%5)%tiles.length]}</div>`).join("")}
function initGalaxy(){const g=$("galaxy");g.innerHTML=factions.map((f,i)=>{const x=8+(i*37)%84;const y=12+(i*53)%76;return `<span class="star" data-name="${f}" style="left:${x}%;top:${y}%;animation:float ${4+i%5}s ease-in-out infinite ${i*.08}s"></span>`}).join("")}
function initChapters(){const list=$("chapterList");list.innerHTML=chapters.map((c,i)=>`<button class="chapter-btn ${i===0?'active':''}" data-index="${i}">${c[0]}</button>`).join("");list.onclick=e=>{const btn=e.target.closest("button");if(!btn)return;document.querySelectorAll(".chapter-btn").forEach(b=>b.classList.remove("active"));btn.classList.add("active");const c=chapters[Number(btn.dataset.index)];$("chapterTitle").textContent=c[0];$("chapterBody").textContent=c[1]+" 这一章将维持约 3500 中文字符的生成目标，并把人物境界、势力关系和伏笔状态写回命盘。";showToast("章节已在命盘中展开")};$("chapterBody").textContent=chapters[0][1]+" 这一章将维持约 3500 中文字符的生成目标，并把人物境界、势力关系和伏笔状态写回命盘。"}
function initInteractions(){document.querySelectorAll(".rail-item").forEach(btn=>btn.onclick=()=>{document.querySelectorAll(".rail-item").forEach(b=>b.classList.remove("active"));btn.classList.add("active");showToast(`已切换至「${btn.textContent}」`) });$("summonBtn").onclick=()=>showToast("请笔中：正在生成 3500 字章节…");$("applyDirection").onclick=()=>showToast("方向修正已写入第 17 章命盘");$("fileInput").onchange=e=>{const f=e.target.files[0];if(!f)return;$("uploadText").textContent=`已采样：${f.name}`;showToast("风格正在采样，叙事纹理已记录")}}
initReveal();initTheme();initDestiny();initAudit();initWorld();initGalaxy();initChapters();initInteractions();
