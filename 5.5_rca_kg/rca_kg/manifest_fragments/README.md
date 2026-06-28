# manifest_fragments

갱신: 2026-06-27 12:21 KST

이 폴더는 P2가 생성하는 L1SW manifest fragment 후보 JSON의 저장 위치다.

예상 산출물:

```text
{kg_root}/manifest_fragments/rca_rach.json
{kg_root}/manifest_fragments/rca_scg.json
{kg_root}/manifest_fragments/rca_tx.json
{kg_root}/manifest_fragments/rca_l2.json
```

이 파일들은 candidate 산출물이다. 사내 L1SW manifest 디렉토리에 반영하기 전 review log의 구조 일치 여부를 확인한다.

일반 사용자는 이 폴더를 직접 수정하지 않는다.
