"""
Background music player using pygame.mixer.

👤 Người 2 – Core
Phụ trách: Phát nhạc nền, quản lý playlist, điều chỉnh âm lượng,
           phát âm thanh thông báo (chuông cảnh báo).

Lưu ý: Người 1 phụ trách toàn bộ UI (kể cả màn hình chọn nhạc).
       Người 3 phụ trách logic tùy chỉnh chuông từ settings.
"""

from pathlib import Path
from typing import List, Optional

# Khởi tạo pygame.mixer một lần khi import module
try:
    import pygame
    pygame.mixer.init()
    _PYGAME_OK = True
except Exception:
    _PYGAME_OK = False

# Định dạng âm thanh được hỗ trợ
SUPPORTED_FORMATS = {".mp3", ".wav", ".ogg"}

# File chuông mặc định (Người 3 có thể thay bằng file tùy chỉnh)
DEFAULT_BELL_SOUND = "assets/sounds/bell.wav"


class MusicPlayer:
    """Phát nhạc nền và âm thanh thông báo bằng pygame.mixer.

    - Nhạc nền: dùng pygame.mixer.music (mp3/ogg/wav, hỗ trợ loop).
    - Chuông/âm thanh ngắn: dùng pygame.mixer.Sound (phát riêng, không ảnh
      hưởng nhạc nền).
    - Nếu không có pygame hoặc không có thiết bị âm thanh, mọi lệnh đều
      là no-op (không báo lỗi).

    Example:
        player = MusicPlayer()
        player.load("assets/music/lofi.mp3")
        player.play(loop=True)
        player.set_volume(0.6)
    """

    def __init__(self) -> None:
        self._current_file: Optional[Path] = None
        self._playlist: List[Path] = []
        self._playlist_index: int = 0
        self._volume: float = 0.5
        self._is_playing: bool = False

        if _PYGAME_OK:
            pygame.mixer.music.set_volume(self._volume)

    # ------------------------------------------------------------------
    # Điều khiển phát nhạc nền
    # ------------------------------------------------------------------

    def load(self, filepath: str) -> bool:
        """Tải một file âm thanh vào bộ phát nhạc nền.

        Args:
            filepath: Đường dẫn tới file âm thanh (.mp3, .wav, .ogg).

        Returns:
            True nếu tải thành công, False nếu file không tồn tại hoặc lỗi.
        """
        if not _PYGAME_OK:
            return False
        path = Path(filepath)
        if not path.exists():
            return False
        if path.suffix.lower() not in SUPPORTED_FORMATS:
            return False
        try:
            pygame.mixer.music.load(str(path))
            self._current_file = path
            self._is_playing = False
            return True
        except Exception:
            return False

    def play(self, loop: bool = True) -> None:
        """Phát nhạc nền.

        Args:
            loop: Nếu True, lặp lại vô hạn (mặc định). False để phát 1 lần.
        """
        if not _PYGAME_OK or self._current_file is None:
            return
        loops = -1 if loop else 0
        pygame.mixer.music.play(loops)
        self._is_playing = True

    def pause(self) -> None:
        """Tạm dừng nhạc nền."""
        if not _PYGAME_OK:
            return
        pygame.mixer.music.pause()
        self._is_playing = False

    def resume(self) -> None:
        """Tiếp tục phát nhạc sau khi pause."""
        if not _PYGAME_OK:
            return
        pygame.mixer.music.unpause()
        self._is_playing = True

    def stop(self) -> None:
        """Dừng hẳn nhạc nền."""
        if not _PYGAME_OK:
            return
        pygame.mixer.music.stop()
        self._is_playing = False

    def set_volume(self, volume: float) -> None:
        """Điều chỉnh âm lượng nhạc nền.

        Args:
            volume: Giá trị từ 0.0 (tắt tiếng) đến 1.0 (to nhất).
        """
        self._volume = max(0.0, min(1.0, volume))
        if _PYGAME_OK:
            pygame.mixer.music.set_volume(self._volume)

    # ------------------------------------------------------------------
    # Quản lý playlist
    # ------------------------------------------------------------------

    def load_playlist(self, folder: str) -> None:
        """Tải toàn bộ file nhạc trong một thư mục làm playlist.

        Args:
            folder: Đường dẫn thư mục chứa file nhạc.
        """
        folder_path = Path(folder)
        if not folder_path.is_dir():
            return
        self._playlist = sorted(
            p for p in folder_path.iterdir()
            if p.suffix.lower() in SUPPORTED_FORMATS
        )
        self._playlist_index = 0
        if self._playlist:
            self.load(str(self._playlist[0]))

    def next_track(self) -> None:
        """Chuyển sang bài tiếp theo trong playlist."""
        if not self._playlist:
            return
        self._playlist_index = (self._playlist_index + 1) % len(self._playlist)
        was_playing = self._is_playing
        self.load(str(self._playlist[self._playlist_index]))
        if was_playing:
            self.play()

    def previous_track(self) -> None:
        """Quay lại bài trước trong playlist."""
        if not self._playlist:
            return
        self._playlist_index = (self._playlist_index - 1) % len(self._playlist)
        was_playing = self._is_playing
        self.load(str(self._playlist[self._playlist_index]))
        if was_playing:
            self.play()

    # ------------------------------------------------------------------
    # Âm thanh thông báo (chuông cảnh báo)
    # ------------------------------------------------------------------

    def play_sound(self, filepath: str = DEFAULT_BELL_SOUND) -> None:
        """Phát một âm thanh ngắn (chuông thông báo).

        Phát độc lập, không ảnh hưởng đến nhạc nền đang chạy.
        Người 3 có thể truyền đường dẫn file tùy chỉnh từ settings.

        Args:
            filepath: Đường dẫn file âm thanh ngắn (.wav hoặc .ogg).
                      Mặc định dùng assets/sounds/bell.wav.
        """
        if not _PYGAME_OK:
            return
        path = Path(filepath)
        if not path.exists():
            return
        try:
            sound = pygame.mixer.Sound(str(path))
            sound.play()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Thuộc tính chỉ đọc (UI đọc các giá trị này)
    # ------------------------------------------------------------------

    @property
    def is_playing(self) -> bool:
        """True nếu nhạc nền đang phát."""
        return self._is_playing

    @property
    def volume(self) -> float:
        """Âm lượng hiện tại (0.0 – 1.0)."""
        return self._volume

    @property
    def current_track(self) -> Optional[str]:
        """Tên file bài nhạc đang được tải, hoặc None."""
        return self._current_file.name if self._current_file else None

    @property
    def playlist(self) -> List[str]:
        """Danh sách tên file trong playlist hiện tại."""
        return [p.name for p in self._playlist]

    @property
    def playlist_index(self) -> int:
        """Vị trí bài đang chọn trong playlist."""
        return self._playlist_index
