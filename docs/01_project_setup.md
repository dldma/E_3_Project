# 01. 프로젝트 및 Git 연결 확인

## 목적

GitHub의 `E_3_Project` 저장소를 WSL Ubuntu 환경의 로컬 프로젝트와 연결하고 정상적으로 작업할 수 있는 상태인지 확인했습니다.

## 확인 명령어

```bash
git remote -v
git branch --show-current
```

정상 확인 결과의 핵심은 다음과 같습니다.

```text
origin  https://github.com/dldma/E_3_Project.git (fetch)
origin  https://github.com/dldma/E_3_Project.git (push)
main
```

`origin`이 GitHub의 `E_3_Project` 저장소를 가리키고 있으며 현재 작업 브랜치는 `main`입니다.

## 최종 프로젝트 파일

```text
E_3_Project/
├── main.py
├── data.json
├── README.md
└── docs/
```

## 스크린샷

### Screenshot 01 — GitHub 저장소 화면

GitHub의 `dldma/E_3_Project` 저장소 화면에서 저장소 이름과 `main.py`, `data.json`, `README.md` 파일이 보이도록 캡처합니다.

권장 파일명:

```text
docs/images/01_github_repository.png
```

![GitHub 저장소](images/01_github_repository.png)

### Screenshot 02 — Git 연결 확인

터미널에서 아래 명령어와 정상 출력이 한 화면에 보이도록 캡처합니다.

```bash
git remote -v
git branch --show-current
```

반드시 보이면 좋은 부분:

```text
origin  https://github.com/dldma/E_3_Project.git
main
```

권장 파일명:

```text
docs/images/02_git_connection.png
```

![Git 연결 확인](images/02_git_connection.png)

> 명령어를 잘못 입력하여 발생한 오류나 프로젝트 구현과 관계없는 터미널 오류는 캡처에 포함하지 않습니다.
