
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
async function main(){const r=await fetch('data/latest.json?'+Date.now());if(!r.ok)throw new Error('数据读取失败');const d=await r.json();
updated.textContent='最近更新：'+d.updated_at+'（土耳其时间）';k1.textContent=d.kpis.top_category;k1n.textContent=d.kpis.top_category_note;k2.textContent=d.kpis.focus_platform;k3.textContent=d.kpis.data_status;
summaryText.innerHTML=d.summary.map(x=>`<p>${esc(x)}</p>`).join('');
function rows(arr,id){document.getElementById(id).innerHTML=arr.map((x,i)=>`<tr data-s="${esc([x.platform,x.category,x.title,x.source].join(' ').toLowerCase())}">
<td><b>${i+1}</b></td><td>${x.thumbnail?`<img class="thumb" src="${esc(x.thumbnail)}" alt="">`:'—'}</td>
<td><span class="badge">${esc(x.platform)}</span></td><td>${esc(x.category)}</td><td><b>${esc(x.title)}</b><br><small>${esc(x.hook)}</small></td>
<td>${esc(x.source)}</td><td>${esc(x.signal)}</td><td>${esc(x.why)}</td><td>${x.url?`<a class="link" target="_blank" rel="noopener" href="${esc(x.url)}">打开</a>`:'待核验'}</td></tr>`).join('')}
rows(d.global_top10,'gt');rows(d.china_top10,'ct');
function filter(inp,tbody){document.getElementById(inp).oninput=e=>document.querySelectorAll('#'+tbody+' tr').forEach(tr=>tr.style.display=tr.dataset.s.includes(e.target.value.toLowerCase())?'':'none')}filter('qg','gt');filter('qc','ct');
ideasGrid.innerHTML=d.ideas.map((x,i)=>`<article class="idea"><span class="badge">选题 ${i+1}</span><h3>${esc(x.title)}</h3><p><b>开头：</b>${esc(x.hook)}</p><p>${esc(x.script)}</p><button data-i="${i}">复制文案</button></article>`).join('');
ideasGrid.querySelectorAll('button').forEach(b=>b.onclick=()=>navigator.clipboard.writeText(d.ideas[+b.dataset.i].script).then(()=>{b.textContent='已复制';setTimeout(()=>b.textContent='复制文案',1200)}));
periodGrid.innerHTML=Object.entries(d.period_reports||{}).map(([k,v])=>`<article class="period"><h3>${esc(k)}</h3><p>${esc(v)}</p></article>`).join('');
archives.innerHTML=d.archive.map(x=>`<a href="${esc(x.url)}">${esc(x.label)}</a>`).join('');
const all=[...d.global_top10,...d.china_top10],cats={},plats={};all.forEach(x=>{cats[x.category]=(cats[x.category]||0)+1;plats[x.platform]=(plats[x.platform]||0)+1});
new Chart(catChart,{type:'bar',data:{labels:Object.keys(cats),datasets:[{label:'入榜次数',data:Object.values(cats)}]},options:{responsive:true,plugins:{legend:{labels:{color:'#eef6ff'}}},scales:{x:{ticks:{color:'#9fb3c8'}},y:{ticks:{color:'#9fb3c8'},beginAtZero:true}}}});
new Chart(platformChart,{type:'doughnut',data:{labels:Object.keys(plats),datasets:[{data:Object.values(plats)}]},options:{responsive:true,plugins:{legend:{labels:{color:'#eef6ff'}}}}});
}main().catch(e=>updated.textContent='读取失败：'+e.message);
