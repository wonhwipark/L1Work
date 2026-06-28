# 5.0 Common Automation Framework

**Status:** Topic04 S3~S4 Common Framework 확정안  
**Target Version:** v0.38 candidate  
**Scope:** 5.1~5.6 prompt 공통 적용 원칙  

---

## 5.0 Purpose

5.0 Common Automation Framework는 5.1~5.6 개별 구현 프롬프트가 동일한 철학과 절차를 공유하도록 정의하는 공통 기준이다.

Topic04의 목적은 단순히 개별 구현 프롬프트를 작성하는 것이 아니라 아래 계층을 확립하는 것이다.

```text
Automation Philosophy
        ↓
Common Framework
        ↓
Individual Prompt
```

개별 항목 상세화는 다음 Step에서 진행한다.

---

## Engineering Philosophy

5.x prompt 전체는 다음 Engineering Philosophy를 따른다.

```text
Environment First
Capability First
Proposal First
Open-source First
Battle-tested First
Simplicity First
```

---

## 5.0.1 Environment Discovery

### Principle

```text
Assume Nothing
```

### Goal

실제 구현 전에 현재 실행 환경을 최대한 조사한다.

### Discovery Targets

```text
OS
Python
Node
Git
Workspace structure
SQLite
PlantUML
Pydantic
MCP
Jira
Confluence
Existing packages
Claude Code
Roo Code
```

### Rule

구현자는 현재 환경을 확인하지 않은 상태에서 특정 도구, 패키지, schema, 저장소 구조를 강제하지 않는다.

---

## 5.0.2 Capability Discovery

### Principle

```text
Use Existing Capability First
```

### Goal

현재 환경에서 이미 사용 가능한 기능을 먼저 확인한다.

### Discovery Questions

```text
Can SQLite be used?
Can Markdown files be used?
Can JSON files be used?
Can YAML files be used?
Can PlantUML be generated?
Can REST API be used?
Can MCP be used?
Can GitHub be used?
Can Perforce be used?
Can existing scripts be reused?
Can existing prompt policy files be loaded?
```

### Rule

```text
Reuse First
Build Last
```

---

## 5.0.3 Proposal First

### Principle

큰 방향은 다음 주체가 결정한다.

```text
User + GPT
```

세부 구현은 다음 주체가 담당한다.

```text
Claude Code
Roo Code
```

### User + GPT Scope

```text
Automation purpose
Workflow direction
High-level architecture
Input/output direction
Schema direction
Success criteria
Dry-run criteria
Boundary between 5.x items
```

### Claude Code / Roo Code Scope

```text
Environment investigation
Capability investigation
Implementation method selection
Dependency selection
Detailed package structure
Detailed schema adjustment
Test method
Dry-run implementation
Implementation notes
```

### Rule

Claude Code / Roo Code는 GPT + 사용자가 정한 큰 방향을 임의로 변경하지 않는다. 필요한 변경이 있으면 제안 형식으로 분리한다.

---

## 5.0.4 Adaptive Schema

### Principle

환경에 맞게 적응하되, 가능한 경우 오픈소스 기반의 검증된 안정적이고 운영 효율이 높은 방식을 우선 제안한다.

### Selection Priority

```text
1. Open-source and widely adopted
2. Proven stability in real projects
3. Efficient for long-term operation
4. Easy to maintain and inspect
```

### Design Principles

```text
Do not invent new frameworks.
Prefer mature and battle-tested solutions.
Avoid unnecessary complexity.
Favor simplicity over novelty.
```

### Candidate Storage Schema

#### Tier 1 Recommended

```text
SQLite
Markdown + Index
```

#### Tier 2

```text
YAML
JSON
```

### Validation Layer

Storage schema와 validation layer는 분리한다.

```text
Pydantic
Dataclass
```

Pydantic과 Dataclass는 저장소 후보가 아니라 schema validation, type safety, data structure definition을 위한 검증/구조화 레이어로 본다.

---

## 5.0.5 Implementation

### Principle

```text
Prefer Existing Environment
```

### Owner

```text
Claude Code
Roo Code
```

### Rule

새로운 패키지 설치보다 현재 환경에서 이미 가능한 구현 방식을 우선한다.  
단, 장기 운영 효율이 명확히 높고 환경상 설치가 가능한 경우에는 제안 후 적용한다.

---

## 5.0.6 Feedback Loop

### Principle

결함, 개선점, 운영 중 발견사항은 다음 실행에 재사용 가능한 형태로 축적한다.

### Flow

```text
Defect
↓
Skill Update
↓
Knowledge DB Update
↓
Prompt Update
↓
Reuse
```

### Rule

Workflow 실행 결과는 일회성 산출물로 끝나지 않고 Skill, Knowledge DB, Prompt 개선 후보로 연결되어야 한다.

---

## 5.0.7 Continuous Improvement

### Long-term Targets

```text
Skill DB
Knowledge DB
Pattern Library
RCA History
Index System
```

### Rule

5.x prompt는 단기 자동화뿐 아니라 장기적으로 반복 가능한 조직 Knowledge 축적 구조로 확장 가능해야 한다.

---

## 5.0.8 Artifact Management

### Principle

```text
Overwrite prohibited
```

반복 실행 시 이전 산출물이 덮어써지면 추적, 비교, RCA, Knowledge DB 연결이 어려워진다. 모든 실행 결과는 timestamp 기반 run folder에 저장한다.

### Base Directory

모든 5.x prompt의 artifact 기준 경로는 단일 환경 변수로 정의한다.

```text
ARTIFACTS_BASE_DIR = %USERPROFILE%\artifacts
```

각 5.x prompt 구현체의 `config.py`는 이 기본값을 사용하며, 사용자가 환경 변수 또는 CLI 옵션으로 재정의할 수 있도록 한다.

예외: Discovery Strategy Profile(`child_page_discovery_profile.json`)은 실행 결과가 아닌 방법 메모리이므로 timestamp 없는 고정 파일명을 사용하며 overwrite를 허용한다.

```text
%USERPROFILE%\artifacts\child_page_discovery_profile.json
```

### Timestamp Format

```text
YYYYMMDD_HHMM_KST
```

### Directory Rule

```text
%USERPROFILE%\artifacts\

run_<timestamp>\

    artifact1
    artifact2
    ...
```

### Naming Rule

```text
<artifact_name>_<timestamp>.<ext>
```

### Example

```text
%USERPROFILE%\artifacts\

run_20260616_0215_KST\

    analysis_report_20260616_0215_KST.md
    gap_report_20260616_0215_KST.md
    callflow_20260616_0215_KST.puml
```

### Rule

각 5.x prompt는 산출물 위치와 파일명을 명시해야 한다.  
반복 실행을 전제로 하며, overwrite는 금지한다. (Discovery Profile 제외)

---

## 5.0.9 Layered Architecture

### Principle

정책, 실행, 산출물, 장기 지식을 분리한다.

### Architecture

```text
Skill Layer
        ↓
Workflow Layer
        ↓
Artifact Layer
        ↓
Knowledge Layer
```

### Ownership

#### Skill Layer

```text
Policy Owner
```

예:

```text
Critical Defect Rule
Code Review Rule
Naming Rule
Priority Rule
HLD Rule
Weekly Report Rule
```

#### Workflow Layer

```text
Policy Consumer
```

예:

```text
5.1 Jira Feedback Loop
5.2 Code Analyzer
5.3 Weekly Report Collection
5.4 HLD-Code Consistency
5.5 RCA Knowledge Graph
5.6 Onboarding Knowledge Pack
```

#### Artifact Layer

```text
Execution History
```

#### Knowledge Layer

```text
Long-term Memory
```

예:

```text
Skill DB
Knowledge DB
Pattern Library
RCA History
Index System
```

### Rule

Workflow modules are policy consumers, not policy owners.

---

## 5.0.10 Skill Loading Strategy

### Principle

```text
Workflow modules shall not own policies.
Policies shall be loaded dynamically from prompt policy files.
```

### Architecture

```text
Skill Layer
        ↓
Skill Loader
        ↓
Workflow Layer
        ↓
Artifact Layer
        ↓
Knowledge Layer
```

### Search Order

```text
Branch Skill
    ↓
Repository Skill
    ↓
Common Prompt Policy
    ↓
Default Prompt
```

### Recommended Skill Format

#### Tier 1

```text
Markdown
```

Markdown은 AI 친화적이고 사람이 읽기 쉬우며 diff 관리가 쉽기 때문에 기본 prompt policy 형식으로 적합하다.

#### Tier 2

```text
YAML
```

YAML은 구조화된 rule, priority, mapping이 필요한 경우에 사용한다.

#### Tier 3

```text
JSON
```

JSON은 기계 처리 중심의 schema 또는 API payload에 사용한다.

### Discovery Targets

```text
.roo/skills exists?
.claude/skills exists?
common prompt policy files exist?
branch-specific prompt policy files exist?
markdown/yaml/json loading possible?
recursive search possible?
merge/fallback/cache possible?
```

### Rule

Team-defined prompt policies are authoritative.  
5.x workflow는 team prompt 정책을 따르며 defect 기준, priority 기준, review 기준 등을 내부에 hardcode하지 않는다.

---

## Deferred to Next Step

다음 Step에서 아래 개별 구현 프롬프트를 5.0 Common Automation Framework에 맞게 상세화한다.

```text
5.1 Jira Feedback Loop
5.2 Code Analyzer
5.3 Weekly Report Collection
5.4 HLD-Code Consistency
5.5 RCA Knowledge Graph
5.6 Onboarding Knowledge Pack
```
