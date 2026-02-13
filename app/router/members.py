from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Member
from app.schema.schemas import MemberCreate, MemberResponse, MemberUpdate

members_router = APIRouter(prefix="/members", tags=["Members"])


@members_router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    query = select(Member)
    members = db.exec(query).all()
    return members


@members_router.get("/{id}", response_model=MemberResponse)
def get_member_by_id(id: int, db: Session = Depends(get_db)):
    member = db.get(Member, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@members_router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@members_router.put("/{id}", response_model=MemberResponse)
def update_member(id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.get(Member, id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = member.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_member, key, value)

    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@members_router.delete("/{id}", status_code=204)
def delete_member(id: int, db: Session = Depends(get_db)):
    member = db.get(Member, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return None
