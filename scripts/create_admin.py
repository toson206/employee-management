import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models import Auth
from app.auth import hash_password

def create_admin(username, password):
    db = SessionLocal()
    try:
        user = db.query(Auth).filter(Auth.username == username).first()
        if user:
            user.role = "super_admin"
            user.password = hash_password(password)
            print(f"-> Đã cập nhật tài khoản '{username}' thành quyền SUPER ADMIN với mật khẩu mới!")
        else:
            new_admin = Auth(
                username=username,
                password=hash_password(password),
                role="super_admin"
            )
            db.add(new_admin)
            print(f"-> Đã tạo mới tài khoản SUPER ADMIN thành công: '{username}'")
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tạo tài khoản Admin")
    parser.add_argument("--username", default="admin", help="Tên đăng nhập admin")
    parser.add_argument("--password", default="admin123", help="Mật khẩu admin")
    args = parser.parse_args()

    create_admin(args.username, args.password)
