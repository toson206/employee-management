from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Auth, Employee, EmployeeDepartment
from app.routers.employees import format_employee_response
from app.schemas import UserResponse, UserRoleUpdate

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả tài khoản đăng nhập trong hệ thống"""
    users = db.query(Auth).order_by(Auth.id).all()
    result = []
    for u in users:
        emp_profile = None
        if u.employee_id:
            emp = (
                db.query(Employee)
                .options(joinedload(Employee.department_associations).joinedload(EmployeeDepartment.department))
                .filter(Employee.id == u.employee_id)
                .first()
            )
            if emp:
                emp_profile = format_employee_response(emp)

        result.append(
            UserResponse(
                id=u.id,
                username=u.username,
                role=u.role or "employee",
                employee_id=u.employee_id,
                created_at=u.created_at,
                employee_profile=emp_profile
            )
        )
    return result


@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, role_data: UserRoleUpdate, db: Session = Depends(get_db)):
    """Thay đổi vai trò của tài khoản (admin hoặc employee)"""
    if role_data.role not in ["admin", "employee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vai trò không hợp lệ (chỉ chấp nhận 'admin' hoặc 'employee')"
        )

    user = db.query(Auth).filter(Auth.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài khoản"
        )

    # KHÓA BẢO VỆ: Super Admin là bất khả xâm phạm!
    if user.role == "super_admin" or user.username in ["admin", "root"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không thể thay đổi vai trò của Quản trị viên tối cao (Super Admin)!"
        )

    user.role = role_data.role
    db.commit()
    db.refresh(user)

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
        role=user.role,
        employee_id=user.employee_id,
        created_at=user.created_at,
        employee_profile=emp_profile
    )

