# issue_type seeds

issue_type별 단서 부품. P3(issue_type 추천), P4(정상경로 대조·required evidence), P5(자가점검)에서 참조한다.

각 seed: Trigger Signatures(분석 시작 단서), Required Evidence(반드시 확인할 항목), 정상경로 대비 이탈 지점.

```text
rach_failure_analyzer.md          RACH 실패
scg_failure_analyzer.md           SCG 실패
tx_abnormal_analyzer.md           TX abnormal
l2_max_retransmission_analyzer.md L2 max retransmission
```

crash/dump는 5.5 RCA KG 대상이 아니다(L1SW Log Analyzer 전담). crash seed는 의도적으로 포함하지 않는다. 원본 패키지의 `rca_kg/skills_seed/`는 SSOT로 유지되며, 이 폴더는 스킬 사용을 위한 흡수본이다.
