
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
async function main(){const r=await fetch('data/latest.json?'+Date.now());if(!r.ok)throw new Error('数据读取失败');const d=await r.json();
updated.textContent='最近更新：'+d.updated_at+'（土耳其时间）';k1.textContent=d.kpis.top_category;k1n.textContent=d.kpis.top_category_note;k2.textContent=d.kpis.focus_platform;k3.textContent=d.kpis.data_status;k4.textContent=d.kpis.high_potential||'3';
summaryText.innerHTML=d.summary.map(x=>`<p>${esc(x)}</p>`).join('');
function rows(arr,id){document.getElementById(id).innerHTML=arr.map((x,i)=>`<tr data-s="${esc([x.platform,x.category,x.title,x.source].join(' ').toLowerCase())}">
<td><b>${i+1}</b></td><td>${x.thumbnail?`<img class="thumb" src="${esc(x.thumbnail)}" alt="">`:'—'}</td>
<td><span class="badge">${esc(x.platform)}</span></td><td>${esc(x.category)}</td><td><b>${esc(x.title)}</b><br><small>${esc(x.hook)}</small></td>
<td>${esc(x.source)}</td><td>${esc(x.signal)}</td><td>${esc(x.why)}</td><td>${x.url?`<a class="link" target="_blank" rel="noopener" href="${esc(x.url)}">打开</a>`:'待核验'}</td></tr>`).join('')}
rows(d.global_top10,'gt');rows(d.china_top10,'ct');
function filter(inp,tbody){document.getElementById(inp).oninput=e=>document.querySelectorAll('#'+tbody+' tr').forEach(tr=>tr.style.display=tr.dataset.s.includes(e.target.value.toLowerCase())?'':'none')}filter('qg','gt');filter('qc','ct');
ideasGrid.innerHTML=(d.ideas||[]).map((x,i)=>`<article class="idea"><span class="badge">脚本 ${i+1}</span><h3>${esc(x.title)}</h3><p><b>3秒钩子：</b>${esc(x.hook)}</p><p>${esc(x.script)}</p><p><b>标题：</b>${esc(x.caption||'')}</p><p><b>标签：</b>${esc(x.tags||'')}</p><button data-i="${i}">复制完整脚本</button></article>`).join('');
ideasGrid.querySelectorAll('button').forEach(b=>b.onclick=()=>navigator.clipboard.writeText([d.ideas[+b.dataset.i].title,d.ideas[+b.dataset.i].hook,d.ideas[+b.dataset.i].script,d.ideas[+b.dataset.i].caption,d.ideas[+b.dataset.i].tags].join('\\n')).then(()=>{b.textContent='已复制';setTimeout(()=>b.textContent='复制完整脚本',1200)}));
competitorGrid.innerHTML=(d.competitors||[]).map(x=>`<article class="period"><h3>${esc(x.name)}</h3><p>${esc(x.status)}</p><p><b>下一步：</b>${esc(x.action)}</p></article>`).join('');
periodGrid.innerHTML=Object.entries(d.period_reports||{}).map(([k,v])=>`<article class="period"><h3>${esc(k)}</h3><p>${esc(v)}</p></article>`).join('');
taskGrid.innerHTML=(d.tasks||[]).map((x,i)=>`<article class="task"><div class="score">${i+1}</div><b>${esc(x.title)}</b><span>${esc(x.detail)}</span></article>`).join('');
archives.innerHTML=(d.archive||[]).map(x=>`<a href="${esc(x.url)}">${esc(x.label)}</a>`).join('');
const all=[...d.global_top10,...d.china_top10],cats={},plats={};all.forEach(x=>{cats[x.category]=(cats[x.category]||0)+1;plats[x.platform]=(plats[x.platform]||0)+1});
new Chart(catChart,{type:'bar',data:{labels:Object.keys(cats),datasets:[{label:'入榜次数',data:Object.values(cats)}]},options:{responsive:true,plugins:{legend:{labels:{color:'#eef6ff'}}},scales:{x:{ticks:{color:'#9fb3c8'}},y:{ticks:{color:'#9fb3c8'},beginAtZero:true}}}});
new Chart(platformChart,{type:'doughnut',data:{labels:Object.keys(plats),datasets:[{data:Object.values(plats)}]},options:{responsive:true,plugins:{legend:{labels:{color:'#eef6ff'}}}}});
}main().catch(e=>updated.textContent='读取失败：'+e.message);
