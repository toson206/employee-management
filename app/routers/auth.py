from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.auth import hash_password, verify_password
from app.database import get_db
from app.models import Auth, Employee, EmployeeDepartment
from app.routers.employees import format_employee_response
from app.schemas import LoginResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản và tự động tạo hồ sơ nhân viên"
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # 1. Kiểm tra trùng username
    existing_user = db.query(Auth).filter(Auth.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập (username) đã tồn tại"
        )

    # 2. Kiểm tra trùng phone hoặc email trong bảng employees
    existing_emp = (
        db.query(Employee)
        .filter((Employee.email == user_data.email) | (Employee.phone == user_data.phone))
        .first()
    )
    if existing_emp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc số điện thoại này đã được sử dụng"
        )

    try:
        # 3. Tạo hồ sơ nhân viên
        new_employee = Employee(
            name=user_data.full_name,
            phone=user_data.phone,
            email=user_data.email
        )
        db.add(new_employee)
        db.flush()  # Sinh ID nhân viên

        # 4. Tạo tài khoản đăng nhập liên kết với nhân viên vừa tạo
        new_user = Auth(
            username=user_data.username,
            password=hash_password(user_data.password),
            role="employee",
            employee_id=new_employee.id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi khi đăng ký tài khoản: {str(e)}"
        )

    user_response = UserResponse(
        id=new_user.id,
        username=new_user.username,
        role=new_user.role,
        employee_id=new_user.employee_id,
        created_at=new_user.created_at,
        employee_profile=format_employee_response(new_employee)
    )

    return user_response



@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Đăng nhập tài khoản bằng Username, Email hoặc SĐT"
)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    login_identifier = user_data.username.strip()

    # Tìm user theo username trước
    user = db.query(Auth).filter(Auth.username == login_identifier).first()

    # Nếu không thấy theo username, tìm theo email hoặc số điện thoại của nhân viên liên kết
    if not user:
        emp = (
            db.query(Employee)
            .filter((Employee.email == login_identifier) | (Employee.phone == login_identifier))
            .first()
        )
        if emp and emp.user_account:
            user = emp.user_account

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập, email, số điện thoại hoặc mật khẩu không chính xác"
        )


    emp_profile = None
    if user.employee_id:
        emp = (
            db.query(Employee)
            .options(joinedload(Employee.department_associations).joinedload(EmployeeDepartment.department))
            .filter(Employee.id == user.employee_id)
            .first()
        )
        if emp:
            emp_profile = format_employee_response(emp)

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        role=user.role or "employee",
        employee_id=user.employee_id,
        created_at=user.created_at,
        employee_profile=emp_profile
    )

    return {
        "message": "Đăng nhập thành công",
        "user": user_response
    }


@router.get(
    "/me/{user_id}",
    response_model=UserResponse,
    summary="Đồng bộ thông tin và vai trò mới nhất của người dùng"
)
def get_user_profile_sync(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Auth).filter(Auth.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tài khoản không tồn tại"
        )

    emp_profile = None
    if user.employee_id:
        emp = (
            db.query(Employee)
            .options(joinedload(Employee.department_associations).joinedload(EmployeeDepartment.department))
            .filter(Employee.id == user.employee_id)
            .first()
        )
        if emp:
            emp_profile = format_employee_response(emp)

    return UserResponse(
        id=user.id,
        username=user.username,
        role=user.role or "employee",
        employee_id=user.employee_id,
        created_at=user.created_at,
        employee_profile=emp_profile
    )


