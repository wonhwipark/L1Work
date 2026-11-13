/* CoWork PUBLIC Executive v2 - same-origin, allowlisted status only.
 * Security boundary is the PRIVATE exporter, not the browser. No HTML injection,
 * PRIVATE API, account data, model invocation or external network request.
 */
(() => {
  "use strict";
  const PHASES = ["요청", "개발", "리뷰", "판정", "완료"];
  const ALLOWED_KINDS = ["USER", "REVIEW", "BLOCKED", "OTHER"];
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
    return obj.work_cards.every(w => w && typeof w === "object" &&
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

  function buildCard(w, i) {
    const card = node("article", "wk-card");
    const header = node("div", "wk-header");
    header.append(node("span", "wk-skill", w.category));
    const badge = node("span", "wk-status " + (kind(w) === "USER" ? "user" :
                   kind(w) === "BLOCKED" ? "blocked" :
                   kind(w) === "REVIEW" ? "review" : ""), w.phase_label);
    header.append(badge);
    card.append(header, node("h3", "", w.title));
    const stage = node("div", "wk-steps");
    stage.setAttribute("aria-label", "현재 문서상 단계 · 이전 단계 검증 완료를 의미하지 않음");
    PHASES.forEach((name, index) => {
      const step = node("span", w.phase_index === index + 1 ? "current" : "", name);
      step.prepend(node("i"));
      stage.append(step);
    });
    card.append(stage);
    const meta = node("div", "wk-meta");
    [["담당", w.owner], ["자체시험", w.test_label], ["독립 리뷰", w.review_label]].forEach(([a,b]) => {
      const cell = node("div");
      cell.append(node("b", "", a), node("span", "", b));
      meta.append(cell);
    });
    card.append(meta);
    const action = node("div", "wk-action");
    action.append(node("strong", "", "다음 조치"), document.createTextNode(" · " + w.next_action));
    card.append(action);
    card.append(node("p", "wk-note", "문서 신고 단계 · 검증된 완료율 아님"));
    return card;
  }

  function renderCards() {
    const grid = $(".wk-grid"), empty = $("#work-filter-empty");
    if (!grid || !data) return;
    const all = [...data.work_cards].sort((a, b) =>
      PRIORITY[kind(a)] - PRIORITY[kind(b)] || a.title.localeCompare(b.title, "ko"));
    const filtered = all.filter(w =>
      (selectedFilter === "all" || kind(w) === selectedFilter) &&
      (w.title + " " + w.category + " " + w.phase_label + " " + w.next_action)
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
    [counts.projects, counts.requests, counts.reviews, counts.receipts].forEach((v, i) => {
      if (kpis[i]) kpis[i].textContent = String(v);
    });
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
    const examples = $(".wk-examples");
    if (examples) {
      const title = $("strong", examples);
      if (title) title.textContent = "스킬별 Work 등록 · 공개 허용 목록에 있는 경우 카드로 표시";
      examples.querySelectorAll(".wk-pills span").forEach(el => {
        const label = el.textContent.includes("l1-fix-workflow") ?
          "l1-fix-workflow" : "l1-github";
        const exists = obj.work_cards.some(w => w.title.startsWith(label));
        el.replaceChildren(document.createTextNode(label + " "),
          node("em", "", exists ? "등록 확인 · 카드에서 단계 확인" :
            "미등록 또는 공개 근거 미확인"));
      });
    }
    renderCards();
  }
  const POLL_MS = 120000;
  async function refresh() {
    const notice = $("#public-sync-status");
    if (!notice || inFlight || document.visibilityState === "hidden" ||
        Date.now() - checkedAt < 15000) return;
    inFlight = true;
    checkedAt = Date.now();
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
    search = input.value.trim().toLocaleLowerCase("ko");
    renderCards();
  });
  document.querySelectorAll("[data-work-filter]").forEach(button => {
    button.addEventListener("click", () => {
      selectedFilter = button.dataset.workFilter;
      renderCards();
    });
  });
  const reset = $("#reset-work-filters");
  if (reset) reset.addEventListener("click", () => {
    selectedFilter = "all"; search = "";
    if (input) input.value = "";
    renderCards();
  });
  refresh();
  window.setInterval(refresh, POLL_MS);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") refresh();
  });
  window.addEventListener("focus", refresh);
})();