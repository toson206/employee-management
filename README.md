# Employee Management API

RESTful API quản lý thông tin nhân viên sử dụng FastAPI và PostgreSQL.

## Công nghệ

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Cài đặt

### 1. Tạo môi trường ảo

```bash
py -3.13 -m venv .venv
```

### 2. Kích hoạt môi trường ảo

Trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Cài đặt thư viện

```bash
pip install "fastapi[standard]" sqlalchemy psycopg2-binary email-validator
```

## Cơ sở dữ liệu PostgreSQL

Tạo database:

```sql
CREATE DATABASE employee_management;
```

Bảng `employees` gồm:

- `id`: Primary Key, Auto Increment
- `name`: Tên nhân viên, bắt buộc
- `phone`: Số điện thoại
- `email`: Email, bắt buộc, đúng định dạng và không trùng
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật

## Chạy project

```bash
uvicorn main:app --reload
```

Server chạy tại: `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/employees/` | Thêm nhân viên |
| GET | `/api/employees/` | Lấy danh sách nhân viên |
| GET | `/api/employees/{id}` | Lấy thông tin nhân viên theo ID |
| PUT | `/api/employees/{id}` | Cập nhật thông tin nhân viên |
| DELETE | `/api/employees/{id}` | Xóa nhân viên |
## Testing

Sử dụng Swagger UI để kiểm tra toàn bộ API CRUD trực tiếp tại:
`http://127.0.0.1:8000/docs`