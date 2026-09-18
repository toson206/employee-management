# 🏢 Employee Management Backend API

Hệ thống Backend RESTful API quản lý nhân sự, phòng ban và phân quyền người dùng, được xây dựng bằng **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic** và **Bcrypt**.

---

## 🚀 Công nghệ sử dụng

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13)
- **Database:** [PostgreSQL](https://www.postgresql.org/) (Cloud Supabase)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Quan hệ 1-1, N-N)
- **Database Migration:** [Alembic](https://alembic.sqlalchemy.org/)
- **Validation:** [Pydantic V2](https://docs.pydantic.dev/)
- **Bảo mật:** [Bcrypt](https://pypi.org/project/bcrypt/) (Mã hóa mật khẩu)
- **Mô hình phân quyền:** RBAC (Super Admin, Admin, Employee)
- **Server:** [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Cấu trúc thư mục Backend

```text
employee-management/
├── alembic/                  # Cấu hình và các file migration cơ sở dữ liệu
│   ├── versions/             # Lịch sử các migration database
│   └── env.py                # Cấu hình Alembic kết nối SQLAlchemy
├── app/
│   ├── routers/              # Các router định nghĩa API endpoints
│   │   ├── auth.py           # API Đăng ký, Đăng nhập (Username/Email/SĐT), đồng bộ quyền
│   │   ├── departments.py    # API CRUD phòng ban, xem và gỡ nhân viên khỏi phòng
│   │   ├── employees.py      # API CRUD nhân viên (kèm phòng ban & cấp tài khoản)
│   │   └── users.py          # API Quản lý tài khoản và phân quyền
│   ├── auth.py               # Các hàm tiện ích bảo mật (hash/verify password bằng Bcrypt)
│   ├── database.py           # Cấu hình kết nối PostgreSQL & Session DB
│   ├── main.py               # Khởi tạo FastAPI, CORS Middleware & Routes
│   ├── models.py             # Định nghĩa cấu trúc bảng SQLAlchemy (Auth, Employee, Department, EmployeeDepartment)
│   └── schemas.py            # Pydantic schemas (Validation & Response models)
├── scripts/                  # Các script hỗ trợ khởi tạo dữ liệu
│   ├── create_admin.py       # Tạo hoặc nâng cấp tài khoản Super Admin
│   ├── init_roles.py         # Khởi tạo quyền mặc định ban đầu
│   └── seed_departments.py   # Nạp dữ liệu phòng ban mẫu
├── .env                      # Cấu hình biến môi trường kết nối DB
├── .env.example              # File mẫu cấu hình môi trường
├── alembic.ini               # Cấu hình Alembic CLI
├── requirements.txt          # Danh sách thư viện Python
└── README.md                 # Tài liệu hướng dẫn sử dụng dự án
```

---

## ⚙️ Hướng dẫn cài đặt và chạy dự án

### 1. Cài đặt thư viện

```bash
# Tạo môi trường ảo (tùy chọn)
python -m venv venv
venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường (`.env`)

Sao chép `.env.example` thành `.env` và điền thông tin kết nối Database của bạn:

```env
DB_HOST=aws-0-ap-southeast-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=your_user
DB_PASSWORD=your_password
```

### 3. Chạy Migration Database

```bash
alembic upgrade head
```

### 4. Khởi động Server Backend

```bash
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Danh sách các API Endpoints

### 🔐 1. Xác thực & Tài khoản cá nhân (`/api/auth`)

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Đăng ký tài khoản (tự động tạo hồ sơ nhân viên tương ứng) |
| `POST` | `/api/auth/login` | Đăng nhập linh hoạt (bằng Username, Email HOẶC Số điện thoại) |
| `GET` | `/api/auth/me/{user_id}` | Lấy thông tin và quyền mới nhất để đồng bộ theo thời gian thực |

### 👥 2. Quản lý Nhân viên (`/api/employees`)

| Phương thức | Endpoint | Mô tả |
| `GET` | `/api/employees/` | Lấy danh sách nhân viên (kèm danh sách phòng ban và ngày tham gia) |
| `GET` | `/api/employees/{id}` | Lấy chi tiết thông tin nhân viên theo ID |
| `POST` | `/api/employees/` | Thêm mới nhân viên (hỗ trợ cấp luôn tài khoản đăng nhập) |
| `PUT` | `/api/employees/{id}` | Cập nhật nhân viên (hỗ trợ phân phòng ban & cấp/đổi tài khoản) |
| `DELETE` | `/api/employees/{id}` | Xóa nhân viên theo ID |


### 🏢 3. Quản lý Phòng ban (`/api/departments`)

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/api/departments/` | Lấy danh sách phòng ban kèm số lượng nhân viên |
| `GET` | `/api/departments/{id}` | Lấy chi tiết phòng ban |
| `POST` | `/api/departments/` | Thêm phòng ban mới |
| `PUT` | `/api/departments/{id}` | Sửa tên, mô tả phòng ban |
| `DELETE` | `/api/departments/{id}` | Xóa phòng ban |
| `DELETE` | `/api/departments/{dept_id}/members/{employee_id}` | Gỡ một nhân viên ra khỏi phòng ban cụ thể |

### 🛡️ 4. Quản lý Phân quyền Người dùng (`/api/users`)

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/api/users/` | Lấy danh sách tất cả tài khoản trong hệ thống |
| `PUT` | `/api/users/{user_id}/role` | Nâng / Hạ quyền Admin <-> Employee (Bảo vệ Super Admin) |
