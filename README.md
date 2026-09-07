# 🏢 Employee Management Backend API

Hệ thống Backend RESTful API quản lý nhân viên và tài khoản xác thực , được xây dựng bằng **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic** và **Bcrypt**.

---

## 🚀 Công nghệ sử dụng

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database Migration:** [Alembic](https://alembic.sqlalchemy.org/)
- **Validation:** [Pydantic V2](https://docs.pydantic.dev/) (kèm `email-validator`)
- **Bảo mật:** [Bcrypt](https://pypi.org/project/bcrypt/) (Mã hóa mật khẩu)
- **Server:** [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Cấu trúc thư mục

```text
employee-management/
├── alembic/                  # Cấu hình và các file migration cơ sở dữ liệu
│   ├── versions/             # Các phiên bản migration DB
│   └── env.py                # Cấu hình Alembic kết nối SQLAlchemy Base
├── app/
│   ├── routers/              # Các router định nghĩa API endpoints
│   │   ├── auth.py           # API Đăng ký, Đăng nhập (Auth)
│   │   └── employees.py      # API CRUD quản lý nhân viên
│   ├── auth.py               # Các hàm tiện ích bảo mật (hash/verify password)
│   ├── database.py           # Cấu hình kết nối PostgreSQL & Session DB
│   ├── main.py               # File khởi tạo ứng dụng FastAPI & Middleware
│   ├── models.py             # Định nghĩa cấu trúc bảng SQLAlchemy (ORM)
│   └── schemas.py            # Pydantic schemas (Data validation & Response)
├── .env                      # File cấu hình biến môi trường (Database credentials)
├── .env.example              # File mẫu biến môi trường
├── alembic.ini               # File cấu hình Alembic CLI
├── requirements.txt          # Danh sách các thư viện Python cần thiết
└── README.md                 # Tài liệu hướng dẫn sử dụng dự án
```

---

## ⚙️ Hướng dẫn cài đặt và chạy dự án

### 1. Yêu cầu hệ thống
- Python 3.13
- PostgreSQL đã cài đặt và đang chạy

### 2. Cài đặt môi trường ảo và thư viện

```bash
# Tạo môi trường ảo (tùy chọn)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường (`.env`)

Tạo file `.env` tại thư mục gốc (hoặc copy từ `.env.example`) và điền thông tin kết nối Database của bạn:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
```

### 4. Chạy Migration tạo bảng Database

```bash
# Áp dụng migration mới nhất vào database
alembic upgrade head
```

### 5. Khởi động Server Backend

```bash
uvicorn app.main:app --reload --port 8000

---

## 📖 Tài liệu API tương tác (Swagger UI)

Khi server đang chạy, bạn mở trình duyệt và truy cập:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Danh sách các API Endpoints

### 🔐 1. Xác thực (Auth)

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Đăng ký tài khoản mới (mật khẩu được băm tự động bằng Bcrypt) |
| `POST` | `/api/auth/login` | Đăng nhập tài khoản (kiểm tra username & password) |

#### Ví dụ Body đăng ký / đăng nhập:
```json
{
  "username": "admin",
  "password": "password123"
}
```

---

### 👥 2. Quản lý Nhân viên (Employees)

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/api/employees/` | Lấy danh sách nhân viên (hỗ trợ phân trang `?skip=0&limit=100`) |
| `GET` | `/api/employees/{id}` | Lấy chi tiết thông tin một nhân viên theo ID |
| `POST` | `/api/employees/` | Thêm mới một hồ sơ nhân viên |
| `PUT` | `/api/employees/{id}` | Cập nhật thông tin nhân viên theo ID |
| `DELETE` | `/api/employees/{id}` | Xóa nhân viên theo ID |
