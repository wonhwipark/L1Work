/* CoWork B-style PUBLIC UI: only pre-approved status.json and handoffs.json, same origin. */
(() => {
 'use strict';
 const CATS = Object.freeze({
   'review-watcher':'협업 운송 전환',
   'dashboard':'CoWork 대시보드',
   'skill-discovery':'스킬 발견·재사용',
   'job-list':'업무 자동화 후보',
   'knowledge-design':'지식 구조 설계'
 });
 const LANES = [
   {name:'상태 확인', match:n=>n===0},
   {name:'개발·시험 기록',match:n=>n===1||n===2},
   {name:'리뷰·검토 기록',match:n=>n===3},
   {name:'판정·후속 기록',match:n=>n===4||n===5}
 ];
 const STEPS = [
  [
   "사용자 요청",
   "업무 GPT · 모바일 Agent",
   "업무 목표·범위를 접수하고 입력 소스·승인 범위를 확인"
  ],
  [
   "Workflow",
   "요청 분류 · 기존 Work 검색·재개",
   "같은 목적의 기존 Work를 우선 재개하고 필요한 작업만 연결"
  ],
  [
   "Kernel",
   "Work ID · Source Revision 관리",
   "원본 revision과 근거·상태 연결을 고정. 문서 등록 자체가 호스트 실행은 아님"
  ],
  [
   "code-analyzer / issue-analyzer",
   "코드 분석 · 이슈 사실 구분",
   "코드 사실과 설계 가정·미확인을 구분해 근거 생성"
  ],
  [
   "doc-converter / hld-composer",
   "코드 분석 · HLD · MSC HTML",
   "허용된 근거를 문서·HLD·MSC HTML로 구성. 실제 내용 검증은 별도"
  ],
  [
   "l1-workspace",
   "분석 결과 · 결정 · Evidence 보존",
   "해당 업무 Work에 원본, 분석 결과, 판정, Evidence, 미해결 항목을 보존"
  ],
  [
   "l1-knowledge-updater",
   "지식 후보 작성",
   "확인된 분석 근거에서 지식 후보를 만들고 기존 writer와 연결"
  ],
  [
   "Module → Feature → Scenario",
   "중복·충돌 대조 · Preview",
   "기존 기술 지식과 비교하고 AS-IS/TO-BE·분류 적합성 및 Preview 검토"
  ],
  [
   "근거 검증 및 게시 판정",
   "승인 / 보완 필요 / 개인 유지",
   "보완은 같은 Work로 돌아가 근거 보충, 개인 유지는 후보 보존, 승인은 게시 진행"
  ],
  [
   "l1sw-dev-knowledge",
   "검증된 기술 지식 게시",
   "유효한 게시 승인과 권한을 확인한 경우에만 그룹 기술 지식 정본에 게시"
  ],
  [
   "게시 revision · 원격 readback",
   "게시 결과를 실제 바이트로 검증",
   "게시된 revision과 원격 본문을 재조회하여 일치 여부 확인"
  ],
  [
   "원래 Work 역링크",
   "지식 게시 결과 연결",
   "원래 업무 Work에 지식 revision·판정·근거의 역링크 기록"
  ],
  [
   "검색 / RAG / 후속 분석 재사용",
   "재사용 실증은 별도",
   "검증된 지식을 탐색·재사용하는 후속 단계. 실제 RAG 호출 성공은 별도로 시험"
  ]
 ];
 const L1_LANES = [
  {
   "id": "request",
   "name": "요청·재개",
   "range": [
    1,
    2,
    3
   ],
   "detail": "사용자 요청 → Workflow → Kernel"
  },
  {
   "id": "analysis",
   "name": "분석·문서화",
   "range": [
    4,
    5
   ],
   "detail": "분석 스킬 → 문서·HLD·MSC"
  },
  {
   "id": "evidence",
   "name": "Work·Evidence",
   "range": [
    6
   ],
   "detail": "업무 결과·판정·Evidence 보존"
  },
  {
   "id": "knowledge",
   "name": "지식 후보·검증",
   "range": [
    7,
    8,
    9
   ],
   "detail": "후보 작성 → 기존 지식 대조 → 게시 판정"
  },
  {
   "id": "publish",
   "name": "게시·재사용",
   "range": [
    10,
    11,
    12,
    13
   ],
   "detail": "그룹 게시 → readback → 역링크 → 재사용"
  }
 ];
 let cards=[], pub=null, mode='board', filter='', focused=null, latestHistory=[];
 const $=id=>document.getElementById(id);
 const el=(type,cls,content)=>{const n=document.createElement(type); if(cls)n.className=cls; if(content!==undefined)n.textContent=String(content);return n};
 const str=(s,max=165)=>typeof s==='string'&&s.length<=max&&!/[<>]/.test(s);
 const validStamp=d=>{const t=Date.parse(d);return Number.isFinite(t)&&t<=Date.now()+3600000};
 const hashTab=()=>['collab','l1','todo'].includes(location.hash.slice(1))?location.hash.slice(1):'collab';
 const phase=c=>Number.isInteger(c.phase_index)?c.phase_index:0;
 function valid(j){
   if(!j||j.schema!=='COWORK_PUBLIC_STATUS_V1'||!Array.isArray(j.work_cards)||j.work_cards.length>5||!j.counts||typeof j.counts!=='object'||!str(j.generated_at,40)||!validStamp(j.generated_at))return false;
   const provider=j.checks&&j.checks.active_provider;
   const live=(j.cutover==='GitHub LIVE (호스트 보고 수용)'&&provider==='GitHub 리뷰 운송 LIVE (호스트 보고 수용)');
   const legacy=(j.cutover==='정식 전환 전'&&['활성 리뷰 제공자 없음','Dropbox 리뷰 제공자 (문서 기록)','기록 미확인'].includes(provider));
   if(!live&&!legacy)return false;
   const seen=new Set();
   return j.work_cards.every(c=>c&&Object.hasOwn(CATS,c.category)&&!seen.has(c.category)&&seen.add(c.category)&&c.title===CATS[c.category]&&Number.isInteger(c.phase_index)&&c.phase_index>=0&&c.phase_index<=5&&['title','owner','phase_label','test_label','review_label','next_action'].every(k=>str(c[k],180)));
 }
 function setTab(tab){
   for(const t of document.querySelectorAll('[data-tab]'))t.setAttribute('aria-selected',String(t.dataset.tab===tab));
   for(const p of document.querySelectorAll('section.panel'))p.classList.toggle('active',p.id===tab);
   if(tab==='collab')$('search').focus({preventScroll:true});
 }
 function stamp(){
   $('asof').textContent=pub&&pub.generated_at?'공개 정보 마지막 변경 · '+new Date(pub.generated_at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'}):'공개 상태 확인 필요';
   $('alert').textContent=pub
     ? '공개 운영 상태: '+pub.cutover+' · 이 표시는 호스트 보고 및 GPT 판정 수용 범위입니다. 변경 시각은 원본 최종 검증 시각이 아니며 무변경 자체는 갱신 실패를 뜻하지 않습니다. 개별 리뷰·지식 게시 완료는 별도 근거가 필요합니다.'
     : '공개 상태 JSON 수신·검증 실패로 현재 운영 상태 판단을 보류합니다. PRIVATE 정본과 실제 실행 근거를 확인해야 합니다.';
 }
 function kpis(){const c=pub?.counts||{}; for(const [id,key] of [['kReq','requests'],['kRev','reviews'],['kRec','receipts']])$(id).textContent=Number.isSafeInteger(c[key])&&c[key]>=0?String(c[key]):'—';$('kWork').textContent=String(cards.length)}
 function txtBlock(c){let p=el('p','',c.next_action||'다음 행동 확인 필요');return p}
 function card(c){let b=el('button','item');b.type='button';b.dataset.category=c.category;b.append(el('strong','',c.title),el('span','mini',c.phase_label),txtBlock(c));b.addEventListener('click',()=>open(c));return b}
 function match(c){const a=(c.title+' '+c.owner+' '+c.phase_label+' '+c.next_action).toLowerCase();return a.includes(filter.toLowerCase())}
 function renderWork(){const visible=cards.filter(match),v=$('workview');v.replaceChildren(); if(mode==='board'){
   const b=el('div','board');for(const lane of LANES){const list=visible.filter(c=>lane.match(phase(c)));const g=el('section','lane');const head=el('h3','',lane.name);head.append(el('em','',list.length));g.append(head);list.forEach(c=>g.append(card(c)));b.append(g)}v.append(b);
 }else{const w=el('div','tablewrap'),t=el('table'),th=el('tr');['업무','기록된 단계','담당','다음 행동'].forEach(s=>th.append(el('th','',s)));t.append(el('thead',''));t.tHead.append(th);const body=el('tbody');for(const c of visible){const tr=el('tr');for(const a of [c.title,c.phase_label,c.owner,c.next_action]){const td=el('td','');if(a===c.title){let b=el('button','',a);b.style.cssText='background:none;border:0;color:#285cb6;text-align:left;padding:0;font-weight:750';b.addEventListener('click',()=>open(c));td.append(b)}else td.textContent=a;tr.append(td)}body.append(tr)}t.append(body);w.append(t);v.append(w)}if(!visible.length)v.append(el('p','note','조건에 해당하는 공개 업무 없음'))}
 function renderTodo(){const p=$('todolist');p.replaceChildren();cards.forEach(c=>{const b=card(c);b.classList.add('todoitem');p.append(b)});if(!cards.length)p.append(el('p','note','허용된 최신 업무 정보 없음'))}
 function open(c){focused=document.activeElement;$('detail').replaceChildren(el('span','mini',c.phase_label),el('h2','',c.title),el('p','', '담당: '+c.owner),el('h3','','기록된 자체시험'),el('p','',c.test_label),el('h3','','기록된 독립 리뷰'),el('p','',c.review_label),el('h3','','다음 행동'),el('p','',c.next_action),el('p','source','공개 상태 스냅샷 기준. 최신 원본 정합성·실행 증거는 별도 검증'));$('veil').classList.add('show');$('drawer').classList.add('show');$('drawer').setAttribute('aria-hidden','false');$('close').focus()}
 function close(){if(!$('drawer').classList.contains('show'))return;$('veil').classList.remove('show');$('drawer').classList.remove('show');$('drawer').setAttribute('aria-hidden','true');if(focused)focused.focus()}
 function renderSteps(){
   const map=$('l1map')||$('l1steps');
   if(!map)return;
   map.replaceChildren();
   L1_LANES.forEach((lane,li)=>{
     const wrap=el('section','l1-lane l1-lane--'+lane.id);
     wrap.setAttribute('aria-label',String(li+1)+'단계 '+lane.name);
     const h=el('div','l1-lane-label');
     h.append(el('span','l1-lane-order','0'+(li+1)),el('strong','',lane.name),el('small','',lane.detail));
     const right=el('div','l1-lane-right'),route=el('div','l1-route');
     lane.range.forEach((num,index)=>{
       if(index)route.append(el('span','l1-route-arrow','→'));
       const btn=el('button','l1-node'+(num===9?' l1-node--decision':''));
       btn.type='button';btn.dataset.l1Step=String(num);
       btn.setAttribute('aria-pressed','false');
       btn.setAttribute('aria-label',num+'단계 '+STEPS[num-1][0]+' 자세히 보기');
       btn.append(el('span','l1-node-num',String(num)),el('strong','',STEPS[num-1][0]),el('small','',STEPS[num-1][1]));
       btn.addEventListener('click',()=>selectStep(num-1));
       route.append(btn);
     });
     right.append(route);
     if(lane.id==='analysis'){
       right.append(el('p','note','③ Kernel의 Source Revision도 ⑤ 문서화 입력으로 연결됩니다. ④ 코드 분석 근거와 함께 사용합니다.'));
     }
     if(lane.id==='knowledge'){
       const branches=el('div','l1-branches');
       for(const [name,note,kind,step] of [
         ['보완 필요 ↩','같은 Work에서 근거 보완 → ⑤ 문서·MSC 단계','rework',4],
         ['개인 유지 ↗','개인 Work에 지식 후보 보존','hold',8],
         ['승인 ↓','⑩ 그룹 기술 지식 게시 단계로 진행','approve',9]
       ]){
         const btn=el('button','l1-branch l1-branch--'+kind);
         btn.type='button';btn.append(el('strong','',name),el('small','',note));
         btn.addEventListener('click',()=>{
           selectStep(step);
           if(kind==='hold')$('l1detail').append(el('p','note','개인 유지 분기: 현재 Work에 후보를 보존하며 그룹 지식에 게시하지 않습니다.'));
         });
         branches.append(btn);
       }
       right.append(branches);
     }
     wrap.append(h,right);map.append(wrap);
     if(li<L1_LANES.length-1){const down=el('div','l1-down','↓');down.setAttribute('aria-hidden','true');map.append(down)}
   });
   map.append(el('p','l1-feedback','↶ ⑬ 검색·RAG·후속 분석 결과는 새로운 요청 또는 같은 목적의 기존 Work 재개(①~②)로 연결'));
   selectStep(0);
 }
 function selectStep(i){
   if(!Number.isInteger(i)||i<0||i>=STEPS.length)return;
   const map=$('l1map')||$('l1steps');
   if(!map)return;
   for(const b of map.querySelectorAll('[data-l1-step]'))b.setAttribute('aria-pressed',String(Number(b.dataset.l1Step)===i+1));
   $('l1detail').replaceChildren(
     el('span','mini','STEP '+(i+1)+' / 13 · 설계 책임'),
     el('h3','',STEPS[i][0]),el('p','',STEPS[i][2]),
     el('p','note','이 연결은 설계상의 책임·데이터 이동 경로입니다. 자동 스킬 호출, Knowledge 게시 및 검색·RAG 실사용 성공을 의미하지 않습니다.')
   );
 }
 function validateHistory(h){if(!h||h.schema!=='L1WORK_HANDOFF_HISTORY_V1'||!Array.isArray(h.entries)||h.entries.length>3)return false;const seen=new Set();return h.entries.every(e=>e&&typeof e.filename==='string'&&/^[A-Za-z0-9][A-Za-z0-9_.-]{0,179}\.md$/.test(e.filename)&&e.filename.toUpperCase().includes('HANDOFF')&&!seen.has(e.filename)&&seen.add(e.filename)&&str(e.title,130)&&/^20\d\d-\d\d-\d\d$/.test(e.published_on))}
 function renderHistory(){const box=$('handoffs');box.replaceChildren();if(!latestHistory.length){box.append(el('p','note','허용된 공개 인계 문서 이력이 없거나 현재 확인되지 않았습니다.'));return}for(const h of latestHistory){const a=el('article');a.append(el('span','',h.published_on),el('b','',h.title));const link=el('a','', 'PUBLIC 원문 열기');link.target='_blank';link.rel='noopener noreferrer';link.href='https://github.com/wonhwipark/L1Work/blob/main/handoffs/'+encodeURIComponent(h.filename);a.append(link);box.append(a)}}
 async function update(){try{const r=await fetch('status.json',{cache:'no-store'});if(!r.ok)throw Error('status '+r.status);const j=await r.json();if(!valid(j))throw Error('public schema');pub=j;cards=j.work_cards;stamp();kpis();renderWork();renderTodo()}catch(e){pub=null;cards=[];stamp();kpis();renderWork();renderTodo()}}
 async function updateHistory(){try{const r=await fetch('handoffs.json',{cache:'no-store'});if(!r.ok)throw Error('history '+r.status);const j=await r.json();latestHistory=validateHistory(j)?j.entries:[]}catch(e){latestHistory=[]}renderHistory()}
 document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{location.hash=b.dataset.tab;setTab(b.dataset.tab)}));window.addEventListener('hashchange',()=>setTab(hashTab()));
 document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.view;document.querySelectorAll('[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));renderWork()}));
 $('search').addEventListener('input',e=>{filter=e.target.value;renderWork()});$('close').addEventListener('click',close);$('veil').addEventListener('click',close);document.addEventListener('keydown',e=>{if(e.key==='Escape')close();if(e.key==='Tab'&&$('drawer').classList.contains('show')){const f=$('drawer').querySelectorAll('button,a,input');if(f.length===1){e.preventDefault();f[0].focus()}}});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden){update();updateHistory()}});window.addEventListener('focus',()=>{update();updateHistory()});setTab(hashTab());renderSteps();stamp();update();updateHistory();setInterval(()=>{update();updateHistory()},120000);
})();
