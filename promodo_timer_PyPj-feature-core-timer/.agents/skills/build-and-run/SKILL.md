---
name: build-and-run
description: >-
  Skill for building, running, and testing the Pomodoro Timer app. Use this
  skill when asked to run the app, run tests, check code quality, or package
  the app into an executable.
---

# Build & Run – Pomodoro Timer

---

## Cài đặt dependencies

> **Chạy ở đâu:** PowerShell (đã activate `.venv`), trong thư mục dự án.

```powershell
pip install -r requirements.txt
```

---

## Chạy app

```powershell
python main.py
```

> ⚠️ App đang ở dạng skeleton — sẽ báo `NotImplementedError` cho đến khi từng người implement `TODO` trong module của mình.

---

## Chạy tests

```powershell
# Toàn bộ tests
pytest tests/ -v

# Theo module
pytest tests/test_timer.py -v         # Core – Người 2
pytest tests/test_history.py -v       # History – Người 3
pytest tests/test_music_player.py -v  # Music – Người 2
```

Chạy với coverage report:

```powershell
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Kiểm tra code quality

```powershell
# Cài tools nếu chưa có
pip install flake8 black isort

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint (max line 100)
flake8 src/ tests/ --max-line-length=100
```

---

## Đóng gói thành EXE (PyInstaller)

```powershell
pip install pyinstaller

pyinstaller --onefile --windowed `
  --name "PomodoroTimer" `
  --add-data "assets;assets" `
  --add-data "data;data" `
  main.py
```

Output EXE sẽ ở thư mục `dist/`.

---

## Bảng lệnh nhanh

| Task | Command |
|---|---|
| Chạy app | `python main.py` |
| Chạy tất cả test | `pytest tests/ -v` |
| Test với coverage | `pytest tests/ --cov=src` |
| Format code | `black src/ tests/` |
| Lint | `flake8 src/ tests/ --max-line-length=100` |
| Build EXE | `pyinstaller --onefile --windowed --name PomodoroTimer main.py` |
