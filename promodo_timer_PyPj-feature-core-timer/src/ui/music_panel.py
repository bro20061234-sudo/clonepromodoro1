"""
Music panel — giao diện chọn nhạc và điều khiển phát nhạc.

👤 Người 3 – Settings + Music UI + History
Phụ trách: Giao diện chọn file nhạc, playlist đơn giản, hiển thị tên bài đang phát.
"""

import customtkinter
from typing import Callable


class MusicPanel(customtkinter.CTkFrame):
    """Panel điều khiển nhạc nền.

    Hiển thị tên bài đang phát, nút play/pause/stop, slider âm lượng,
    và nút chọn file nhạc.
    Nhận callbacks từ MainWindow — KHÔNG import MusicPlayer trực tiếp.

    Args:
        master: Widget cha.
        on_play: Callback khi nhấn Play.
        on_pause: Callback khi nhấn Pause.
        on_stop: Callback khi nhấn Stop.
        on_volume_change: Callback nhận volume mới (float 0.0–1.0).
        on_pick_file: Callback khi nhấn nút chọn file nhạc.
    """

    def __init__(
        self,
        master,
        on_play: Callable,
        on_pause: Callable,
        on_resume: Callable,
        on_stop: Callable,
        on_volume_change: Callable[[float], None],
        on_pick_folder: Callable,
        on_previous: Callable,
        on_next: Callable,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_play = on_play
        self._on_pause = on_pause
        self._on_resume = on_resume
        self._on_stop = on_stop
        self._on_volume_change = on_volume_change
        self._on_pick_folder = on_pick_folder
        self._on_previous = on_previous
        self._on_next = on_next
        self._build_ui()

    def _build_ui(self) -> None:
        """Create track information and music playback controls."""
        customtkinter.CTkLabel(
            self,
            text="Background music",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=12, pady=(12, 4))

        self._track_label = customtkinter.CTkLabel(
            self,
            text="No music loaded",
            anchor="w",
            wraplength=400,
        )
        self._track_label.pack(fill="x", padx=12, pady=4)

        controls = customtkinter.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=8, pady=4)
        customtkinter.CTkButton(
            controls,
            text="Previous",
            command=self._on_previous,
            width=84,
        ).pack(side="left", expand=True, padx=3)
        self._play_button = customtkinter.CTkButton(
            controls,
            text="Play",
            command=self._on_play,
            width=70,
        )
        self._play_button.pack(side="left", expand=True, padx=3)
        customtkinter.CTkButton(
            controls,
            text="Stop",
            command=self._on_stop,
            width=70,
        ).pack(side="left", expand=True, padx=3)
        customtkinter.CTkButton(
            controls,
            text="Next",
            command=self._on_next,
            width=70,
        ).pack(side="left", expand=True, padx=3)

        volume_row = customtkinter.CTkFrame(self, fg_color="transparent")
        volume_row.pack(fill="x", padx=12, pady=(4, 8))
        customtkinter.CTkLabel(volume_row, text="Volume").pack(
            side="left", padx=(0, 8)
        )
        self._volume_slider = customtkinter.CTkSlider(
            volume_row,
            from_=0.0,
            to=1.0,
            command=self._on_volume_change,
        )
        self._volume_slider.pack(side="left", fill="x", expand=True)

        customtkinter.CTkButton(
            self,
            text="Choose music folder",
            command=self._on_pick_folder,
            height=32,
        ).pack(fill="x", padx=12, pady=(0, 12))

    def update_track_label(self, track_name: str) -> None:
        """Hiển thị tên bài hát đang phát.

        Args:
            track_name: File name or display name of the current track.
        """
        self._track_label.configure(text=track_name or "No music loaded")

    def set_volume(self, volume: float) -> None:
        """Set the displayed volume slider."""
        self._volume_slider.set(volume)

    def set_playing_state(self, is_playing: bool) -> None:
        """Chuyển icon nút Play/Pause theo trạng thái.

        Args:
            is_playing: True when music is playing.
        """
        if is_playing:
            self._play_button.configure(text="Pause", command=self._on_pause)
        else:
            self._play_button.configure(text="Play", command=self._on_play)

    def set_paused_state(self, is_paused: bool) -> None:
        """Show Resume while the current track is paused."""
        if is_paused:
            self._play_button.configure(text="Resume", command=self._on_resume)
