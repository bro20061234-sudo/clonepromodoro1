# UI Component Rules

> **Scope**:
> - `src/ui/main_window.py`, `timer_widget.py`, `theme.py` → 👤 **Người 1**
> - `src/ui/settings_panel.py`, `music_panel.py` → 👤 **Người 3**

---

## Framework

- Dùng **CustomTkinter** làm primary UI framework.
- Gọi ở `main.py` khi khởi động:
  ```python
  customtkinter.set_appearance_mode("System")
  customtkinter.set_default_color_theme("blue")
  ```

---

## Quy tắc thiết kế chung

- Mỗi phần UI riêng biệt = một class kế thừa từ widget CTk phù hợp.
- **KHÔNG đặt business logic** bên trong UI class. Gọi methods từ `src/core/` thay vào đó.
- Truyền dependency vào constructor (dependency injection), không import core trực tiếp trong widget.

**Ví dụ đúng:**
```python
class TimerWidget(customtkinter.CTkFrame):
    def __init__(self, master, on_start, on_pause, on_reset, **kwargs):
        super().__init__(master, **kwargs)
        # Nhận callback từ ngoài vào — không tự import PomodoroTimer
```

---

## Người 1 — GUI chính

### `main_window.py`
- Layout tổng thể, khởi tạo tất cả widget con.
- Nhận `timer`, `music_player`, `history` qua constructor.
- Đăng ký callbacks từ timer: `on_tick`, `on_phase_change`.
- Chứa `_schedule_tick()` → gọi `timer.tick()` mỗi 1 giây qua `after(1000)`.

### `timer_widget.py`
- Hiển thị đồng hồ đếm ngược (MM:SS).
- Nút: Start, Pause/Resume, Reset.
- Nhận callbacks: `on_start`, `on_pause`, `on_resume`, `on_reset`.

### `theme.py`
- Định nghĩa tất cả màu sắc, font, spacing dùng chung toàn app.
- Không widget nào được hardcode màu hex — lấy từ `theme.py`.

---

## Người 3 — Settings + Music Panel

### `settings_panel.py`
- Form nhập thời lượng Work / Short Break / Long Break.
- Validate dữ liệu nhập (phải là số nguyên dương).
- Gọi `on_save(dict)` khi lưu — không tự ghi dữ liệu ra file.

### `music_panel.py`
- Label hiển thị tên bài hát đang phát.
- Nút Play / Pause / Stop.
- Slider âm lượng.
- Nút chọn file nhạc (mở file dialog).
- Nhận toàn bộ hành động qua callbacks.

---

## Timer Display

- Cập nhật mỗi giây qua `after(1000, callback)` — **không dùng `time.sleep()`**.
- Hủy `after` callback khi cửa sổ đóng để tránh memory leak.

---

## Layout

- Dùng `.grid()` làm primary layout manager.
- `padx` / `pady` tối thiểu: **8px**.
- Dùng `sticky="nsew"` + `columnconfigure(weight=1)` cho layout responsive.

---

## Color & Theme (`theme.py`)

```python
WORK_COLOR        = "#E74C3C"
SHORT_BREAK_COLOR = "#2ECC71"
LONG_BREAK_COLOR  = "#3498DB"
FONT_TIMER        = ("Segoe UI", 64, "bold")
PAD_MD            = 16
```
