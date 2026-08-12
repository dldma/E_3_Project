# 03. data.json 분석 모드

## 목적

`data.json`에서 5×5, 13×13, 25×25 필터 및 패턴을 불러와 각 테스트 케이스를 자동으로 판정합니다.

## 실행

```bash
python3 main.py
```

프로그램 실행 후 `2`를 선택합니다.

```text
[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
선택: 2
```

## data.json 구성

필터는 크기별로 다음 구조를 가집니다.

```text
filters
├── size_5
│   ├── cross
│   └── x
├── size_13
│   ├── cross
│   └── x
└── size_25
    ├── cross
    └── x
```

패턴은 다음 규칙으로 구성했습니다.

```text
size_{N}_{idx}
```

현재 구성은 각 크기에 Cross/X 패턴을 하나씩 두어 총 6개의 테스트 케이스를 분석하도록 되어 있습니다.

```text
size_5_1
size_5_2
size_13_1
size_13_2
size_25_1
size_25_2
```

## 라벨 정규화

`data.json`의 외부 표현은 다음과 같이 내부 표준 라벨로 변환합니다.

```text
expected "+"  → Cross
expected "x"  → X
filter "cross" → Cross
filter "x"     → X
```

판정 및 PASS/FAIL 비교는 정규화가 끝난 `Cross`, `X`를 기준으로 수행합니다.

## 패턴 크기 선택

예를 들어 다음 패턴 키가 있다면,

```text
size_13_2
```

키에서 `13`을 추출하여 다음 필터 그룹을 선택합니다.

```text
filters["size_13"]
```

## 크기 및 스키마 검증

MAC 계산 전에 다음 항목을 확인합니다.

- 해당 크기의 필터가 존재하는지
- Cross 필터와 X 필터가 모두 존재하는지
- `input`과 `expected`가 존재하는지
- 패턴이 N×N인지
- 필터가 N×N인지
- expected 라벨을 정상적으로 정규화할 수 있는지

문제가 있는 케이스는 프로그램 전체를 종료하지 않고 해당 케이스만 FAIL 처리하도록 구성했습니다.

## 스크린샷

### Screenshot 04 — 필터 로드 완료

다음 세 줄이 모두 보이도록 캡처합니다.

```text
✓ size_5 필터 로드 완료 (Cross, X)
✓ size_13 필터 로드 완료 (Cross, X)
✓ size_25 필터 로드 완료 (Cross, X)
```

권장 파일명:

```text
docs/images/04_filter_load.png
```

![필터 로드](images/04_filter_load.png)

### Screenshot 05 — PASS 판정 로그

5×5, 13×13, 25×25 중 여러 크기의 테스트 케이스가 보이도록 캡처합니다.

각 케이스에서 다음 항목이 확인되어야 합니다.

```text
Cross 점수: ...
X 점수: ...
판정: ... | expected: ... | PASS
```

가능하면 5×5 / 13×13 / 25×25가 모두 포함되도록 캡처합니다.

권장 파일명:

```text
docs/images/05_json_pass_cases.png
```

![JSON PASS 케이스](images/05_json_pass_cases.png)

> 단순 명령어 오타, 잘못된 실행 위치 등 구현과 관계없는 실패 로그는 제출용 문서에 포함하지 않습니다.
