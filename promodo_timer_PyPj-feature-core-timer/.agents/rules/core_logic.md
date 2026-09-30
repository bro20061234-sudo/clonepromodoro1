# Core Logic Rules – Người 2 (`src/core/`)

> **Scope**: `src/core/timer.py`, `src/core/music_player.py`, `src/core/notification.py`
> Người 3 phụ trách `src/core/history.py` (xem phần riêng bên dưới).

---

## Nguyên tắc chính

- `src/core/` là **zero UI dependency**. Không bao giờ import từ `src/ui/`.
- Mọi state (timer, nhạc) đều sống ở đây.
- Logic phải có thể test độc lập bằng `pytest` — không cần mở cửa sổ GUI.

---

## ✅ Trạng thái thực tế (đã implement xong – branch `feature/core-timer`)

| File | Trạng thái |
|---|---|
| `timer.py` | ✅ Hoàn chỉnh |
| `music_player.py` | ✅ Hoàn chỉnh |
| `notification.py` | ✅ Hoàn chỉnh |

---

## `timer.py` – API thực tế

### Khởi tạo

```python
from src.core.timer import PomodoroTimer, PomodoroState

timer = PomodoroTimer(
    work_minutes=25,
    short_break_minutes=5,
    long_break_minutes=15,
    sessions_before_long=4,
)
```

### Điều khiển (Người 1 gọi từ UI buttons)

```python
timer.start()           # IDLE → WORK
timer.pause()           # WORK/BREAK → PAUSED
timer.resume()          # PAUSED → trở về pha cũ
timer.reset()           # → IDLE
timer.skip_phase()      # bỏ qua pha hiện tại ngay lập tức
timer.tick()            # UI gọi mỗi giây qua after(1000, ...)
```

### Cài đặt thời lượng (Người 3 gọi từ Settings Panel)

```python
# Có hiệu lực từ lần start() tiếp theo
timer.set_duration(work=25, short_break=5, long_break=15)
```

### Đăng ký callbacks (Người 1 đăng ký trong main_window.py qua main.py)

```python
# Gọi mỗi giây với số giây còn lại
timer.on_tick(lambda remaining_secs: ...)

# Gọi khi chuyển pha (WORK / SHORT_BREAK / LONG_BREAK / IDLE)
timer.on_phase_change(lambda state: ...)

# Gọi khi hoàn thành 1 phiên WORK (để history.py lưu lại)
timer.on_session_complete(lambda: ...)

# Chuông cảnh báo trước khi hết phiên
# warning_seconds mặc định = 300 (5 phút)
# Người 3 gọi lại với giá trị tùy chỉnh từ Settings
timer.on_warning(callback=lambda: ..., warning_seconds=300)
```

### Properties (Người 1 đọc để hiển thị)

```python
timer.state              # PomodoroState hiện tại
timer.remaining_seconds  # Số giây còn lại
timer.completed_sessions # Số phiên WORK đã hoàn thành
```

### Chu kỳ tự động

```
WORK (25') → SHORT_BREAK (5') → WORK → SHORT_BREAK → LONG_BREAK (15') → WORK → ...
                                                  ↑ sau mỗi 4 phiên WORK
```

---

## `music_player.py` – API thực tế

> ⚠️ Phân chia trách nhiệm:
> - **Người 2**: logic phát nhạc, quản lý playlist, chọn nhạc từ danh sách
> - **Người 1**: toàn bộ UI (kể cả màn hình chọn nhạc, nút play/pause nhạc)
> - **Người 3**: logic tùy chỉnh chuông thông báo từ Settings

### Khởi tạo

```python
from src.core.music_player import MusicPlayer

player = MusicPlayer()  # tự init pygame.mixer, graceful nếu không có audio
```

### Nhạc nền (Người 1 gọi khi người dùng bấm nút trên UI)

```python
player.load("assets/music/lofi.mp3")  # trả về True/False
player.play(loop=True)                 # phát (mặc định lặp)
player.pause()
player.resume()
player.stop()
player.set_volume(0.6)                 # 0.0 → 1.0, tự clamp
```

### Playlist (Người 1 gọi khi người dùng chọn thư mục nhạc)

```python
player.load_playlist("assets/music/")  # tự quét .mp3/.wav/.ogg
player.next_track()                     # chuyển bài, wrap-around
player.previous_track()
```

### Properties (Người 1 đọc để hiển thị trên UI)

```python
player.current_track   # tên file đang phát (str | None)
player.playlist        # danh sách tên file (List[str])
player.playlist_index  # vị trí bài hiện tại
player.is_playing      # bool
player.volume          # float
```

### Chuông ngắn / âm thanh thông báo

```python
# Phát độc lập, KHÔNG ảnh hưởng nhạc nền đang chạy
# Người 3 truyền filepath tùy chỉnh từ Settings
# File mặc định: assets/sounds/bell.wav
player.play_sound("assets/sounds/bell.wav")
```

---

## `notification.py` – API thực tế

```python
from src.core.notification import NotificationManager

notifier = NotificationManager()

notifier.notify_work_end()           # "⏰ Hết giờ làm việc!"
notifier.notify_break_end()          # "💪 Hết giờ nghỉ!"
notifier.notify_long_break_end()     # "🚀 Hết giờ nghỉ dài!"
notifier.notify_warning(minutes_left=5)  # "⏳ Còn 5 phút!"
```

> Ưu tiên **plyer** (Windows toast notification).
> Fallback **tkinter.messagebox** — an toàn vì luôn chạy trong main thread.

---

## Cách kết nối trong `main.py` (Người 1 làm)

```python
# Ví dụ wire notification khi phase thay đổi
def _handle_notification(state, notifier):
    from src.core.timer import PomodoroState
    if state in (PomodoroState.SHORT_BREAK, PomodoroState.LONG_BREAK):
        notifier.notify_work_end()
    elif state == PomodoroState.WORK:
        notifier.notify_break_end()

timer.on_phase_change(lambda s: _handle_notification(s, notifier))

# Wire chuông cảnh báo (warning_seconds Người 3 có thể thay đổi)
timer.on_warning(
    callback=lambda: music_player.play_sound("assets/sounds/bell.wav"),
    warning_seconds=300,
)
```

---

## `history.py` – Người 3 (chưa implement)

> File này nằm trong `src/core/` nhưng do **Người 3** implement.

- Lưu lịch sử phiên vào `data/history.json`
- Gọi trong callback `timer.on_session_complete(lambda: history.add_session(...))`
- Schema mỗi entry:
  ```json
  {
    "date": "09/09/2026",
    "start_time": "20:00",
    "end_time": "20:25",
    "phase": "Work",
    "status": "Completed"
  }
  ```
- ⚠️ Hiện tại `test_history.py` đang fail toàn bộ vì `_load()` chưa implement.
