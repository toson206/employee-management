import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models import Auth, Employee
from app.auth import hash_password

def init_roles():
    db = SessionLocal()
    try:
        print("Đang kiểm tra và phân quyền tài khoản...")
        # Lấy tất cả user hiện có, nếu có user nào thì set user đầu tiên làm admin
        all_users = db.query(Auth).all()
        if all_users:
            for i, user in enumerate(all_users):
                if i == 0 or user.username in ["admin", "root"]:
                    user.role = "admin"
                    print(f"-> Đã gán quyền ADMIN cho tài khoản: {user.username}")
                else:
                    user.role = "employee"
                    print(f"-> Tài khoản {user.username} có quyền: {user.role}")
        else:
            # Nếu chưa có user nào, tạo sẵn 1 admin
            admin_user = Auth(
                username="admin",
                password=hash_password("admin123"),
                role="admin"
            )
            db.add(admin_user)
            print("-> Đã tạo tài khoản Admin mặc định: admin / admin123")

        # Kiểm tra nếu có nhân viên, liên kết tài khoản nhân viên mẫu với nhân viên đầu tiên
        first_employee = db.query(Employee).first()
        if first_employee:
            emp_user = db.query(Auth).filter(Auth.username == "nhanvien").first()
            if not emp_user:
                emp_user = Auth(
                    username="nhanvien",
                    password=hash_password("123456"),
                    role="employee",
                    employee_id=first_employee.id
                )
                db.add(emp_user)
                print(f"-> Đã tạo tài khoản nhân viên mẫu: nhanvien / 123456 (Liên kết với NV: {first_employee.name})")
            else:
                emp_user.role = "employee"
                emp_user.employee_id = first_employee.id
                print(f"-> Đã cập nhật tài khoản {emp_user.username} liên kết với NV: {first_employee.name}")

        db.commit()
        print("Khởi tạo quyền thành công!")
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_roles()
