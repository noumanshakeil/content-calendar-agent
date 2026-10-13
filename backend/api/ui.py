from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import calendar as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Content Calendar Agent", "posts": await svc.list_posts(db)})

@router.post("/ui/plan")
async def ui_plan(theme: str = Form(...), channel: str = Form("linkedin"), db: AsyncSession = Depends(get_db)):
    await svc.plan_week(db, theme, channel)
    return RedirectResponse("/", status_code=303)
