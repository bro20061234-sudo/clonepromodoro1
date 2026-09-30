"""
Main application window.

👤 Người 1 – GUI
Phụ trách: Layout tổng thể, khởi tạo và kết nối các widget con.
"""

import customtkinter
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from typing import TYPE_CHECKING

from src.core.history import SessionEntry
from src.core.timer import PomodoroState
from src.ui.music_panel import MusicPanel
from src.ui.settings_panel import SettingsPanel
from src.ui.timer_widget import TimerWidget

if TYPE_CHECKING:
    from src.core import PomodoroTimer, MusicPlayer
    from src.core.history import History


class MainWindow(customtkinter.CTk):
    """Root application window. Owns and lays out all child widgets.

    Receives all dependencies via constructor (injected from main.py).
    Contains NO business logic — delegates everything to core modules.

    Args:
        timer: The Pomodoro timer controller.
        music_player: The background music player.
        history: Session history manager.
    """

    def __init__(
        self,
        timer: "PomodoroTimer",
        music_player: "MusicPlayer" = None,
        history: "History" = None,
    ) -> None:
        super().__init__()
        self._timer = timer
        self._music = music_player
        self._history = history
        self._phase_started_at = None
        self._settings_window = None
        self._statistics_window = None
        self._tick_running = False

        self.title("Pomodoro Timer")
        self.geometry("480x760")
        self.resizable(False, False)

        self._setup_layout()
        self._register_timer_callbacks()

    def _setup_layout(self) -> None:
        """Build and place all child widgets on the window."""
        self._timer_widget = TimerWidget(
            self,
            on_start=self._start_timer,
            on_pause=self._pause_timer,
            on_resume=self._resume_timer,
            on_reset=self._reset_timer,
            on_skip=self._timer.skip_phase,
        )
        self._timer_widget.pack(fill="x", padx=24, pady=24)

        self._sessions_label = customtkinter.CTkLabel(
            self,
            text="Completed sessions: 0",
        )
        self._sessions_label.pack(pady=8)

        if self._music is not None:
            self._music_panel = MusicPanel(
                self,
                on_play=self._play_music,
                on_pause=self._pause_music,
                on_resume=self._resume_music,
                on_stop=self._stop_music,
                on_volume_change=self._set_music_volume,
                on_pick_folder=self._pick_music_folder,
                on_previous=self._previous_music_track,
                on_next=self._next_music_track,
            )
            self._music_panel.pack(fill="x", padx=24, pady=8)
            self._music_panel.set_volume(self._music.volume)
            self._refresh_music_track_label()

        actions = customtkinter.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=24, pady=(8, 16))
        customtkinter.CTkButton(
            actions,
            text="Settings",
            command=self._open_settings,
        ).pack(side="left", expand=True, padx=(0, 6))
        customtkinter.CTkButton(
            actions,
            text="Statistics",
            command=self._open_statistics,
        ).pack(side="left", expand=True, padx=(6, 0))

    def _refresh_music_track_label(self) -> None:
        """Show the loaded track, even if the audio device is unavailable."""
        if self._music is None:
            return
        playlist = self._music.playlist
        track_name = self._music.current_track
        if track_name is None and playlist:
            track_name = playlist[self._music.playlist_index]
        self._music_panel.update_track_label(track_name or "No tracks found")

    def _play_music(self) -> None:
        """Start the selected background track."""
        self._music.play()
        self._music_panel.set_playing_state(self._music.is_playing)

    def _pause_music(self) -> None:
        """Pause the selected background track."""
        self._music.pause()
        self._music_panel.set_paused_state(True)

    def _resume_music(self) -> None:
        """Resume the selected background track."""
        self._music.resume()
        self._music_panel.set_playing_state(self._music.is_playing)

    def _stop_music(self) -> None:
        """Stop the selected background track."""
        self._music.stop()
        self._music_panel.set_playing_state(False)

    def _set_music_volume(self, volume: float) -> None:
        """Apply the volume selected in the music panel."""
        self._music.set_volume(volume)

    def _pick_music_folder(self) -> None:
        """Load a playlist from a folder selected by the user."""
        default_folder = Path(__file__).resolve().parents[2] / "assets" / "music"
        folder = filedialog.askdirectory(
            parent=self,
            initialdir=str(default_folder),
            title="Choose a music folder",
        )
        if folder:
            self._music.stop()
            self._music.load_playlist(folder)
            self._music_panel.set_playing_state(False)
            self._refresh_music_track_label()

    def _previous_music_track(self) -> None:
        """Load and play the previous playlist track."""
        self._music.previous_track()
        self._refresh_music_track_label()
        self._music_panel.set_playing_state(self._music.is_playing)

    def _next_music_track(self) -> None:
        """Load and play the next playlist track."""
        self._music.next_track()
        self._refresh_music_track_label()
        self._music_panel.set_playing_state(self._music.is_playing)

    def _register_timer_callbacks(self) -> None:
        """Subscribe UI update methods to timer events."""
        self._timer.on_tick(self._on_tick)
        self._timer.on_phase_change(self._on_phase_change)
        self._timer.on_session_complete(self._on_session_complete)

    # ------------------------------------------------------------------
    # Timer event handlers (called by PomodoroTimer callbacks)
    # ------------------------------------------------------------------

    def _on_tick(self, remaining_seconds: int) -> None:
        """Update the timer display every second.

        Args:
            remaining_seconds: Seconds left in the current phase.
        """
        self._timer_widget.update_time(remaining_seconds)

    def _on_phase_change(self, state) -> None:
        """React to a phase transition (e.g. Work → Break).

        Args:
            state: The new PomodoroState.
        """
        phase_names = {
            PomodoroState.WORK: "Work",
            PomodoroState.SHORT_BREAK: "Short Break",
            PomodoroState.LONG_BREAK: "Long Break",
        }
        self._timer_widget.update_phase(phase_names.get(state, "Ready"))
        self._timer_widget.set_paused_state(state == PomodoroState.PAUSED)
        if state == PomodoroState.WORK:
            self._phase_started_at = datetime.now()

    def _on_session_complete(self) -> None:
        """React to a completed WORK session."""
        self._sessions_label.configure(
            text=f"Completed sessions: {self._timer.completed_sessions}"
        )
        if self._history is not None and self._phase_started_at is not None:
            completed_at = datetime.now()
            self._history.add_session(
                SessionEntry(
                    date=self._phase_started_at.strftime("%d/%m/%Y"),
                    start_time=self._phase_started_at.strftime("%H:%M"),
                    end_time=completed_at.strftime("%H:%M"),
                    phase="Work",
                    status="Completed",
                )
            )

    # ------------------------------------------------------------------
    # Tick driver — UI owns the after() loop
    # ------------------------------------------------------------------

    def _schedule_tick(self) -> None:
        """Drive the timer by calling tick() every second via after()."""
        if not self._tick_running or self._timer.state == PomodoroState.IDLE:
            self._tick_running = False
            return
        self._timer.tick()
        self.after(1000, self._schedule_tick)

    def _start_timer(self) -> None:
        """Start the timer and begin the UI tick loop."""
        self._timer.start()
        if not self._tick_running:
            self._tick_running = True
            self._schedule_tick()

    def _reset_timer(self) -> None:
        """Reset the timer and stop scheduling ticks until the next start."""
        self._tick_running = False
        self._timer.reset()

    def _save_settings(self, durations: dict) -> None:
        """Apply durations selected by the user to future timer phases."""
        self._timer.set_duration(**durations)

    def _open_settings(self) -> None:
        """Open the duration settings in a separate window."""
        if self._settings_window is not None and self._settings_window.winfo_exists():
            self._settings_window.focus()
            return

        self._settings_window = customtkinter.CTkToplevel(self)
        self._settings_window.title("Timer Settings")
        self._settings_window.geometry("360x390")
        self._settings_window.resizable(False, False)
        SettingsPanel(
            self._settings_window,
            on_save=self._save_settings,
            current=self._timer.durations,
        ).pack(fill="both", expand=True, padx=12, pady=12)
        self._settings_window.transient(self)
        self._settings_window.focus()

    def _open_statistics(self) -> None:
        """Show completed-session statistics from the current history."""
        if self._statistics_window is not None and self._statistics_window.winfo_exists():
            self._statistics_window.focus()
            return

        entries = self._history.get_all() if self._history is not None else []
        completed_entries = [entry for entry in entries if entry.status == "Completed"]

        self._statistics_window = customtkinter.CTkToplevel(self)
        self._statistics_window.title("Statistics")
        self._statistics_window.geometry("360x260")
        self._statistics_window.resizable(False, False)
        customtkinter.CTkLabel(
            self._statistics_window,
            text="Study Statistics",
            font=("Arial", 22, "bold"),
        ).pack(pady=(24, 16))
        customtkinter.CTkLabel(
            self._statistics_window,
            text=f"Completed sessions: {len(completed_entries)}",
            font=("Arial", 18),
        ).pack(pady=8)
        customtkinter.CTkLabel(
            self._statistics_window,
            text=f"This run: {self._timer.completed_sessions}",
        ).pack(pady=4)
        customtkinter.CTkButton(
            self._statistics_window,
            text="Refresh",
            command=self._refresh_statistics,
        ).pack(pady=16)
        self._statistics_window.transient(self)
        self._statistics_window.focus()

    def _refresh_statistics(self) -> None:
        """Refresh the statistics dialog after a new session completes."""
        if self._statistics_window is None or not self._statistics_window.winfo_exists():
            return
        self._statistics_window.destroy()
        self._statistics_window = None
        self._open_statistics()

    def _pause_timer(self) -> None:
        """Pause the timer and show the Resume control."""
        self._timer.pause()
        self._timer_widget.set_paused_state(True)

    def _resume_timer(self) -> None:
        """Resume the timer and show the Pause control."""
        self._timer.resume()
        self._timer_widget.set_paused_state(False)
