from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    group_id: int


class StudentUpdate(BaseModel):
    name: str
    group_id: int


class Student(BaseModel):
    id: int
    name: str
    group_id: int

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    name: str
    parent_id: int | None = None


class GroupUpdate(BaseModel):
    name: str
    parent_id: int | None


class GroupShort(BaseModel):
    id: int
    name: str
    parent_id: int | None = None

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    name: str
    subGroups: list['Group'] = []

    class Config:
        orm_mode = True
