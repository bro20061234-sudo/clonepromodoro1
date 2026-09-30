# Pomodoro Timer – AI Agent Rules

## Project Overview

Đây là một ứng dụng **Pomodoro Timer** desktop hoàn chỉnh, xây dựng bằng **Python + CustomTkinter**.
Dự án được phát triển bởi **team 3 người**, mỗi người phụ trách một module độc lập.

---

## Tính năng đầy đủ

- ⏱️ Đồng hồ Pomodoro: Work / Short Break / Long Break
- ▶️ Start / Pause / Resume / Reset
- ⚙️ Cài đặt thời lượng phiên học
- 🔊 Nhạc nền + âm thanh thông báo
- 🎵 Chọn playlist hoặc file nhạc
- 📊 Thống kê số phiên đã hoàn thành
- 📅 Lịch sử học tập
- 🚫 Chặn ứng dụng gây sao nhãng (Discord, Steam, game, mạng xã hội...)
- 🔔 Desktop notification khi hết phiên
- 🌙 Dark / Light mode
- 💾 Lưu cấu hình người dùng (JSON/SQLite)
- 📈 Dashboard thống kê thời gian tập trung

---

## Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter
- **Audio**: pygame (nhạc nền) + playsound / winsound (notification sound)
- **Data Storage**: SQLite (lịch sử, thống kê) + JSON (cấu hình người dùng)
- **Process Management**: psutil (chặn app)
- **Notifications**: plyer
- **Charts**: matplotlib (dashboard)
- **Package Manager**: pip + `requirements.txt`
- **Version Control**: Git
- **Testing**: pytest

---

## Phân chia công việc theo người

### 👤 Người 1 – GUI (`src/ui/`)
- Thiết kế giao diện tổng thể
- Timer display + animation
- Settings panel
- Dark / Light mode
- Tích hợp các widget từ Core và Focus Mode

### 👤 Người 2 – Core (`src/core/`)
- Logic Pomodoro (đếm giờ, chuyển pha)
- Music player (phát nhạc nền, chọn file)
- Desktop notification
- Lưu/đọc dữ liệu (SQLite + JSON)
- Thống kê phiên học

### 👤 Người 3 – Focus Mode (`src/focus/`)
- Phát hiện và chặn process (psutil)
- Quản lý danh sách app cần block
- Whitelist / Blacklist
- Dashboard thống kê thời gian tập trung (matplotlib)

---

## Project Structure

```
promodo_timer_PyPj/
├── main.py                     # App entry point – khởi tạo và kết nối các module
├── requirements.txt
├── README.md
├── GEMINI.md                   # AI rules (file này)
├── config/
│   └── user_settings.json      # Cấu hình người dùng (tự sinh, không commit)
├── assets/
│   ├── sounds/                 # File âm thanh notification
│   └── music/                  # Nhạc nền mặc định
├── .agents/
│   ├── rules/
│   └── skills/
│
├── src/
│   │
│   ├── ui/                     # 👤 Người 1 – GUI
│   │   ├── __init__.py
│   │   ├── main_window.py      # Cửa sổ chính, layout tổng thể
│   │   ├── timer_widget.py     # Widget hiển thị đồng hồ + animation
│   │   ├── settings_panel.py   # Panel cài đặt thời lượng, theme
│   │   ├── music_panel.py      # UI chọn nhạc, playlist
│   │   └── theme.py            # Dark/Light mode constants
│   │
│   ├── core/                   # 👤 Người 2 – Core
│   │   ├── __init__.py
│   │   ├── timer.py            # Logic Pomodoro (trạng thái, đếm giờ, chuyển pha)
│   │   ├── music_player.py     # Phát nhạc nền, quản lý playlist
│   │   ├── notification.py     # Desktop notification khi hết phiên
│   │   ├── settings.py         # Đọc/ghi cấu hình JSON
│   │   └── database.py         # SQLite: lưu lịch sử và thống kê phiên
│   │
│   └── focus/                  # 👤 Người 3 – Focus Mode
│       ├── __init__.py
│       ├── blocker.py          # Phát hiện và kill/block process
│       ├── app_list.py         # Quản lý whitelist/blacklist app
│       └── dashboard.py        # Vẽ biểu đồ thống kê (matplotlib)
│
└── tests/
    ├── test_timer.py           # Test core/timer.py
    ├── test_settings.py        # Test core/settings.py
    ├── test_database.py        # Test core/database.py
    ├── test_blocker.py         # Test focus/blocker.py
    └── test_app_list.py        # Test focus/app_list.py
```

---

## Architecture Rules

### Nguyên tắc tổng quát
- **Người 1 (UI)** KHÔNG được chứa business logic. Chỉ hiển thị và nhận sự kiện.
- **Người 2 (Core)** KHÔNG import từ `src/ui/` hoặc `src/focus/`.
- **Người 3 (Focus)** KHÔNG import từ `src/ui/`. Có thể import từ `src/core/database.py` để lưu thống kê.
- `main.py` là nơi DUY NHẤT kết nối cả 3 module lại với nhau.

### Giao tiếp giữa các module
- UI gọi Core thông qua **callback functions** hoặc **event binding** – không giữ reference trực tiếp.
- Tránh circular import. Dùng dependency injection khi cần.

### Timer
- Chỉ dùng `after(1000, callback)` của tkinter/CTk để cập nhật timer trong UI. Tuyệt đối không dùng `time.sleep()` trong UI thread.
- State machine của Pomodoro phải nằm hoàn toàn trong `src/core/timer.py`.

---

## Coding Standards

- Follow **PEP 8**.
- Maximum line length: **100 characters**.
- Dùng **type hints** cho tất cả function signatures.
- Dùng **f-strings** (không dùng `.format()` hay `%`).
- Mọi public class và function đều phải có **docstring** (Google style).
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

- Branch theo người + tính năng: `feature/gui-timer-animation`, `feature/core-music-player`, `feature/focus-blocker`
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
- Khi tạo file mới, đặt đúng vào thư mục của người phụ trách (ui / core / focus).
- Khi fix bug, luôn tạo hoặc update test tương ứng trong `tests/`.
- Khi thêm dependency mới vào `requirements.txt`, giải thích rõ lý do.
- Khi hỏi về một tính năng, xác định rõ nó thuộc module của **ai** (Người 1/2/3) trước khi viết code.
