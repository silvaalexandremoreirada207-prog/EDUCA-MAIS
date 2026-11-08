/* Educa+ extras: toasts, XP, níveis, streak, conquistas, progresso, ordenação */
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function toast(msg,type='ok'){
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>toast(msg,type));return;}
  let box=document.getElementById('toasts');
  if(!box){box=document.createElement('div');box.id='toasts';box.className='fixed bottom-5 right-5 z-[100] space-y-2';document.body.appendChild(box);}
  const t=document.createElement('div');
  t.className='px-4 py-3 rounded-2xl shadow-2xl border-2 text-sm font-black max-w-xs '+(type==='xp'?'bg-yellow-400 text-blue-950 border-yellow-200':'bg-blue-950 text-white border-yellow-400');
  t.textContent=msg;box.appendChild(t);setTimeout(()=>t.remove(),3500);
}
/* ---- progresso por usuário ---- */
const BADGES=[
  {id:'start',ico:'fa-flag',name:'Primeiro Passo',desc:'Inicie 1 missão',ok:s=>s.started>=1},
  {id:'multi',ico:'fa-layer-group',name:'Multitarefa',desc:'Inicie 3 missões',ok:s=>s.started>=3},
  {id:'done',ico:'fa-trophy',name:'Chefão Derrotado',desc:'Conclua 1 missão',ok:s=>s.done>=1},
  {id:'fav',ico:'fa-bookmark',name:'Colecionador',desc:'Salve 3 favoritos',ok:s=>s.favs>=3},
  {id:'fire',ico:'fa-fire',name:'Em Chamas',desc:'Sequência de 3 dias',ok:s=>s.streak>=3},
  {id:'lvl3',ico:'fa-star',name:'Veterano',desc:'Chegue ao nível 3',ok:s=>s.level>=3},
];
function pKey(){const u=getCurrentUser();return u?'educa_plus_prog_'+u.email:null;}
function getProg(){const k=pKey();if(!k)return{courses:{},xp:0,streak:0,last:'',badges:[]};
  try{return JSON.parse(localStorage.getItem(k))||{courses:{},xp:0,streak:0,last:'',badges:[]};}catch{return{courses:{},xp:0,streak:0,last:'',badges:[]};}}
function saveProg(p){const k=pKey();if(k)localStorage.setItem(k,JSON.stringify(p));}
function levelOf(xp){return Math.floor(xp/200)+1;}
function stats(p){const c=Object.values(p.courses);return{started:c.length,done:c.filter(x=>x.done).length,favs:getFavorites().length,streak:p.streak,level:levelOf(p.xp)};}
function addXP(p,n,why){p.xp+=n;toast(`+${n} XP · ${why}`,'xp');}
function touchStreak(p){
  const today=new Date().toISOString().slice(0,10);if(p.last===today)return;
  const y=new Date(Date.now()-864e5).toISOString().slice(0,10);
  p.streak=p.last===y?p.streak+1:1;p.last=today;addXP(p,5,'sequência diária');
}
function checkBadges(p){const s=stats(p);BADGES.forEach(b=>{if(!p.badges.includes(b.id)&&b.ok(s)){p.badges.push(b.id);toast('🏆 Conquista: '+b.name,'xp');}});}
function requireLogin(){if(!getCurrentUser()){toast('Entre para registrar seu progresso!');openAuthModal('login');return false;}return true;}
function startCourse(id){
  if(!requireLogin())return;const p=getProg();
  if(!p.courses[id]){p.courses[id]={pct:0,done:false,note:''};addXP(p,10,'missão iniciada');}
  touchStreak(p);checkBadges(p);saveProg(p);openCourseModal(id);renderHUD();decorateCards();
}
function setPct(id,v){
  const p=getProg(),c=p.courses[id];if(!c)return;v=+v;
  const gain=Math.max(0,Math.floor((v-c.pct)/10)*2);c.pct=v;
  if(v>=100&&!c.done){c.done=true;addXP(p,100,'missão concluída!');}else if(gain)addXP(p,gain,'progresso');
  touchStreak(p);checkBadges(p);saveProg(p);renderHUD();decorateCards();
  const l=document.getElementById('pctLabel');if(l)l.textContent=v+'%';
}
function saveNote(id,v){const p=getProg();if(p.courses[id]){p.courses[id].note=v;saveProg(p);}}
/* ---- modal do curso com progresso e anotações ---- */
const _openCourseModal=openCourseModal;
openCourseModal=function(id){
  _openCourseModal(id);const c=getProg().courses[id];
  const box=document.querySelector('#modalContent .space-y-3');if(!box)return;
  const extra=document.createElement('div');extra.className='bg-blue-900 p-4 rounded-2xl border-2 border-blue-700 mb-4';
  extra.innerHTML=c?`<div class="flex justify-between text-xs font-black uppercase text-yellow-400 mb-2"><span>Seu progresso</span><span id="pctLabel">${c.pct}%</span></div>
    <input type="range" min="0" max="100" step="10" value="${c.pct}" oninput="setPct('${esc(id)}',this.value)" class="w-full accent-yellow-400">
    <textarea rows="2" placeholder="Anotações da missão..." onchange="saveNote('${esc(id)}',this.value)" class="mt-3 w-full bg-blue-950 border-2 border-blue-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-yellow-400">${esc(c.note)}</textarea>`
    :`<button onclick="startCourse('${esc(id)}')" class="w-full bg-white text-blue-950 font-black py-3 rounded-xl uppercase text-sm"><i class="fa-solid fa-flag mr-2"></i>Iniciar missão (+10 XP)</button>`;
  box.parentNode.insertBefore(extra,box);
};
/* ---- HUD no topo + ordenação + barras nos cards ---- */
function renderHUD(){
  const u=getCurrentUser();let h=document.getElementById('hud');
  if(!u){h&&h.remove();return;}
  const nav=document.querySelector('header .max-w-7xl');if(!nav)return;
  if(!h){h=document.createElement('a');h.id='hud';h.href=location.pathname.includes('professor')?'#':'/aluno/';
    h.className='hidden lg:flex items-center space-x-3 bg-blue-950 border-2 border-yellow-400/60 rounded-2xl px-3 py-1.5 text-xs font-black text-white';
    nav.insertBefore(h,nav.children[1]);}
  const p=getProg(),pct=(p.xp%200)/2;
  h.innerHTML=`<span class="text-yellow-400">NV ${levelOf(p.xp)}</span><span class="w-24 h-2 bg-blue-800 rounded-full overflow-hidden"><span class="block h-full bg-yellow-400" style="width:${pct}%"></span></span><span>${p.xp} XP</span><span class="text-orange-400"><i class="fa-solid fa-fire"></i> ${p.streak}</span>`;
}
function decorateCards(){
  const p=getProg();
  document.querySelectorAll('#coursesGrid button[onclick^="openCourseModal"]').forEach(b=>{
    const id=b.getAttribute('onclick').match(/'(.+?)'/)[1],c=p.courses[id];
    b.parentNode.querySelector('.pbar')?.remove();if(!c)return;
    const d=document.createElement('div');d.className='pbar mb-3';
    d.innerHTML=`<div class="h-2 bg-blue-950 rounded-full overflow-hidden"><div class="h-full ${c.done?'bg-emerald-400':'bg-yellow-400'}" style="width:${c.pct}%"></div></div><p class="text-[10px] font-black uppercase text-blue-200 mt-1">${c.done?'✔ Concluída':c.pct+'% completo'}</p>`;
    b.parentNode.insertBefore(d,b);
    b.querySelector('span').textContent=c.done?'Revisar missão':'Continuar missão';
  });
}
const _getStored=getStoredCourses;
getStoredCourses=function(){
  const list=_getStored().slice(),s=document.getElementById('sortSelect');if(!s)return list;
  const lv={Iniciante:0,'Intermediário':1,'Avançado':2};
  if(s.value==='rating')list.sort((a,b)=>(b.rating||0)-(a.rating||0));
  if(s.value==='level')list.sort((a,b)=>lv[a.level]-lv[b.level]);
  if(s.value==='az')list.sort((a,b)=>a.title.localeCompare(b.title,'pt'));
  return list;
};
const _render=renderStudentCourses;
renderStudentCourses=function(){_render();decorateCards();};
function surprise(){const l=_getStored();openCourseModal(l[Math.floor(Math.random()*l.length)].id);}
document.addEventListener('DOMContentLoaded',()=>{
  const q=JSON.parse(sessionStorage.getItem('toastq')||'[]');sessionStorage.removeItem('toastq');q.forEach(m=>toast(m));
  renderHUD();
  const cat=document.getElementById('categoryFilter');
  if(cat){
    const s=document.createElement('select');s.id='sortSelect';s.className=cat.className;
    s.innerHTML='<option value="">Ordem padrão</option><option value="rating">Melhor avaliados</option><option value="level">Menor dificuldade</option><option value="az">A → Z</option>';
    s.addEventListener('change',renderStudentCourses);cat.parentNode.appendChild(s);
    const r=document.createElement('button');r.type='button';r.title='Missão surpresa';r.onclick=surprise;
    r.className='bg-white text-blue-950 px-4 py-3 rounded-2xl font-black text-xs uppercase shadow';r.innerHTML='<i class="fa-solid fa-dice mr-1"></i>Surpresa';
    cat.parentNode.appendChild(r);
    // layout: busca em linha própria; filtros e botão dividem a linha de baixo
    const bar=cat.parentNode;bar.classList.add('flex-wrap');bar.classList.replace('max-w-3xl','max-w-4xl');
    bar.firstElementChild.classList.add('basis-full');
    bar.querySelectorAll('select').forEach(x=>x.classList.add('flex-1','min-w-[10rem]'));
    r.classList.add('whitespace-nowrap');
    renderStudentCourses();
  }
});
