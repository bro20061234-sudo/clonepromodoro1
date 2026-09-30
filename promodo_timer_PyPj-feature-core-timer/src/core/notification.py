"""
Desktop notification manager.

👤 Người 2 – Core
Phụ trách: Gửi desktop notification khi phiên kết thúc.
Fallback về tkinter.messagebox nếu plyer không khả dụng.
"""

try:
    from plyer import notification as _plyer_notification
    _PLYER_AVAILABLE = True
except ImportError:
    _PLYER_AVAILABLE = False


class NotificationManager:
    """Sends desktop notifications when a Pomodoro session ends.

    Thứ tự ưu tiên:
      1. plyer – hiện system notification (toast/balloon trên Windows).
      2. tkinter.messagebox – popup đơn giản nếu plyer lỗi.

    Lưu ý: callback luôn được gọi trong main thread (qua tkinter after()),
    nên dùng messagebox là an toàn.

    Example:
        notifier = NotificationManager()
        notifier.notify_work_end()
        notifier.notify_break_end()
    """

    APP_NAME: str = "Pomodoro Timer"

    def notify_work_end(self) -> None:
        """Gửi thông báo khi phiên làm việc kết thúc."""
        self._send(
            title="⏰ Hết giờ làm việc!",
            message="Đã đến lúc nghỉ giải lao. Thư giãn một chút nhé! 🎉",
        )

    def notify_break_end(self) -> None:
        """Gửi thông báo khi nghỉ ngắn kết thúc."""
        self._send(
            title="💪 Hết giờ nghỉ!",
            message="Đã đến lúc bắt đầu phiên học mới. Tập trung nào!",
        )

    def notify_long_break_end(self) -> None:
        """Gửi thông báo khi nghỉ dài kết thúc."""
        self._send(
            title="🚀 Hết giờ nghỉ dài!",
            message="Đã sẵn sàng cho vòng Pomodoro mới chưa? Let's go!",
        )

    def notify_warning(self, minutes_left: int = 5) -> None:
        """Gửi thông báo cảnh báo còn N phút nữa hết phiên.

        Args:
            minutes_left: Số phút còn lại (hiển thị trong nội dung).
        """
        self._send(
            title=f"⏳ Còn {minutes_left} phút!",
            message=f"Phiên sẽ kết thúc sau {minutes_left} phút nữa.",
        )

    def _send(self, title: str, message: str) -> None:
        """Gửi notification, ưu tiên plyer, fallback về messagebox.

        Args:
            title: Tiêu đề thông báo.
            message: Nội dung thông báo.
        """
        if _PLYER_AVAILABLE:
            try:
                _plyer_notification.notify(
                    title=title,
                    message=message,
                    app_name=self.APP_NAME,
                    timeout=5,
                )
                return
            except Exception:
                pass

        # Fallback: tkinter messagebox
        # An toàn vì hàm này luôn được gọi từ main thread (qua after())
        import tkinter.messagebox as messagebox
        messagebox.showinfo(title=title, message=message)
