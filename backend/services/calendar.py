from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Post

async def plan_week(session: AsyncSession, theme: str, channel: str = "linkedin") -> list[Post]:
    llm = get_llm()
    raw = await llm.complete(
        f"Propose 5 content ideas for theme '{theme}' on {channel}. One title per line.",
        system="You are a content strategist. Titles only, no fluff.",
    )
    titles = [ln.strip("-• ").strip() for ln in raw.splitlines() if len(ln.strip()) > 4][:5]
    if not titles:
        titles = [f"{theme} angle {i}" for i in range(1, 6)]
    start = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    created = []
    for idx, title in enumerate(titles):
        slot = (start + timedelta(days=idx)).strftime("%Y-%m-%dT%H:%M:%SZ")
        post = Post(id=uuid.uuid4().hex[:10], title=title[:240], channel=channel, publish_at=slot, body=f"Draft for: {title}", status="planned")
        session.add(post); created.append(post)
    await session.commit()
    return created

async def list_posts(session: AsyncSession) -> list[Post]:
    return list((await session.execute(select(Post).order_by(Post.publish_at.asc()))).scalars())
