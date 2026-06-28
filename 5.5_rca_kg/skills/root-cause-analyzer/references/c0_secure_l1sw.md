# C0 — _l1sw.txt 확보 분기

별도 단계라기보다 P0/P1이 쓰는 분기. `_l1sw.txt`가 없을 때만. 목표는 P1에 쓸 `_l1sw.txt` 확보.

current_run.yaml을 읽고 분기:
1. `selected_l1sw_txt`가 있으면 → 존재/크기 확인 후 next_step=P1, NEXT_STEP에 P1 안내.
2. `l1sw_txt_candidates`가 여러 개면 → 번호 목록, 사용자가 번호만 입력 → `selected_l1sw_txt` 저장 → next_step=P1.
3. `selected_l1sw_txt`가 없고 `.sdm` 후보가 있으면 → L1SW parse.ps1 실제 경로 + 후보 .sdm으로 실행 명령 제시. 파라미터명이 확실하면 실행해도 됨. 불확실하면 명령 후보만 제시하고 멈춤. 생성된 `_l1sw.txt` 경로를 `selected_l1sw_txt`에 저장.
4. `.sdm`도 없으면 → next_step=WAIT_INPUT_LOG, NEXT_STEP에 사용자가 배치할 파일 형식·위치 예시.

각 경우 current_run.yaml과 NEXT_STEP_5.5.md 갱신 + 진행줄.
[사람 확인] `_l1sw.txt` 경로가 맞는지만.

주의: RCA는 L1SW를 강제로 자동 실행하지 않는다. 파라미터가 확실할 때만 실행, 아니면 안내.
