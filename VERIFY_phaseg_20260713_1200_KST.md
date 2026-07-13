# VERIFY — Phase G 내부 실행 검증 (code-analyzer v0.9.10)

목적: Phase G(flow 취합)가 사내 실제 코드에서 의도대로 도는지 확인한다.
설계 가정(호출 체인으로 순서 확정 / 심볼 페어링 / 거짓 결손 방지)이 실물에서 성립하는지 본다.

**출력 규칙**
- 결과는 두 블록으로 나뉜다.
  - **[LOCAL]** — 심볼명이 들어간다. **사내에만 두고 밖으로 옮기지 않는다.** `flow_pairing.json` 작성용.
  - **[REPORT]** — **숫자 한 줄.** 이것만 옮겨 적으면 된다. 코드 정보 없음.
- 스크립트는 기존 산출물을 **고치지 않는다.** 새 timestamp 파일만 만든다.

---

## STEP 0 — 사전 조건

1. v0.9.10 설치 (`SKILL.md`에 `version: v0.9.10`)
2. **서로 다른 소스 파일 2개 이상** 분석 완료 (Phase F까지). 가급적 **REQ 송신 파일 + CNF 수신 파일** 한 쌍.
   → file_group이 1개면 Phase G는 `PHASEG_SKIP:SINGLE_FILE_GROUP`으로 정상 skip된다(검증 불가).

## STEP 1 — 실행

`code_analyzer_output`이 있는 폴더에서 아래를 `phaseg_verify.py`로 저장하고 실행한다.

```
python phaseg_verify.py
```

경로가 다르면: `python phaseg_verify.py <code_analyzer_output 경로> <스킬 scripts 폴더>`

```python
# phaseg_verify.py  (read-only inspection; runs the Phase G scripts, edits nothing)
import sys, os, json, glob, subprocess, collections

root = sys.argv[1] if len(sys.argv) > 1 else "code_analyzer_output"
skill = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
    "~/.claude/skills/code-analyzer/scripts")

V = {}

# V0: installed skill version
sk = os.path.join(os.path.dirname(skill), "SKILL.md")
try:
    txt = open(sk, encoding="utf-8", errors="ignore").read()
    V["V0"] = 1 if "version: v0.9.10" in txt else (2 if "version: v0.9" in txt else 3)
except Exception:
    V["V0"] = 4

# V1: composer run
comp = os.path.join(skill, "flow_composer.py")
rend = os.path.join(skill, "flow_msc_render.py")
try:
    r = subprocess.run([sys.executable, comp, root], capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0 and "FLOWS:" in out:
        V["V1"] = 1
    elif "AUTO_BLOCKED" in out:
        V["V1"] = 2
    else:
        V["V1"] = 3
except Exception:
    V["V1"] = 4
    out = ""

# V2: flows json
cands = glob.glob(os.path.join(root, "flows_*.json"))
data = None
if not cands:
    V["V2"] = 3
else:
    fj = sorted(cands, key=lambda p: os.path.getmtime(p))[-1]
    try:
        data = json.load(open(fj, encoding="utf-8"))
        V["V2"] = 1 if data.get("schema") == "code-analyzer/flows/v0" else 2
    except Exception:
        V["V2"] = 4

flows = (data or {}).get("flows") or []
steps = [s for f in flows for s in (f.get("steps") or [])]
pairs = [p for f in flows for p in (f.get("pairings") or [])]
pc = collections.Counter(p.get("pair_status") for p in pairs)
cc = collections.Counter(f.get("confidence") for f in flows)
ec = collections.Counter(s.get("evidence") for s in steps)

# V3: flow count
n = len(flows)
V["V3"] = 1 if n >= 3 else (2 if n == 2 else (3 if n == 1 else 4))

# V4: cross-file step (the whole point of Phase G)
cf = sum(1 for s in steps if s.get("cross_file"))
V["V4"] = 1 if cf >= 2 else (2 if cf == 1 else 3)

# V5: pair_status distribution
if not pairs:
    V["V5"] = 5
elif pc["paired"] and pc["unpaired"]:
    V["V5"] = 1
elif pc["paired"] and not pc["unpaired"]:
    V["V5"] = 2
elif pc["unpaired"] and not pc["paired"]:
    V["V5"] = 3
else:
    V["V5"] = 4

# V6: confidence distribution
if cc["HIGH"]:
    V["V6"] = 1
elif cc["MEDIUM"]:
    V["V6"] = 2
elif cc["LOW"]:
    V["V6"] = 3
else:
    V["V6"] = 4

# V7: call-chain evidence actually used (Q3=1 assumption holds?)
V["V7"] = 1 if ec["call-chain"] else (2 if ec["line-order"] else 3)

# V8: entry step from procedure_runtime_index
V["V8"] = 1 if ec["runtime-index"] else 2

# V9: MSC render (explicit paths; no cwd dependency)
try:
    if cands:
        subprocess.run([sys.executable, rend, fj, root], capture_output=True, text=True)
    pumls = glob.glob(os.path.join(root, "msc_flow", "*.puml"))
    ok = 0
    for p in pumls:
        t = open(p, encoding="utf-8", errors="ignore").read()
        if t.startswith("@startuml") and t.rstrip().endswith("@enduml"):
            ok += 1
    if pumls and ok == len(pumls):
        V["V9"] = 1
    elif pumls:
        V["V9"] = 2
    else:
        V["V9"] = 3
except Exception:
    V["V9"] = 4

# V10: out_of_inventory evidence path exercised
V["V10"] = 1 if pc["out_of_inventory"] else 2

# V11: [RN] volume
rn = sum(len(f.get("rn") or []) for f in flows) + len((data or {}).get("rn") or [])
V["V11"] = 1 if rn == 0 else (2 if rn <= 5 else (3 if rn <= 20 else 4))

# ---------- [LOCAL] internal only. Do NOT copy out. ----------
print("")
print("[LOCAL] --- internal only, do not copy out ---")
pol = (data or {}).get("pairing_policy") or {}
print("flow_pairing.json present:", pol.get("present"))
unp = sorted(set(p["symbol"] for p in pairs if p.get("pair_status") == "unpaired"))
oob = sorted(set(p["symbol"] for p in pairs if p.get("pair_status") == "out_of_inventory"))
print("unpaired symbols (review -> declare reply-less ones in flow_pairing.json):")
for s in unp:
    print("   -", s)
print("out_of_inventory symbols (handler outside analyzed scope):")
for s in oob:
    print("   -", s)
print("flows:", [f.get("flow_id") for f in flows])
print("")

# ---------- [REPORT] numbers only ----------
print("[REPORT] --- copy these two lines only ---")
print("VERIFY: " + " ".join("%s=%s" % (k, V[k]) for k in
                            sorted(V, key=lambda x: int(x[1:]))))
print("N: flows=%d steps=%d crossfile=%d paired=%d no_reply=%d out_of_inv=%d "
      "unpaired=%d rn=%d puml=%d"
      % (n, len(steps), cf, pc["paired"], pc["declared_no_reply"],
         pc["out_of_inventory"], pc["unpaired"], rn,
         len(glob.glob(os.path.join(root, "msc_flow", "*.puml")))))
```

---

## STEP 2 — 회신 (이 두 줄만)

```
VERIFY: V0=? V1=? V2=? V3=? V4=? V5=? V6=? V7=? V8=? V9=? V10=? V11=?
N: flows=? steps=? crossfile=? paired=? no_reply=? out_of_inv=? unpaired=? rn=? puml=?
```

[LOCAL] 블록은 옮기지 않는다. 그건 사내에서 `flow_pairing.json`을 쓸 때만 본다.

---

## 문항 정의 (해석표 — 회신 불필요)

**V0 설치 버전**
1. v0.9.10 2. v0.9.x 구버전 3. 버전 마커 없음 4. SKILL.md 못 찾음

**V1 composer 실행**
1. 정상 (FLOWS: 출력) 2. AUTO_BLOCKED (경로/입력 문제) 3. 스크립트 오류 4. 실행 자체 실패

**V2 flows json**
1. 생성됨, schema=flows/v0 2. 생성됐으나 schema 불일치 3. 생성 안 됨 4. 파싱 실패

**V3 flow 개수** — 1. 3개 이상 2. 2개 3. 1개 4. 0개

**V4 cross-file step (Phase G 존재 이유)**
1. 2개 이상 2. 1개 3. **0개** ← 파일 경계를 넘는 flow가 안 잡힘

**V5 pair_status 분포**
1. paired + unpaired 혼재 (정상적인 실코드 모습)
2. paired만 (짝이 전부 인벤토리 안에 있음)
3. unpaired만 ← 페어링이 전혀 성립 안 함
4. 그 외 조합 5. pairings 자체가 비어 있음 (송신 REQ 없음)

**V6 confidence 최고값** — 1. HIGH 존재 2. MEDIUM까지 3. LOW뿐 4. 없음

**V7 seq 근거** — 1. call-chain 사용됨 2. line-order로 폴백 3. 근거 없음

**V8 entry step** — 1. runtime-index에서 생성됨 2. 없음 (procedure_runtime_index 파싱 실패 의심)

**V9 flow MSC 렌더** — 1. 정상 (@startuml~@enduml) 2. 일부 손상 3. puml 0개 4. 렌더 실패

**V10 out_of_inventory** — 1. 있음 (call-edge escape 근거 작동) 2. 없음

**V11 [RN] 총량** — 1. 0개 2. 1~5 3. 6~20 4. 21개 이상

---

## 판정 기준 (내가 결과를 어떻게 읽는가)

| 결과 | 뜻 | 다음 |
|---|---|---|
| V1=1 V2=1 V4≥2 V6=1 V7=1 | **설계대로 동작** | v0.7(compare flows 소비) 트랙 진행 |
| V4=3 (cross-file 0) | 파일 경계를 넘는 flow가 안 잡힘 | 분석한 두 파일이 실제로 msg를 주고받는 쌍인지 확인. 맞다면 페어링 규칙 재설계 |
| V7=2 (line-order 폴백) | call_edges가 순서 근거로 못 쓰임 | edge 필드명이 스크립트 가정과 다름 → 필드명 확인 필요 |
| V8=2 | `procedure_runtime_index` 파싱 실패 | analysis_progress.md 포맷이 phase1 규격과 다름 |
| V5=3 (unpaired만) | 접미 규칙이 실코드 명명과 불일치 | `pair_overrides` 대량 필요 or 접미 휴리스틱 폐기 검토 |
| V11=4 ([RN] 21+) | 가정 어긋남이 많음 | [LOCAL] 목록으로 원인 분류 |

**중요**: `unpaired`가 많이 나와도 **버그가 아니다.** TX_SWAP_REQ처럼 응답 없는 설계가 섞여 있는
게 정상이다. [LOCAL] 목록을 보고 응답 없는 심볼을 `flow_pairing.json`의 `no_reply_symbols`에
선언하면 사라진다. 선언 전에는 결손으로 판정되지 않고 검토 항목으로만 남는다.
