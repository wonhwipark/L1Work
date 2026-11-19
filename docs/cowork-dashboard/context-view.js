/* P1/P2 CoWork public context view.
 * Render ONLY previously approved same-origin status.json fields and fixed labels.
 * Never read PRIVATE GitHub sources, infer execution evidence, or persist history.
 */
(() => {
 'use strict';
 const FIELDS = Object.freeze([
  {id:'review-watcher',title:'협업·리뷰',hint:'실제 리뷰와 호스트 운영 상태는 별도 근거로 확인'},
  {id:'skill-discovery',title:'스킬·배포',hint:'개발·PUBLIC 게시·업무 설치는 서로 다른 단계'},
  {id:'job-list',title:'업무 실행',hint:'Job 기록이 코드 분석 완료를 증명하지 않음'},
  {id:'knowledge-design',title:'L1 지식',hint:'지식 후보와 그룹 게시·활용은 별도 단계'}
 ]);
 const NAMES=Object.freeze({'review-watcher':'협업 운송 전환','dashboard':'CoWork 대시보드','skill-discovery':'스킬 발견·재사용','job-list':'업무 자동화 후보','knowledge-design':'지식 구조 설계'});
 const $=id=>document.getElementById(id);
 const text=(tag,cls,v)=>{const n=document.createElement(tag);if(cls)n.className=cls;n.textContent=v;return n};
 const safe=s=>typeof s==='string'&&s.length<=180&&!/[<>]/.test(s);
 let previous=null;
 let pending=false;
 function approved(j){
   if(!j||j.schema!=='COWORK_PUBLIC_STATUS_V1'||!Array.isArray(j.work_cards)||j.work_cards.length>5||!j.checks||!safe(j.generated_at))return false;
   const time=Date.parse(j.generated_at);
   if(!Number.isFinite(time)||time>Date.now()+3600000)return false;
   const allowedLive=(j.cutover==='GitHub LIVE (호스트 보고 수용)'&&j.checks.active_provider==='GitHub 리뷰 운송 LIVE (호스트 보고 수용)');
   const allowedLegacy=(j.cutover==='정식 전환 전'&&['활성 리뷰 제공자 없음','Dropbox 리뷰 제공자 (문서 기록)','기록 미확인'].includes(j.checks.active_provider));
   if(!allowedLive&&!allowedLegacy)return false;
   const seen=new Set();
   return j.work_cards.every(c=>c&&Object.hasOwn(NAMES,c.category)&&!seen.has(c.category)&&seen.add(c.category)&&c.title===NAMES[c.category]&&Number.isInteger(c.phase_index)&&c.phase_index>=0&&c.phase_index<=5&&['owner','phase_label','test_label','review_label','next_action'].every(k=>safe(c[k])));
 }
 const compact=j=>Object.fromEntries(j.work_cards.map(c=>[c.category,JSON.stringify([c.phase_index,c.phase_label,c.test_label,c.review_label,c.next_action])]));
 function openArea(category){
   const nav=document.querySelector('[data-tab="collab"]');
   if(nav)nav.click();
   const search=$('search');
   if(search){search.value=NAMES[category];search.dispatchEvent(new Event('input',{bubbles:true}));}
   const found=document.querySelector('#workview [data-category="'+category+'"]');
   if(found)found.focus({preventScroll:false});
 }
 function overview(j){
   const target=$('contextCards');if(!target)return;
   target.replaceChildren();
   const map=Object.fromEntries(j.work_cards.map(c=>[c.category,c]));
   for(const field of FIELDS){
     const c=map[field.id];
     const box=text('article','cx-card','');
     box.append(text('h3','',field.title));
     box.append(text('p','cx-state',c?c.phase_label:'공개 기록 미확인'));
     box.append(text('p','cx-next',c?'다음 확인: '+c.next_action:'공개 근거가 없어 판단 보류'));
     box.append(text('p','cx-hint',field.hint));
     const btn=text('button','cx-link','관련 공개 업무 보기');
     btn.type='button';btn.disabled=!c;btn.addEventListener('click',()=>openArea(field.id));box.append(btn);
     target.append(box);
   }
   $('contextStamp').textContent='공개 자료 마지막 변경: '+new Date(j.generated_at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})+' · 호스트 최신 실측 시각 아님';
 }
 function links(j){
   const box=$('contextRelations');if(!box)return;box.replaceChildren();
   const present=new Set(j.work_cards.map(c=>c.category));
   const flow=FIELDS.filter(f=>present.has(f.id));
   if(!flow.length){box.append(text('p','cx-hint','공개 연결 자료 없음'));return}
   const row=text('div','cx-flow','');
   flow.forEach((f,i)=>{if(i)row.append(text('span','cx-arrow','→'));row.append(text('span','cx-node',f.title))});
   box.append(row,text('p','cx-hint','책임·인계 관점의 개념 연결이며 실제 자동 호출·승인·설치·분석 성공을 뜻하지 않습니다. Work ID·리뷰 ID·영수증 상세는 PRIVATE 근거에서만 확인합니다.'));
 }
 function deltas(now,j){
   const box=$('contextDelta');if(!box)return;box.replaceChildren();
   if(previous===null){box.append(text('p','cx-hint','이번 페이지 열람 중 이전에 비교할 공개 스냅샷이 없습니다. 과거 변경 이력을 추정하지 않습니다.'));previous=now;return}
   const changed=Object.keys(NAMES).filter(k=>previous[k]!==now[k] && (Object.hasOwn(previous,k)||Object.hasOwn(now,k)));
   if(changed.length===0){box.append(text('p','cx-hint','이번 페이지 열람 중 확인한 공개 상태 필드의 변화 없음 · 최신 실측을 의미하지 않습니다.'));}
   else {
     box.append(text('p','cx-state','이번 열람 중 공개 항목 '+changed.length+'개에서 변경 관측'));
     for(const id of changed){const current=j.work_cards.find(c=>c.category===id);box.append(text('p','cx-change',NAMES[id]+': '+(current?current.phase_label+' / '+current.next_action:'공개 자료에서 사라짐')))}
   }
   previous=now;
 }
 function unavailable(){
   const box=$('contextCards');if(box)box.replaceChildren(text('p','cx-hint','공개 상태 수신·검증 실패: 현재 판단을 보류합니다. PRIVATE 정본 및 호스트 근거 확인 필요.'));
   if($('contextStamp'))$('contextStamp').textContent='현재 공개 정보 검증 실패';
   if($('contextRelations'))$('contextRelations').replaceChildren(text('p','cx-hint','원본 검증 전 관계 표시 보류'));
   if($('contextDelta'))$('contextDelta').replaceChildren(text('p','cx-hint','오류 상태에서는 변경분을 표시하지 않음'));
   previous=null;
 }
 async function refresh(){
  if(pending)return;pending=true;
  try{
    const r=await fetch('status.json',{cache:'no-store'});
    if(!r.ok)throw Error('status failed');
    const j=await r.json();
    if(!approved(j))throw Error('unapproved status');
    overview(j);links(j);deltas(compact(j),j);
  }catch(_){unavailable()}finally{pending=false}
 }
 refresh();
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
 window.addEventListener('focus',refresh);
 setInterval(refresh,120000);
})();
