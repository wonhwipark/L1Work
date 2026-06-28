# root-cause-analyzer references index

갱신: 2026-06-27 12:21 KST

이 파일은 설치 검증용 참조 인덱스다. `install_skill.ps1`과 `validate_install.ps1`은 `skill_manifest.yaml`의 필수 파일 목록에 따라 이 파일이 함께 설치됐는지 확인한다.

## Reference files

- `p0_env_probe.md`
- `c0_secure_l1sw.md`
- `p1_format_probe.md`
- `p2_manifest_fragments.md`
- `p3_signal.md`
- `p4_rca_and_case.md`
- `p5_review.md`
- `p6_keywords_promote.md`
- `methodology.md`
- `seeds/README.md`

## v0.21 path policy

- `workspace_root` = RCA_standalone 패키지 루트.
- `kg_root` = 누적 RCA KG 저장소.
- P1~P6 runtime 산출물은 `{kg_root}` 아래에 저장한다.
