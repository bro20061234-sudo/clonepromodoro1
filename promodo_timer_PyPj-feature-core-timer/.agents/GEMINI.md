# Pomodoro Timer – AI Agent Rules

## Project Overview

Đây là một ứng dụng **Pomodoro Timer** desktop, xây dựng bằng **Python + CustomTkinter**.
Dự án được phát triển bởi **team 3 người**, mỗi người phụ trách một module độc lập.

---

## Tính năng

- ⏱️ Đồng hồ Pomodoro: Work / Short Break / Long Break
- ▶️ Start / Pause / Resume / Reset
- ⚙️ Cài đặt thời lượng phiên học
- 🔊 Nhạc nền + âm thanh thông báo
- 🎵 Chọn playlist hoặc file nhạc
- 🔔 Desktop notification khi hết phiên
- 🌙 Dark / Light mode
- 📅 Lịch sử học tập

---

## Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter
- **Audio**: pygame (nhạc nền) + plyer (notification)
- **Data Storage**: JSON (lịch sử phiên — đơn giản, không dùng DB)
- **Package Manager**: pip + `requirements.txt`
- **Version Control**: Git
- **Testing**: pytest

---

## Phân chia công việc

### 👤 Người 1 — GUI chính (`src/ui/` — phần chính)
- Thiết kế cửa sổ chính (`main_window.py`)
- Hiển thị đồng hồ + animation (`timer_widget.py`)
- Dark / Light mode (`theme.py`)
- Kết nối giao diện với Core

**Khối lượng:** ~35%

### 👤 Người 2 — Core / Logic (`src/core/`)
- Logic đếm ngược, chuyển pha Work/Break (`timer.py`)
- Phát nhạc nền, âm thanh (`music_player.py`)
- Desktop notification (`notification.py`)

**Khối lượng:** ~35%

### 👤 Người 3 — Settings + Music UI + History
- Form cài đặt thời lượng (`src/ui/settings_panel.py`)
- UI chọn nhạc, playlist (`src/ui/music_panel.py`)
- Lưu và hiển thị lịch sử phiên (`src/core/history.py`)

**Khối lượng:** ~30%

---

## Project Structure

```
promodo_timer_PyPj/
├── main.py                     # Entry point – khởi tạo và kết nối các module
├── requirements.txt
├── README.md
├── GEMINI.md                   # AI rules (file này)
├── POMODORO_TASK_DIVISION.md   # Bảng phân chia task chi tiết
│
├── data/
│   └── history.json            # Lịch sử phiên (tự sinh, không commit)
│
├── assets/
│   ├── icons/
│   ├── sounds/                 # File âm thanh notification
│   └── music/                  # Nhạc nền
│
├── .agents/
│   ├── hooks.json
│   ├── rules/
│   └── skills/
│
├── src/
│   ├── core/                   # 👤 Người 2 (+ history của Người 3)
│   │   ├── timer.py            # Logic Pomodoro – State machine
│   │   ├── music_player.py     # Phát nhạc nền (pygame)
│   │   ├── notification.py     # Desktop notification (plyer)
│   │   └── history.py          # Lưu/đọc lịch sử phiên (JSON) – Người 3
│   │
│   └── ui/                     # 👤 Người 1 (main_window, timer_widget, theme)
│       ├── main_window.py      # Cửa sổ chính – Người 1
│       ├── timer_widget.py     # Đồng hồ + nút điều khiển – Người 1
│       ├── theme.py            # Dark/Light mode constants – Người 1
│       ├── settings_panel.py   # Form cài đặt – Người 3
│       └── music_panel.py      # UI chọn nhạc – Người 3
│
└── tests/
    ├── test_timer.py
    ├── test_history.py
    └── test_music_player.py
```

---

## Architecture Rules

- **Người 1 (UI)**: KHÔNG chứa business logic. Chỉ hiển thị và nhận sự kiện.
- **Người 2 (Core)**: KHÔNG import từ `src/ui/`.
- **Người 3**: `history.py` nằm trong `src/core/` nhưng KHÔNG import từ `src/ui/`.
  `settings_panel.py` và `music_panel.py` nằm trong `src/ui/` nhưng KHÔNG chứa logic.
- `main.py` là nơi **DUY NHẤT** kết nối các module.

### Timer
- Chỉ dùng `after(1000, callback)` trong UI thread. Tuyệt đối không dùng `time.sleep()`.
- State machine Pomodoro nằm hoàn toàn trong `src/core/timer.py`.

---

## Coding Standards

- Follow **PEP 8**. Max line length: **100 characters**.
- Dùng **type hints** cho tất cả function signatures.
- Dùng **f-strings**.
- Mọi public class/function phải có **docstring** (Google style).
- Không dùng `global` variables.

### Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Variables, functions, modules | `snake_case` | `start_timer()` |
| Classes | `PascalCase` | `TimerWidget` |
| Constants | `SCREAMING_SNAKE_CASE` | `DEFAULT_WORK_DURATION = 25` |
| Private methods/attrs | `_single_underscore` | `_tick()` |

---

## Git Workflow

- Branch theo người + tính năng: `feature/gui-timer`, `feature/core-timer`, `feature/settings-history`
- Commit messages theo **Conventional Commits**: `feat:`, `fix:`, `chore:`, `docs:`, `test:`
- Chạy `pytest tests/` trước khi push.
- Không commit trực tiếp vào `main`. Dùng Pull Requests.

---

## AI Agent Instructions

### 🔴 BẮT BUỘC – Đầu mỗi hội thoại mới

Trước khi làm bất cứ việc gì, AI agent PHẢI thực hiện và xác nhận 2 bước sau:

```powershell
# Bước 1 – Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Bước 2 – Lấy code mới nhất từ GitHub
git pull origin main
```

- Nếu `hooks.json` đã tự chạy → kiểm tra output và thông báo kết quả cho người dùng.
- Nếu chưa tự chạy → nhắc người dùng chạy 2 lệnh trên trước khi tiếp tục.
- Nếu `git pull` báo **CONFLICT** → hướng dẫn resolve conflict trước, không làm gì khác.

Chi tiết đầy đủ: **`.agents/rules/session_startup.md`**

---

### Các quy tắc khác

- Trước khi gợi ý lệnh build/run, **đọc `.agents/skills/`**.
- Khi tạo file mới, đặt đúng vào thư mục của người phụ trách theo bảng trên.
- Khi fix bug, luôn tạo hoặc update test tương ứng trong `tests/`.
- Khi thêm dependency mới vào `requirements.txt`, giải thích rõ lý do.
- Khi hỏi về một tính năng, xác định rõ nó thuộc module của **ai** trước khi viết code.
