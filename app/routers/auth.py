from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.database import get_db
from app.models import Auth
from app.schemas import LoginResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản"
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(Auth).filter(Auth.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập (username) đã tồn tại"
        )

    new_user = Auth(
        username=user_data.username,
        password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Đăng nhập tài khoản"
)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Auth).filter(Auth.username == user_data.username).first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác"
        )

    return {
        "message": "Đăng nhập thành công",
        "user": user
    }
