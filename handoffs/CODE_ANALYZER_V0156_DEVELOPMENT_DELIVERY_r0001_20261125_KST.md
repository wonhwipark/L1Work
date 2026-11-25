# Code Analyzer v0.15.6 개발 전달 — 2026-11-25 KST

- 기존 Work: L1-WORKSPACE-RAG-20261111-001.
- 대상: `wonhwipark/L1Work/main/code-analyzer_v0_15_6_1125.zip` (development_not_for_deployment).
- 기반: v0.15.5 594,930 B / SHA-256 `61099248ab0a4b2597ca8316e613f5987caaee671d735337eea1e0f70a6c2877`, 기존 ZIP 불변.
- 신규 ZIP: 611,206 B / SHA-256 `bf1f369aed47e75c38fad3061041e720d5497953b0d90bcf4dc2fbf0d97b69ef` / Git blob `c6948d79bcce8910fdaa246095fe2cccc1fe12a5`.
- 변경: VERSION, 릴리스 메타데이터, SKILL.md, install.py, skillsilent manifest의 v0.15.6 정합성. callers/callees에서 실제 소스의 단순 직접 호출 표기 및 caller 경계를 검사; 불충분하면 UNCERTAIN, 기존 구조 근거 유지. 선택적 anchor_kind/source_excerpt. 신규 회귀 13건.
- 실제 GPT 검사: 원본 CRC 220/220 및 manifest 219/219, 새 ZIP CRC 222/222 및 manifest 221/221, 전체 파일 내용 왕복 및 경로 검사 PASS. 격리 Python harness 13/13 PASS (common/run_probe 일부 대역; 전체 패키지 실행 아님). 패키지에 삽입한 helper/test SHA가 격리 시험용 원본과 일치.
- 제한: 기존 v0.15.5 선별 회귀 전체, v0.15.6 전체 회귀·설치 자체검사·독립 리뷰·업무 호스트 G0/실제 Qwen/제품 E2E = NOT_RUN. 로컬 DNS 제한으로 전체 ZIP을 Python 환경에 반입하지 못해 GitHub Base64 경로에서 패키징. 실제 운영 설치·배포·자동 업데이트 금지.
- 직접 호출 표기 확인은 C++ target resolution, 빌드 활성화, 런타임 도달, dispatch/함수 포인터 해석, MSC 실행 순서의 확정이 아님. 복잡한 형태는 UNKNOWN/UNCERTAIN으로 유지하고 현장 결손 실측 후 최소 EXTEND.
- 다음: 업무 호스트 운영과 분리된 격리 환경에서 기존 test_call_edge_coverage_v0155, 신규 test_call_edge_evidence_v0156, test_accuracy_storage_v0146, test_opencode_parallel_v0152 및 설치 self-check 실행. 기존 활성본은 유지; 게이트 통과 후 별도 승인으로 전환 검토.
