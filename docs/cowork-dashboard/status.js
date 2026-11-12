/* CoWork PUBLIC Pages: display only already-sanitized status.json.
 * No PRIVATE repository/API access. No third-party requests. No HTML insertion.
 * This is a browser viewer, NOT a security filter: private exporter owns the gate.
 */
(() => {
  "use strict";
  const PHASE_NAMES = ["요청", "개발", "리뷰", "판정", "완료"];
  const MAX_CARDS = 30;
  const fields = ["title", "category", "owner", "phase_label", "review_label", "test_label", "next_action"];
  const by = (selector, parent = document) => parent.querySelector(selector);
  const make = (tag, className, value) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = String(value);
    return el;
  };
  function valid(data) {
    if (!data || typeof data !== "object" || Array.isArray(data) ||
        data.schema !== "COWORK_PUBLIC_STATUS_V1" ||
        data.source !== "APPROVED_AGGREGATE_ONLY" ||
        data.cutover !== "정식 전환 전" ||
        !["AUTOMATED_ALLOWLIST", "BOOTSTRAP_NOT_AUTO"].includes(data.sync_mode) ||
        !/^\d{4}-\d{2}-\d{2}$/.test(data.snapshot_date || "")) return false;
    const counts = data.counts;
    if (!counts || typeof counts !== "object" ||
        !["projects", "requests", "reviews", "receipts", "works"].every(key =>
          Number.isSafeInteger(counts[key]) && counts[key] >= 0 && counts[key] <= 100000)) return false;
    if (!Array.isArray(data.work_cards) || data.work_cards.length > MAX_CARDS) return false;
    return data.work_cards.every(card =>
      card && typeof card === "object" && fields.every(k =>
        typeof card[k] === "string" && card[k].length <= 180) &&
      Number.isInteger(card.phase_index) &&
      card.phase_index >= 0 && card.phase_index <= 5
    );
  }
  function cardNode(item, index) {
    const card = make("article", "wk-card");
    const head = make("div", "wk-header");
    head.append(make("span", "wk-skill", "WORK " + String(index + 1).padStart(2, "0") + " · " + item.category));
    const chip = make("span", "wk-status" + (item.phase_index === 0 ? " blocked" : ""), item.phase_label);
    head.append(chip);
    card.append(head, make("h3", "", item.title));
    const steps = make("div", "wk-steps");
    steps.setAttribute("aria-label", "진행 위치 표시 · 검증된 완료율 아님");
    PHASE_NAMES.forEach((label, i) => {
      const cls = item.phase_index === i + 1 ? "current" :
                  item.phase_index > i + 1 ? "past" : "";
      const segment = make("span", cls, label);
      segment.prepend(make("i"));
      steps.append(segment);
    });
    card.append(steps);
    const meta = make("div", "wk-meta");
    [["담당", item.owner], ["개발자 자체시험", item.test_label],
     ["독립 리뷰", item.review_label]].forEach(([name, value]) => {
      const box = make("div");
      box.append(make("b", "", name), make("span", "", value));
      meta.append(box);
    });
    card.append(meta);
    const action = make("div", "wk-action");
    action.append(make("strong", "", "다음 조치"), document.createTextNode(" · " + item.next_action));
    card.append(action, make("p", "wk-note", "PRIVATE 기록 기반 상위 단계 신고 · 완료 증빙 아님"));
    return card;
  }
  function update(data) {
    const list = by(".wk-grid");
    const notice = by("#public-sync-status");
    if (!list || !notice) return;
    const counts = data.counts;
    const kpis = document.querySelectorAll(".kpi-num");
    [counts.projects, counts.requests, counts.reviews, counts.receipts].forEach((value, i) => {
      if (kpis[i]) kpis[i].textContent = String(value);
    });
    const tags = by(".wk-tags");
    if (tags) {
      const tally = {
        development: data.work_cards.filter(x => x.phase_index === 2).length,
        review: data.work_cards.filter(x => x.phase_index === 3).length,
        blocked: data.work_cards.filter(x => x.phase_index === 0).length,
        complete: data.work_cards.filter(x => x.phase_index === 5).length
      };
      tags.replaceChildren(...[
        ["공개 허용 Work", data.work_cards.length],
        ["개발 단계 신고", tally.development],
        ["리뷰 단계 신고", tally.review],
        ["완료 신고(미검증)", tally.complete],
        ["단계·게이트 미확인", tally.blocked]
      ].map(([key,value]) => {
        const label = make("span");
        label.append(document.createTextNode(key + " "), make("b", "", value));
        return label;
      }));
    }
    list.replaceChildren(...data.work_cards.map(cardNode));
    const date = data.snapshot_date.replaceAll("-", ".");
    const label = data.sync_mode === "AUTOMATED_ALLOWLIST" ?
      "자동 갱신 연결 · PUBLIC 허용 상태만 · 기준일 " + date :
      "초기 상태 게시 · 자동 발행 인증 설정 대기 · 기준일 " + date;
    notice.textContent = label;
    const upperDate = by(".hero-tags span");
    if (upperDate) upperDate.textContent = date + " 기준";
    const examples = by(".wk-examples");
    if (examples) {
      const title = by("strong", examples);
      if (title) title.textContent = "스킬별 독립 Work 등록 현황 · 실제 등록 시 카드에 반영";
      examples.querySelectorAll(".wk-pills span").forEach(el => {
        const label = el.textContent.includes("l1-fix-workflow") ? "l1-fix-workflow" : "l1-github";
        const present = data.work_cards.some(x => x.title.startsWith(label));
        el.replaceChildren(document.createTextNode(label + " "),
                           make("em", "", present ? "등록됨 · 카드에서 단계 확인" : "미등록 · 상태 미확인"));
      });
    }
  }
  async function run() {
    const notice = by("#public-sync-status");
    if (!notice) return;
    try {
      const response = await fetch("./status.json", {cache: "no-store", credentials: "omit"});
      if (!response.ok) throw new Error("status unavailable");
      const data = await response.json();
      if (!valid(data)) throw new Error("invalid public schema");
      update(data);
    } catch (_) {
      notice.textContent = "마지막 게시 스냅샷 표시 중 · 자동 동기화 데이터 확인 필요";
    }
  }
  run();
})();
