from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import calendar as svc

class PlanIn(BaseModel):
    theme: str = Field(min_length=2)
    channel: str = "linkedin"

router = APIRouter()

@router.get("")
async def list_posts(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_posts(db)
    return {"posts": [{"id": p.id, "title": p.title, "channel": p.channel, "publish_at": p.publish_at, "status": p.status} for p in rows]}

@router.post("/plan-week")
async def plan_week(payload: PlanIn, db: AsyncSession = Depends(get_db)):
    rows = await svc.plan_week(db, payload.theme, payload.channel)
    return {"created": len(rows), "posts": [{"id": p.id, "title": p.title, "publish_at": p.publish_at} for p in rows]}
