from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.auth import hash_password
from app.database import get_db
from app.models import Auth, Department, Employee, EmployeeDepartment
from app.schemas import EmployeeCreate, EmployeeDepartmentItem, EmployeeResponse



router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)


def format_employee_response(employee: Employee) -> EmployeeResponse:
    dept_items = []
    for assoc in employee.department_associations:
        if assoc.department:
            dept_items.append(
                EmployeeDepartmentItem(
                    id=assoc.department.id,
                    name=assoc.department.name,
                    assigned_at=assoc.assigned_at
                )
            )
    return EmployeeResponse(
        id=employee.id,
        name=employee.name,
        phone=employee.phone,
        email=employee.email,
        created_at=employee.created_at,
        updated_at=employee.updated_at,
        departments=dept_items
    )


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    employees = (
        db.query(Employee)
        .options(joinedload(Employee.department_associations).joinedload(EmployeeDepartment.department))
        .order_by(Employee.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [format_employee_response(emp) for emp in employees]


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = (
        db.query(Employee)
        .options(joinedload(Employee.department_associations).joinedload(EmployeeDepartment.department))
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy nhân viên"
        )

    return format_employee_response(employee)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    final_username = None
    if employee_data.username:
        base_username = employee_data.username.strip()
        final_username = base_username
        counter = 2
        # Tự động thêm đuôi số (2), (3)... nếu bị trùng username
        while db.query(Auth).filter(Auth.username == final_username).first():
            final_username = f"{base_username} ({counter})"
            counter += 1

    employee = Employee(
        name=employee_data.name,
        phone=employee_data.phone,
        email=employee_data.email
    )

    try:
        db.add(employee)
        db.flush()  # Sinh ra employee.id trước

        # Gán các phòng ban được chọn
        if employee_data.department_ids:
            for dept_id in set(employee_data.department_ids):
                assoc = EmployeeDepartment(
                    employee_id=employee.id,
                    department_id=dept_id
                )
                db.add(assoc)

        # Cấp luôn tài khoản đăng nhập nếu có username và password
        if final_username and employee_data.password:
            new_auth = Auth(
                username=final_username,
                password=hash_password(employee_data.password),
                role="employee",
                employee_id=employee.id
            )
            db.add(new_auth)

        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc số điện thoại đã tồn tại"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi: {str(e)}"
        )

    return format_employee_response(employee)



@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy nhân viên"
        )

    employee.name = employee_data.name
    employee.phone = employee_data.phone
    employee.email = employee_data.email

    try:
        # Cập nhật danh sách phòng ban: xóa các liên kết cũ và gán liên kết mới
        db.query(EmployeeDepartment).filter(EmployeeDepartment.employee_id == employee_id).delete()

        if employee_data.department_ids:
            for dept_id in set(employee_data.department_ids):
                assoc = EmployeeDepartment(
                    employee_id=employee_id,
                    department_id=dept_id
                )
                db.add(assoc)

        # Cấp tài khoản đăng nhập nếu có username và password
        if employee_data.username and employee_data.password:
            existing_auth = db.query(Auth).filter(Auth.username == employee_data.username.strip()).first()
            if existing_auth and existing_auth.employee_id != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tên đăng nhập '@{employee_data.username}' đã có người sử dụng"
                )

            current_auth = db.query(Auth).filter(Auth.employee_id == employee_id).first()
            if current_auth:
                current_auth.username = employee_data.username.strip()
                current_auth.password = hash_password(employee_data.password)
            else:
                new_auth = Auth(
                    username=employee_data.username.strip(),
                    password=hash_password(employee_data.password),
                    role="employee",
                    employee_id=employee_id
                )
                db.add(new_auth)

        db.commit()
        db.refresh(employee)
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc số điện thoại đã tồn tại"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lỗi: {str(e)}"
        )

    return format_employee_response(employee)




@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy nhân viên"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Xóa nhân viên thành công"
    }
