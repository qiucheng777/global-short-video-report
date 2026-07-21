
async function loadData(){
  const res = await fetch('data/latest.json?ts=' + Date.now());
  if(!res.ok) throw new Error('数据文件读取失败');
  return res.json();
}
function esc(v=''){return String(v).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
function renderRows(items, target){
  const el=document.getElementById(target);
  el.innerHTML=items.map((x,i)=>`<tr data-search="${esc([x.platform,x.category,x.title,x.creator].join(' ').toLowerCase())}">
    <td><strong>${i+1}</strong></td>
    <td><span class="badge">${esc(x.platform)}</span></td>
    <td>${esc(x.category)}</td>
    <td><strong>${esc(x.title)}</strong><br><small>${esc(x.hook||'')}</small></td>
    <td>${esc(x.creator)}</td>
    <td>${esc(x.signal)}</td>
    <td>${esc(x.why)}</td>
    <td>${x.url?`<a class="link" target="_blank" rel="noopener" href="${esc(x.url)}">打开</a>`:'待核验'}</td>
  </tr>`).join('');
}
function setupSearch(inputId, tableId){
  document.getElementById(inputId).addEventListener('input',e=>{
    const q=e.target.value.trim().toLowerCase();
    document.querySelectorAll(`#${tableId} tr`).forEach(tr=>tr.style.display=tr.dataset.search.includes(q)?'':'none');
  });
}
function copyText(text,btn){
  navigator.clipboard.writeText(text).then(()=>{const old=btn.textContent;btn.textContent='已复制';setTimeout(()=>btn.textContent=old,1200)})
}
loadData().then(data=>{
  document.getElementById('updatedAt').textContent=`最近更新：${data.updated_at}（土耳其时间）`;
  document.getElementById('topCategory').textContent=data.kpis.top_category;
  document.getElementById('topCategoryNote').textContent=data.kpis.top_category_note;
  document.getElementById('crossPlatform').textContent=data.kpis.cross_platform;
  document.getElementById('focusPlatform').textContent=data.kpis.focus_platform;
  document.getElementById('dataStatus').textContent=data.kpis.data_status;
  document.getElementById('dailySummary').innerHTML=data.summary.map(x=>`<p>${esc(x)}</p>`).join('');
  renderRows(data.global_top10,'globalTable');
  renderRows(data.china_top10,'chinaTable');
  document.getElementById('ideasGrid').innerHTML=data.ideas.map((x,i)=>`<article class="idea">
    <span class="badge">选题 ${i+1}</span><h3>${esc(x.title)}</h3><p><strong>开头钩子：</strong>${esc(x.hook)}</p>
    <p>${esc(x.script)}</p><button class="copy-btn">复制文案</button></article>`).join('');
  document.querySelectorAll('.copy-btn').forEach((b,i)=>b.onclick=()=>copyText(data.ideas[i].script,b));
  document.getElementById('periodReports').innerHTML=Object.entries(data.period_reports).map(([k,v])=>`<article class="period"><h3>${esc(k)}</h3><p>${esc(v)}</p></article>`).join('');
  document.getElementById('archiveLinks').innerHTML=data.archive.map(x=>`<a href="${esc(x.url)}">${esc(x.label)}</a>`).join('');
  setupSearch('globalSearch','globalTable'); setupSearch('chinaSearch','chinaTable');
}).catch(err=>{
  document.getElementById('updatedAt').textContent=err.message;
});
