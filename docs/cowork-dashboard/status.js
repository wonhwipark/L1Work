/* CoWork PUBLIC Executive v4 - same-origin, allowlisted status only.
 * Security boundary is the PRIVATE exporter, not the browser. No HTML injection,
 * PRIVATE API, account data, model invocation or external network request.
 */
(() => {
  "use strict";
  const PHASES = ["요청", "개발", "리뷰", "판정", "완료"];

  const HANDOFF_LINKS = Object.freeze({
    "msc-b-viewer": "https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md"
  });
  const HANDOFF_LABELS = ["문서 게시", "리뷰 요청", "결과 접수", "GPT 판정", "후속 반영"];
  const HANDOFF_STATUS = {
    PUBLISHED: ["인계 게시 완료 · 리뷰 미실행", 1],
    REQUESTED: ["리뷰 요청 기록 · 실행 확인 전", 2],
    RECEIVED: ["리뷰 결과 접수 기록", 3],
    DECIDED: ["GPT 판정 기록", 4],
    APPLIED: ["후속 반영 기록 · 검증 별도", 5]
  };
  function validHandoffs(cards) {
    if (cards === undefined) return true; // V1 snapshot created before this feature
    if (!Array.isArray(cards) || cards.length > 8) return false;
    const seen = new Set();
    return cards.every(h => {
      if (!h || typeof h !== "object" || Array.isArray(h) ||
          !Object.hasOwn(HANDOFF_LINKS,h.id) || seen.has(h.id) ||
          !Object.hasOwn(HANDOFF_STATUS,h.stage) ||
          typeof h.title !== "string" || h.title.length > 100 ||
          typeof h.kind !== "string" || h.kind.length > 50 ||
          typeof h.review_label !== "string" || h.review_label.length > 90 ||
          typeof h.next_action !== "string" || h.next_action.length > 140 ||
          typeof h.updated_on !== "string" || !/^20[0-9]{2}-[0-9]{2}-[0-9]{2}$/.test(h.updated_on) ||
          h.source_url !== HANDOFF_LINKS[h.id]) return false;
      seen.add(h.id);
      return true;
    });
  }
  // Handoff history is independent of the PRIVATE review/Work status exporter.
  // All sources are already PUBLIC L1Work handoffs; never infer feedback state.
  const HISTORY_FILENAME = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,179}\\.md$/;
  const HISTORY_BASE = "https://github.com/wonhwipark/L1Work/blob/main/handoffs/";
  let historyCached = "";
  let historyInFlight = false;
  function validHandoffHistory(obj) {
    if (!obj || typeof obj !== "object" || Array.isArray(obj) ||
        obj.schema !== "L1WORK_HANDOFF_HISTORY_V1" ||
        !Array.isArray(obj.entries) || obj.entries.length > 3) return false;
    const seen = new Set();
    return obj.entries.every(entry => {
      if (!entry || typeof entry !== "object" || Array.isArray(entry) ||
          typeof entry.filename !== "string" ||
          !HISTORY_FILENAME.test(entry.filename) ||
          !entry.filename.toUpperCase().includes("HANDOFF") ||
          seen.has(entry.filename) ||
          typeof entry.title !== "string" ||
          entry.title.length < 1 || entry.title.length > 130 ||
          typeof entry.published_on !== "string" ||
          !/^20\\d{2}-\\d{2}-\\d{2}$/.test(entry.published_on) ||
          !Number.isFinite(Date.parse(entry.published_on))) return false;
      seen.add(entry.filename);
      return true;
    });
  }
  function renderHandoffHistory(items) {
    const list = $("#handoff-list");
    if (!list) return;
    const cards = items.map((item, index) => {
      const card = node("article", "handoff-card");
      const head = node("div", "handoff-card-head");
      const date = node("time", "handoff-date", "게시일 " + item.published_on);
      date.dateTime = item.published_on;
      head.append(node("span", "handoff-type", "공개 인계서 · " + (index + 1)), date);
      const link = node("a", "handoff-link", "원문 열기");
      link.href = HISTORY_BASE + encodeURIComponent(item.filename);
      card.append(head, node("h3", "", item.title), link);
      return card;
    });
    list.replaceChildren(...cards);
    const count = $("#handoff-count");
    if (count) count.textContent = "최근 " + items.length + "건 · 공개 문서";
  }
  async function refreshHandoffHistory() {
    if (historyInFlight || !$("#handoff-list")) return;
    historyInFlight = true;
    try {
      const response = await fetch("./handoffs.json", {cache: "no-store", credentials: "omit"});
      if (!response.ok) throw new Error("Public handoff history unavailable");
      const obj = await response.json();
      if (!validHandoffHistory(obj)) throw new Error("Public handoff history rejected");
      const signature = JSON.stringify(obj);
      if (signature !== historyCached) {
        renderHandoffHistory(obj.entries);
        historyCached = signature;
      }
    } catch (_) {
      // Keep the three known PUBLIC document links from the static HTML fallback.
    } finally {
      historyInFlight = false;
    }
  }

  const ALLOWED_KINDS = ["USER", "REVIEW", "BLOCKED", "OTHER"];
  // Fixed, public-safe work explanations. Never built from PRIVATE free text.
  const WORK_INFO = Object.freeze({
    "review-watcher": { purpose: "스킬 개발 결과를 독립 리뷰와 GPT 최종 판정까지 안전하게 연결하는 협업 경로 정비", outcome: "검증 가능한 리뷰 요청·결과 연결과 전환 준비" },
    "dashboard": { purpose: "여러 작업의 담당·진행 단계·확인할 일을 GitHub에서 자동 수집해 한 화면에 표시", outcome: "업데이트 시 자동 반영되는 업무 현황 화면" },
    "skill-discovery": { purpose: "이미 보유한 스킬의 기능·적용 범위를 검토해 중복 개발 대신 재사용", outcome: "근거가 확인된 스킬 기능 목록과 재사용 기준" },
    "job-list": { purpose: "Job-list 기반 작업 실행·결과 확인 절차를 검토하고 후보를 시험", outcome: "실행 환경 검증을 거친 원샷 자동화 흐름" },
    "knowledge-design": { purpose: "업무별 지식과 이슈 이력을 구조화해 찾고 갱신하기 쉬운 방식 설계", outcome: "지식 분류 기준과 검색·갱신 구조" }
  });
  const UNKNOWN_INFO = Object.freeze({purpose:"공개 승인된 업무 범주의 목적 설명 확인 중",outcome:"공개 범위 검증 후 표시"});
  const STATUS_VALUES = ["미실행·대기", "기록 미관측", "추가 증거 검증 필요"];
  const PROVIDERS = ["활성 리뷰 제공자 없음", "Dropbox 리뷰 제공자 (문서 기록)", "기록 미확인"];
  const FIELDS = ["title", "category", "owner", "phase_label", "review_label", "test_label", "next_action"];
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const node = (tag, className = "", value) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = String(value);
    return el;
  };
  let data = null;
  let selectedFilter = "all";
  let selectedWork = null;
  let search = "";
  let inFlight = false;
  let checkedAt = 0;
  let cached = "";

  function valid(obj) {
    if (!obj || typeof obj !== "object" || Array.isArray(obj) ||
        obj.schema !== "COWORK_PUBLIC_STATUS_V1" ||
        obj.source !== "APPROVED_AGGREGATE_ONLY" ||
        obj.cutover !== "정식 전환 전" ||
        !["AUTOMATED_ALLOWLIST", "BOOTSTRAP_NOT_AUTO"].includes(obj.sync_mode) ||
        !/^\d{4}-\d{2}-\d{2}$/.test(obj.snapshot_date || "")) return false;
    if (obj.generated_at !== undefined &&
        (typeof obj.generated_at !== "string" ||
         !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(obj.generated_at) ||
         !Number.isFinite(Date.parse(obj.generated_at)))) return false;
    if (!obj.counts || typeof obj.counts !== "object" ||
        !["projects", "works", "requests", "reviews", "receipts"].every(k =>
          Number.isSafeInteger(obj.counts[k]) && obj.counts[k] >= 0 &&
          obj.counts[k] <= 100000)) return false;
    if (!obj.checks || typeof obj.checks !== "object" ||
        !STATUS_VALUES.includes(obj.checks.independent_review) ||
        !STATUS_VALUES.includes(obj.checks.windows_stage1) ||
        !PROVIDERS.includes(obj.checks.active_provider || "기록 미확인")) return false;
    if (!Array.isArray(obj.work_cards) || obj.work_cards.length > 30 ||
        obj.work_cards.length > obj.counts.works) return false;
    return validHandoffs(obj.handoffs) && obj.work_cards.every(w => w && typeof w === "object" &&
      FIELDS.every(k => typeof w[k] === "string" && w[k].length <= 180) &&
      Number.isInteger(w.phase_index) && w.phase_index >= 0 && w.phase_index <= 5 &&
      (w.action_kind === undefined || ALLOWED_KINDS.includes(w.action_kind)));
  }

  function prettyDate(iso) {
    if (!iso) return "생성 시각 미제공 · 날짜만 확인";
    const d = new Date(iso);
    return new Intl.DateTimeFormat("ko-KR", {
      timeZone: "Asia/Seoul", year: "numeric", month: "2-digit",
      day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false
    }).format(d) + " KST";
  }
  function kind(w) {
    return ALLOWED_KINDS.includes(w.action_kind) ? w.action_kind :
      w.phase_index === 3 ? "REVIEW" : w.phase_index === 0 ? "BLOCKED" : "OTHER";
  }
  const PRIORITY = {USER: 0, BLOCKED: 1, REVIEW: 2, OTHER: 3};

  const workKey = w => w.category + "|" + w.title;

  function buildCard(w) {
    const card = node("article", "wk-card");
    const header = node("div", "wk-header");
    header.append(node("span", "wk-skill", w.category));
    header.append(node("span",
      "wk-status " + (kind(w) === "BLOCKED" ? "blocked" : kind(w) === "REVIEW" ? "review" : ""),
      w.phase_label));
    card.append(header, node("h3", "", w.title));
    const info = WORK_INFO[w.category] || UNKNOWN_INFO;
    card.append(node("p", "wk-purpose", info.purpose));
    const outcome = node("div", "wk-outcome");
    outcome.append(node("strong", "", "목표 산출물"), node("span", "", info.outcome));
    card.append(outcome);

    const facts = node("div", "wk-factlist");
    const addFact = (label, value, className = "") => {
      const el = node("div", className);
      el.append(node("strong", "", label), node("span", "", value));
      facts.append(el);
    };
    addFact("현재 확인 가능한 시험 기록", w.test_label);
    addFact("독립 검증 상태", w.review_label);
    addFact("남은 작업 · 다음 조치", w.next_action, "wk-fact-next");
    if (kind(w) === "BLOCKED")
      addFact("차단 분류", "공개 상태에서 차단 분류됨 · 구체적 사유는 공개 자료에 없음", "wk-fact-risk");
    card.append(facts);

    const stage = node("div", "wk-steps");
    stage.setAttribute("aria-label", "문서상 현재 단계만 강조 · 이전 단계 완료를 뜻하지 않음");
    PHASES.forEach((name, index) => {
      const step = node("span", w.phase_index === index + 1 ? "current" : "", name);
      step.prepend(node("i"));
      stage.append(step);
    });
    card.append(stage);
    const meta = node("div", "wk-meta");
    const owner = node("div");
    owner.append(node("b", "", "담당"), node("span", "", w.owner));
    meta.append(owner);
    card.append(meta);
    card.append(node("p", "wk-note", "문서상 단계·자체시험 기록은 실제 완료 및 독립 리뷰 PASS를 의미하지 않습니다."));
    return card;
  }

  function openWorkDetail(w) {
    selectedWork = workKey(w);
    selectedFilter = "all";
    search = "";
    const input = $("#work-search");
    if (input) input.value = "";
    const details = $("#work-tracker");
    if (details) details.open = true;
    renderCards();
    if (details && typeof details.scrollIntoView === "function")
      details.scrollIntoView({block: "start", behavior: "smooth"});
  }

  function renderOverview() {
    const tbody = $("#work-overview-rows");
    if (!tbody || !data) return;
    const all = [...data.work_cards].sort((a, b) =>
      PRIORITY[kind(a)] - PRIORITY[kind(b)] || a.title.localeCompare(b.title, "ko"));
    const rows = all.map(w => {
      const info = WORK_INFO[w.category] || UNKNOWN_INFO;
      const tr = node("tr");
      const title = node("th", "portfolio-name");
      title.setAttribute("scope", "row");
      title.append(node("strong", "", w.title), node("span", "portfolio-phase", w.phase_label));
      const open = node("button", "portfolio-open", "상세 보기");
      open.type = "button";
      open.setAttribute("aria-label", w.title + " 상세 검증 펼쳐 보기");
      open.setAttribute("aria-controls", "work-tracker");
      open.addEventListener("click", () => openWorkDetail(w));
      title.append(open);
      const objective = node("td", "portfolio-purpose", info.purpose);
      objective.dataset.label = "무엇을 해결하나";
      const evidence = node("td", "portfolio-evidence");
      evidence.dataset.label = "확인된 기록";
      evidence.append(node("span", "", w.test_label), node("small", "", w.review_label));
      const next = node("td", "portfolio-next", w.next_action);
      next.dataset.label = "남은 작업";
      tr.append(title, objective, evidence, next);
      return tr;
    });
    tbody.replaceChildren(...rows);
    const count = $("#overview-visible-count");
    if (count) count.textContent = "공개 " + all.length + "개 · 전체 " + data.counts.works + "개 중";
  }

  function renderCards() {
    const grid = $(".wk-grid"), empty = $("#work-filter-empty");
    if (!grid || !data) return;
    const all = [...data.work_cards].sort((a, b) =>
      PRIORITY[kind(a)] - PRIORITY[kind(b)] || a.title.localeCompare(b.title, "ko"));
    const filtered = all.filter(w =>
      (selectedWork === null || workKey(w) === selectedWork) &&
      (selectedFilter === "all" || kind(w) === selectedFilter) &&
      (w.title + " " + w.category + " " + w.phase_label + " " + w.next_action +
       " " + (WORK_INFO[w.category] || UNKNOWN_INFO).purpose +
       " " + (WORK_INFO[w.category] || UNKNOWN_INFO).outcome +
       " " + w.test_label + " " + w.review_label)
        .toLocaleLowerCase("ko").includes(search));
    grid.replaceChildren(...filtered.map(buildCard));
    if (empty) {
      empty.hidden = filtered.length !== 0;
      empty.textContent = selectedFilter === "USER" ?
        "현재 공개 자료에서 확인된 추가 사용자 조치가 없습니다." :
        "조건과 일치하는 공개 작업이 없습니다. 다른 필터를 선택해 주세요.";
    }
    const n = $("#work-filter-count");
    if (n) n.textContent = "공개 " + data.work_cards.length + "개 중 " + filtered.length + "개 표시";
    document.querySelectorAll("[data-work-filter]").forEach(b => {
      const pressed = b.dataset.workFilter === selectedFilter;
      b.setAttribute("aria-pressed", String(pressed));
      b.classList.toggle("selected", pressed);
    });
  }

  function render(obj) {
    data = obj;
    const counts = obj.counts;
    const kpis = document.querySelectorAll(".kpi-num");
    [counts.works, obj.work_cards.length,
      obj.work_cards.filter(w => kind(w) === "REVIEW").length,
      obj.work_cards.filter(w => kind(w) === "BLOCKED").length].forEach((v, i) => {
      if (kpis[i]) kpis[i].textContent = String(v);
    });
    for (const [selector, value] of [
      ["#tech-requests", counts.requests],
      ["#tech-reviews", counts.reviews],
      ["#tech-receipts", counts.receipts]
    ]) {
      const el = $(selector);
      if (el) el.textContent = String(value);
    }
    const visible = obj.work_cards.length;
    const hidden = Math.max(0, counts.works - visible);
    const covered = $("#work-coverage");
    if (covered) covered.textContent =
      "전체 Work " + counts.works + "개 · 공개 " + visible + "개 · 비공개/미승인 " + hidden + "개";
    const total = $("#work-coverage-note");
    if (total) total.textContent = "공개 허용 목록에 없는 작업은 이름과 상세를 표시하지 않습니다.";
    const urgent = obj.work_cards.filter(w => kind(w) === "USER").length;
    const attention = $("#work-attention-count");
    if (attention) attention.textContent = String(urgent);
    const quick = $("#work-priority-message");
    if (quick) quick.textContent = urgent ?
      "사용자 확인이 필요한 공개 작업 " + urgent + "개" :
      "현재 공개 정보 기준 추가 사용자 조치 없음";
    const generated = prettyDate(obj.generated_at);
    const produced = $("#generated-time");
    if (produced) produced.textContent = generated;
    const provider = obj.checks.active_provider || "기록 미확인";
    for (const sel of ["#active-provider-label", "#active-provider-path", "#review-provider-badge"]) {
      const el = $(sel);
      if (el) el.textContent = provider;
    }
    const operation = $("#operational-state-label");
    if (operation) operation.textContent = provider === "활성 리뷰 제공자 없음" ?
      "현재 자동 리뷰 실행 중지 · GitHub 정식 LIVE 전환 전" :
      "최신 운영 기록 기반 · 정식 전환 전";
    document.querySelectorAll(".tablebox tbody tr").forEach(tr => {
      const title = tr.querySelector("th")?.textContent?.trim();
      const badge = tr.querySelector("td .state");
      if (!badge) return;
      if (title === "Windows 호스트 검증") badge.textContent = obj.checks.windows_stage1;
      if (title === "독립 리뷰") badge.textContent = obj.checks.independent_review;
      if (title === "활성 리뷰 제공자") badge.textContent = provider;
      badge.className = "state gray";
    });
    const date = obj.snapshot_date.replaceAll("-", ".");
    for (const sel of ["#work-snapshot-date", "#summary-snapshot-date"]) {
      const el = $(sel);
      if (el) el.textContent = date;
    }
    const upper = $(".hero-tags span");
    if (upper) upper.textContent = date + " 기준";
    const controls = $("#work-controls");
    if (controls) controls.hidden = false;
    if (selectedWork && !obj.work_cards.some(w => workKey(w) === selectedWork)) selectedWork = null;
    renderOverview();
    renderCards();
  }
  const POLL_MS = 120000;
  async function refresh() {
    const notice = $("#public-sync-status");
    if (!notice || inFlight || document.visibilityState === "hidden" ||
        Date.now() - checkedAt < 15000) return;
    inFlight = true;
    checkedAt = Date.now();
    void refreshHandoffHistory();
    try {
      const response = await fetch("./status.json", {cache: "no-store", credentials: "omit"});
      if (!response.ok) throw new Error("PUBLIC status unavailable");
      const obj = await response.json();
      if (!valid(obj)) throw new Error("PUBLIC status schema rejected");
      const signature = JSON.stringify(obj);
      if (signature !== cached) {
        render(obj);
        cached = signature;
      }
      const time = new Intl.DateTimeFormat("ko-KR", {
        timeZone: "Asia/Seoul", hour: "2-digit", minute: "2-digit", hour12: false
      }).format(new Date());
      const checkTime = $("#last-check-time");
      if (checkTime) checkTime.textContent = time + " KST";
      notice.textContent = obj.sync_mode === "AUTOMATED_ALLOWLIST" ?
        "공개 상태 수신 정상 · 페이지 열린 동안 2분마다 확인" :
        "초기 공개 상태 · 자동 게시 설정 확인 필요";
    } catch (_) {
      notice.textContent = data ?
        "최근 수신한 상태 표시 중 · 다음 자동 확인 대기" :
        "공개 상태 확인 실패 · 정적 기본 화면 표시 중";
    } finally {
      inFlight = false;
    }
  }

  const input = $("#work-search");
  if (input) input.addEventListener("input", () => {
    selectedWork = null;
    search = input.value.trim().toLocaleLowerCase("ko");
    renderCards();
  });
  document.querySelectorAll("[data-work-filter]").forEach(button => {
    button.addEventListener("click", () => {
      selectedWork = null;
      selectedFilter = button.dataset.workFilter;
      renderCards();
    });
  });
  const reset = $("#reset-work-filters");
  if (reset) reset.addEventListener("click", () => {
    selectedWork = null; selectedFilter = "all"; search = "";
    if (input) input.value = "";
    renderCards();
  });
  const detailLink = document.querySelector('a[href="#work-tracker"]');
  if (detailLink) detailLink.addEventListener("click", () => {
    const details = $("#work-tracker");
    if (details) details.open = true;
    selectedWork = null;
    renderCards();
  });
  refresh();
  window.setInterval(refresh, POLL_MS);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") refresh();
  });
  window.addEventListener("focus", refresh);
})();