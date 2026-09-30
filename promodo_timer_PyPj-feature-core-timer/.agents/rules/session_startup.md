# Session Startup Checklist – AI Agent

## Quy tắc bắt buộc khi bắt đầu mỗi hội thoại mới

Mỗi khi người dùng bắt đầu một conversation mới trong dự án này, AI agent **PHẢI** thực hiện
các bước sau **trước khi** làm bất cứ việc gì khác:

---

### Bước 1 – Kích hoạt môi trường ảo

Chạy lệnh sau trong PowerShell tại thư mục gốc của dự án:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Kiểm tra:** Nếu terminal hiển thị `(.venv)` ở đầu dòng → thành công.

Nếu báo lỗi `cannot be loaded because running scripts is disabled`, chạy lệnh sau **một lần**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau đó chạy lại lệnh Activate.

---

### Bước 2 – Lấy code mới nhất từ GitHub

```powershell
git pull origin main
```

**Tại sao cần bước này?**
- Đồng đội có thể đã merge code mới vào `main`.
- AI agent đọc code trực tiếp từ file — sau khi pull, AI sẽ thấy đúng phiên bản
  mới nhất và tránh gợi ý code xung đột với công việc của người khác.

---

## Hành động của AI agent

Khi bắt đầu hội thoại mới, AI agent phải:

1. **Chạy tự động** 2 lệnh trên (thông qua `hooks.json`).
2. **Thông báo kết quả** cho người dùng: venv đã active chưa, git pull có thay đổi gì không.
3. **Nếu git pull báo conflict** → hướng dẫn người dùng cách resolve trước khi tiếp tục.
4. **Chỉ sau khi hoàn thành 2 bước trên** mới bắt đầu hỗ trợ coding.

---

## Nếu hooks.json không tự chạy được

AI agent phải **chủ động nhắc** người dùng chạy 2 lệnh trên mỗi khi bắt đầu conversation,
và chờ xác nhận người dùng đã chạy xong trước khi tiếp tục.
