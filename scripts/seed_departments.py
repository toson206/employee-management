import os
import sys

# Thêm đường dẫn gốc vào sys.path để import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models import Department

INITIAL_DEPARTMENTS = [
    {
        "name": "Phòng Nhân sự",
        "description": "Quản lý tuyển dụng"
    },
    {
        "name": "Phòng Kế toán",
        "description": "Quản lý tài chính"
    },
    {
        "name": "Phòng Kinh doanh",
        "description": "Tìm kiếm khách hàng"
    }
]

def seed_departments():
    db = SessionLocal()
    try:
        print("Đang kiểm tra và khởi tạo dữ liệu phòng ban...")
        for dept_data in INITIAL_DEPARTMENTS:
            existing = db.query(Department).filter(Department.name == dept_data["name"]).first()
            if not existing:
                dept = Department(
                    name=dept_data["name"],
                    description=dept_data["description"]
                )
                db.add(dept)
                print(f"-> Đã thêm phòng ban: {dept_data['name']}")
            else:
                print(f"-> Đã tồn tại: {dept_data['name']}")
        db.commit()
        print("Khởi tạo 3 phòng ban mẫu thành công!")
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi khởi tạo phòng ban: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_departments()
