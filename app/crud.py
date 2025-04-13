from sqlalchemy.orm import Session

from app import models, schemas


def get_students(db: Session, query: str | None = None) -> list[models.Student]:
    queryset = db.query(models.Student)
    if not query:
        return queryset.all()

    return queryset.join(models.Group).filter(
        models.Student.name.ilike(f'%{query}%') |
        models.Group.name.ilike(f'%{query}%')
    ).all()


def get_student(db: Session, student_id: int) -> models.Student | None:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student | None:
    if not get_group(db, student.group_id):
        return None

    db_student = models.Student(
        name=student.name,
        email=student.email,
        group_id=student.group_id,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    if not get_group(db, student.group_id):
        return None

    db_student.name = student.name
    db_student.group_id = student.group_id
    db_student.commit()
    db_student.refresh()
    return db_student


def delete_student(db: Session, student_id: int) -> models.Student | None:
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student


def get_groups(db: Session, query: str | None = None) -> list[models.Group]:
    queryset = db.query(models.Group)
    if not query:
        return queryset.all()

    return queryset.filter(models.Group.name.ilike(f'%{query}%')).all()


def get_group(db: Session, group_id: int) -> models.Group | None:
    return (
        db.query(models.Group)
        .filter(models.Group.id == group_id)
        .first()
    )


def create_group(db: Session, group: schemas.GroupCreate) -> models.Group | None:
    if group.parent_id and not get_group(db, group.parent_id):
        return None

    db_group = models.Group(
        name=group.name,
        parent_id=group.parent_id,
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(db: Session, group_id: int, group: schemas.GroupUpdate) -> models.Group | None:
    db_group = get_group(db, group_id)
    if not db_group:
        return None

    if group.parent_id and not get_group(db, group.parent_id):
        return None

    db_group.name = group.name
    db_group.parent_id = group.parent_id
    db.commit()
    db.refresh(db_group)

    return db_group


def delete_group(db: Session, group_id: int) -> models.Group | None:
    db_group = get_group(db, group_id)
    if not db_group:
        return None

    if db_group.subGroups:
        return None

    db.delete(db_group)
    db.commit()
    return db_group
