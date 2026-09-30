"""
Pomodoro Timer – Application Entry Point.

👥 main.py là nơi DUY NHẤT kết nối 3 module:
   - src/ui/   (Người 1)
   - src/core/ (Người 2 + Người 3 phần history)
   - Người 3 cũng đóng góp src/ui/settings_panel.py, music_panel.py

Không đặt business logic ở đây. Chỉ khởi tạo và wire dependencies.
"""

import customtkinter
from pathlib import Path

from src.core.timer import PomodoroTimer
from src.core.music_player import MusicPlayer
from src.core.notification import NotificationManager
from src.core.history import History

from src.ui.main_window import MainWindow


def main() -> None:
    """Khởi tạo toàn bộ module và chạy ứng dụng."""

    # ── Appearance ────────────────────────────────────────────────────
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # ── Core (Người 2) ────────────────────────────────────────────────
    timer = PomodoroTimer(
        work_minutes=25,
        short_break_minutes=5,
        long_break_minutes=15,
        sessions_before_long=4,
    )
    music_player = MusicPlayer()
    music_folder = Path(__file__).resolve().parent / "assets" / "music"
    music_player.load_playlist(str(music_folder))
    notifier = NotificationManager()

    # ── History (Người 3) ─────────────────────────────────────────────
    history = History()

    # Wire notification đến timer
    timer.on_phase_change(lambda state: _handle_notification(state, notifier))

    # ── GUI (Người 1) ─────────────────────────────────────────────────
    window = MainWindow(
        timer=timer,
        music_player=music_player,
        history=history,
    )

    window.mainloop()


def _handle_notification(state, notifier: NotificationManager) -> None:
    """Gửi notification phù hợp khi pha thay đổi.

    Args:
        state: PomodoroState mới.
        notifier: NotificationManager instance.
    """
    from src.core.timer import PomodoroState
    if state in (PomodoroState.SHORT_BREAK, PomodoroState.LONG_BREAK):
        notifier.notify_work_end()
    elif state == PomodoroState.WORK:
        notifier.notify_break_end()


if __name__ == "__main__":
    main()
