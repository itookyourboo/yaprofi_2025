from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


app = FastAPI()


@app.get('/students', response_model=list[schemas.Student])
def get_students(query: str | None = None, db: Session = Depends(get_db)):
    return crud.get_students(db, query=query)


@app.post('/students', response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.create_student(db, student=student)
    if not db_student:
        raise HTTPException(status_code=404)
    return db_student


@app.put('/students/{student_id}', response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id=student_id, student=student)
    if not db_student:
        raise HTTPException(status_code=404)
    return db_student


@app.delete('/students/{student_id}', response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404)
    return db_student


@app.get('/groups', response_model=list[schemas.Group])
def get_groups(query: str | None = None, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, query=query)
    print(groups, groups[0].subGroups)
    return crud.get_groups(db, query=query)


@app.post('/groups', response_model=schemas.GroupShort)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.create_group(db=db, group=group)
    if not db_group:
        raise HTTPException(status_code=404)
    return db_group


@app.get('/groups/{group_id}', response_model=schemas.GroupShort)
def get_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404)
    return db_group


@app.put('/groups/{group_id}', response_model=schemas.GroupShort)
def update_group(group_id: int, group: schemas.GroupUpdate, db: Session = Depends(get_db)):
    db_group = crud.update_group(db, group_id=group_id, group=group)
    if not db_group:
        raise HTTPException(status_code=404)
    return db_group


@app.delete('/groups/{group_id}', response_model=schemas.GroupShort)
def delete_student(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.delete_group(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404)
    return db_group
