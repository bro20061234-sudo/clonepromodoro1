"""
Settings panel — giao diện chỉnh thời lượng phiên Pomodoro.

👤 Người 3 – Settings + Music UI + History
Phụ trách: Form nhập thời lượng Work/Break, kiểm tra dữ liệu nhập, gọi callback khi lưu.
"""

import customtkinter
from typing import Callable


class SettingsPanel(customtkinter.CTkFrame):
    """Panel chỉnh thời lượng Work / Short Break / Long Break.

    Hiển thị form nhập liệu và nút Save.
    Gọi on_save(dict) khi người dùng xác nhận — KHÔNG tự lưu dữ liệu.

    Args:
        master: Widget cha.
        on_save: Callback nhận dict {"work": int, "short_break": int, "long_break": int}.
        current: Dict giá trị hiện tại để điền sẵn vào form.
    """

    def __init__(
        self,
        master,
        on_save: Callable[[dict], None],
        current: dict,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._on_save = on_save
        self._current = current
        self._build_ui()

    def _build_ui(self) -> None:
        """Tạo các input field và nút Save."""
        self._entries = {}
        fields = (
            ("work", "Work (minutes)"),
            ("short_break", "Short break (minutes)"),
            ("long_break", "Long break (minutes)"),
        )

        for key, label_text in fields:
            customtkinter.CTkLabel(self, text=label_text).pack(anchor="w", padx=12, pady=(8, 0))
            entry = customtkinter.CTkEntry(self)
            entry.pack(fill="x", padx=12, pady=(2, 0))
            self._entries[key] = entry

        self._error_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self._error_label.pack(padx=12, pady=(6, 0))
        customtkinter.CTkButton(self, text="Save", command=self._on_save_clicked).pack(
            padx=12, pady=10
        )
        self.refresh(self._current)

    def _on_save_clicked(self) -> None:
        """Thu thập giá trị từ form, validate rồi gọi callback."""
        try:
            values = {key: int(entry.get().strip()) for key, entry in self._entries.items()}
        except ValueError:
            self._error_label.configure(text="Please enter whole numbers.")
            return

        if any(value <= 0 for value in values.values()):
            self._error_label.configure(text="Durations must be greater than 0.")
            return

        self._error_label.configure(text="")
        self._current = values
        self._on_save(values)

    def refresh(self, current: dict) -> None:
        """Cập nhật lại giá trị hiển thị trên form.

        Args:
            current: Dict chứa giá trị mới để điền vào form.
        """
        self._current = dict(current)
        for key, entry in self._entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(self._current[key]))
