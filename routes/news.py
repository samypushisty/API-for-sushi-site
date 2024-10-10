from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from auth.converter import RequestAnswer
from data_base import get_session
from models.models import News

news = []


async def reload_news_bd_id(session: AsyncSession):
    try:
        global news
        query = select(News.id)
        result = await session.execute(query)
        news = result.scalars().all()[::-1]
    except Exception as e:
        print(e)


news_rout = APIRouter(
    prefix="/commands/news",
    tags=["news"]
)


@news_rout.get("")
async def news_get(news_id: int, session: AsyncSession = Depends(get_session)):
    try:
        query_news = select(News).filter(News.id == news_id)
        result = await session.execute(query_news)
        result = result.scalars().first()
        if result:
            return RequestAnswer(detail=result, status_code=200)
        else:
            return RequestAnswer(detail="None id", status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@news_rout.get("/upload_image")
async def upload_image(news_id: int):
    try:
        # Алекс фотки добавляй в images пример "news_1" где 1 id новости
        file_path = f"images/{"news_"+str(news_id)+".jpg"}"
         # Алекс нужен хеш удОли headers={"Cache-Control": "no-cache, no-store, must-revalidate"
        return FileResponse(file_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")


@news_rout.get("/{page}")
async def eight_news(page: int,
                     session: AsyncSession = Depends(get_session)):
    try:
        if page * 8 - 8 < len(news):
            if page * 8 < len(news):
                first_id = page * 8 - 8
                last_id = page * 8 - 1
            else:
                first_id = page * 8 - 8
                last_id = len(news) - 1

            print(news[first_id:last_id+1])
            query = select(News).filter(News.id.in_(news[first_id:last_id+1]))
            result = await session.execute(query)
            result = result.scalars().all()[::-1]
            return RequestAnswer(detail=result, status_code=200)
        else:
            return RequestAnswer(detail="page not found", status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()
