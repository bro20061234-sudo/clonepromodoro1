---
name: setup-dev-environment
description: >-
  Hướng dẫn từng bước để setup môi trường phát triển Pomodoro Timer trên máy mới.
  Dùng skill này khi thành viên hỏi cách setup dự án, cài dependencies, hoặc chạy app lần đầu.
---

# Setup Dev Environment – Pomodoro Timer

> Làm đúng thứ tự. Tất cả lệnh chạy trong **Windows PowerShell**.

---

## Bước 1 – Kiểm tra Python và Git

```powershell
python --version   # Cần 3.10 trở lên
git --version
```

- Python chưa cài: https://www.python.org/downloads/ (tích **"Add Python to PATH"**)
- Git chưa cài: https://git-scm.com/download/win

---

## Bước 2 – Clone dự án

```powershell
git clone https://github.com/MiKuwu/promodo_timer_PyPj.git
cd promodo_timer_PyPj
```

> Từ đây trở đi, **tất cả lệnh chạy trong thư mục `promodo_timer_PyPj`**.

---

## Bước 3 – Tạo môi trường ảo (một lần duy nhất)

```powershell
python -m venv .venv
```

---

## Bước 4 – Kích hoạt môi trường ảo

```powershell
.\.venv\Scripts\Activate.ps1
```

Kiểm tra: dòng nhắc phải có `(.venv)` ở đầu.

Nếu bị lỗi execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

> ✅ **Tự động hóa**: Antigravity AI tự chạy bước này mỗi khi mở dự án qua `hooks.json`.

---

## Bước 5 – Cài thư viện

```powershell
pip install -r requirements.txt
```

Thư viện cần thiết: `customtkinter`, `pygame`, `plyer`, `pytest`

---

## Bước 6 – Mở trong Antigravity

**Antigravity 2.0**: Sidebar → Projects → + Add Project → chọn thư mục `promodo_timer_PyPj`

**Antigravity IDE**: File → Open Folder → chọn thư mục `promodo_timer_PyPj`

AI tự đọc `GEMINI.md` và `.agents/` → sẵn sàng hỗ trợ ngay.

---

## Bước 7 – Chạy test

```powershell
pytest tests/ -v
```

---

## Troubleshooting

| Lỗi | Cách sửa |
|---|---|
| `'python' is not recognized` | Cài lại Python, tích "Add to PATH" |
| `'git' is not recognized` | Cài Git tại git-scm.com |
| `cannot be loaded because running scripts is disabled` | Chạy `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `ModuleNotFoundError: customtkinter` | Activate `.venv` rồi `pip install -r requirements.txt` |
| Không thấy `(.venv)` ở đầu dòng | Chưa activate — chạy `.\.venv\Scripts\Activate.ps1` |
