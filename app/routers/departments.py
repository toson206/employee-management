from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Department, EmployeeDepartment
from app.schemas import DepartmentCreate, DepartmentMemberItem, DepartmentResponse

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"]
)


def format_department_response(dept: Department) -> DepartmentResponse:
    members = []
    for assoc in dept.employee_associations:
        if assoc.employee:
            members.append(
                DepartmentMemberItem(
                    id=assoc.employee.id,
                    name=assoc.employee.name,
                    phone=assoc.employee.phone,
                    email=assoc.employee.email,
                    assigned_at=assoc.assigned_at
                )
            )
    return DepartmentResponse(
        id=dept.id,
        name=dept.name,
        description=dept.description,
        created_at=dept.created_at,
        members_count=len(members),
        members=members
    )


@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả các phòng ban kèm danh sách nhân viên"""
    depts = (
        db.query(Department)
        .options(joinedload(Department.employee_associations).joinedload(EmployeeDepartment.employee))
        .order_by(Department.id)
        .all()
    )
    return [format_department_response(d) for d in depts]


@router.get("/{dept_id}", response_model=DepartmentResponse)
def get_department(dept_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết một phòng ban"""
    dept = (
        db.query(Department)
        .options(joinedload(Department.employee_associations).joinedload(EmployeeDepartment.employee))
        .filter(Department.id == dept_id)
        .first()
    )
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng ban"
        )
    return format_department_response(dept)


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(dept_data: DepartmentCreate, db: Session = Depends(get_db)):
    """Thêm một phòng ban mới"""
    existing = db.query(Department).filter(Department.name == dept_data.name.strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Phòng ban '{dept_data.name}' đã tồn tại"
        )

    dept = Department(
        name=dept_data.name.strip(),
        description=dept_data.description
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return format_department_response(dept)


@router.put("/{dept_id}", response_model=DepartmentResponse)
def update_department(dept_id: int, dept_data: DepartmentCreate, db: Session = Depends(get_db)):
    """Cập nhật thông tin phòng ban"""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng ban"
        )

    existing = db.query(Department).filter(Department.name == dept_data.name.strip(), Department.id != dept_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Phòng ban tên '{dept_data.name}' đã tồn tại"
        )

    dept.name = dept_data.name.strip()
    dept.description = dept_data.description
    db.commit()
    db.refresh(dept)
    return format_department_response(dept)


@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    """Xóa một phòng ban"""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy phòng ban"
        )

    db.delete(dept)
    db.commit()
    return {"message": "Xóa phòng ban thành công"}


@router.delete("/{dept_id}/members/{employee_id}")
def remove_employee_from_department(dept_id: int, employee_id: int, db: Session = Depends(get_db)):
    """Gỡ một nhân viên ra khỏi phòng ban cụ thể"""
    assoc = (
        db.query(EmployeeDepartment)
        .filter(
            EmployeeDepartment.department_id == dept_id,
            EmployeeDepartment.employee_id == employee_id
        )
        .first()
    )
    if not assoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhân viên này không thuộc phòng ban đã chọn"
        )

    db.delete(assoc)
    db.commit()
    return {"message": "Đã gỡ nhân viên ra khỏi phòng ban thành công"}


