# ⏱️ FocusWatch

> 작업 중인 창을 자동으로 감지하여 실제 집중 시간만 측정하는 스마트 타이머

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-UI_Framework-41CD52?style=flat-square&logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 프로젝트 소개

**FocusWatch**는 컴퓨터 작업 중 실제로 집중한 시간만 정확하게 측정해주는 생산성 도구입니다.

기존 타이머 앱과 달리, FocusWatch는 **현재 포커스된 창이 등록된 작업 목록에 있는 경우에만** 시간을 카운트합니다. SNS, 유튜브 등 딴짓을 하는 동안에는 타이머가 멈추기 때문에, 순수하게 작업에 투자한 시간을 파악할 수 있습니다.

---

## ✨ 주요 특징 (Key Features)

- **🎯 스마트 집중 감지** — 활성 창을 1초마다 감지하여, 등록된 앱에 포커스가 있을 때만 경과 시간을 누적
- **🔴 시각적 상태 표시** — 집중 중일 때는 타이머가 빨간색, 이탈 중일 때는 흰색으로 전환되어 상태를 직관적으로 확인
- **📋 최대 3개 앱 등록** — 여러 작업 도구(IDE, 문서 편집기, 터미널 등)를 동시에 등록하여 유연하게 추적
- **🪟 항상 위 투명 오버레이** — 반투명 플로팅 위젯이 화면 위에 항상 표시되어 작업 흐름을 방해하지 않음
- **⌨️ 키보드 단축키 지원** — 마우스 없이도 타이머 정지/초기화 가능 (Windows/macOS 각각 지원)
- **🔄 실시간 프로세스 목록 갱신** — 현재 실행 중인 모든 창 목록을 즉시 새로고침

---

## 🛠️ 기술 스택 (Tech Stack)

| 분류 | 기술 |
|------|------|
| Language | Python 3.x |
| UI Framework | PyQt6 |
| UI 테마 | qt-material |
| 창 감지 | pygetwindow |
| 패키징 | PyInstaller (선택) |

---

## 🚀 시작하기 (Getting Started)

### 필수 조건

- Python 3.8 이상
- pip 패키지 매니저

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/focuswatch.git
cd focuswatch

# 2. 가상환경 생성 (권장)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. 의존성 설치
pip install PyQt6 qt-material pygetwindow
```

### 실행

```bash
python gui.py
```

---

## 📖 사용법 (Usage)

### 1단계 — 작업 앱 등록

1. 앱 실행 후 메인 패널에서 드롭다운 목록을 클릭합니다.
2. 현재 실행 중인 창 목록이 표시됩니다. (최대 3개 등록 가능)
3. 추적할 창을 선택하면 리스트에 추가됩니다.
4. 목록에서 항목을 **우클릭**하면 삭제할 수 있습니다.

> 💡 목록이 최신 상태가 아닐 경우, 🔄 **새로고침 버튼**을 눌러 업데이트하세요.

### 2단계 — 타이머 시작

▶ **시작 버튼**을 누르면 메인 패널이 숨겨지고 반투명 오버레이 타이머가 화면 위에 표시됩니다.

```
등록된 앱이 포커스 됨  →  타이머 🔴 빨간색 (카운트 중)
다른 창으로 이동       →  타이머 ⚪ 흰색   (일시 정지)
```

### 3단계 — 타이머 제어 (단축키)

| 동작 | Windows | macOS |
|------|---------|-------|
| 타이머 정지 & 메인 패널 복귀 | `Ctrl + S` | `Cmd + S` |
| 타이머 초기화 (0으로 리셋) | `Ctrl + R` | `Cmd + R` |

### 오버레이 이동

오버레이 창을 **드래그**하여 화면 원하는 위치에 자유롭게 배치할 수 있습니다.

---

## 📁 프로젝트 구조

```
focuswatch/
├── gui.py              # 메인 애플리케이션 (UI + 로직)
├── resources/
│   ├── style.css       # 커스텀 스타일시트
│   ├── play.svg        # 시작 버튼 아이콘
│   └── refresh.svg     # 새로고침 버튼 아이콘
└── README.md
```

---

## ⚠️ 알려진 제한 사항

- 최대 **3개**의 앱만 동시에 등록할 수 있습니다.
- `pygetwindow`의 특성상, 일부 시스템에서 창 제목이 다르게 표시될 수 있습니다.
- macOS에서는 접근성 권한 허용이 필요할 수 있습니다.

---

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 배포됩니다.
