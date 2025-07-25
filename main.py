import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session, select
from db import get_session

from models.urls import Urls

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
	allow_headers=['*']
)

# READ data (CRUD)
@app.get("/")
async def root():
    return {"message": "ShrinkRay API"}

@app.get("/urls")
async def get_all_urls(session: Session = Depends(get_session)):
    statement = select(Urls)
    results = session.exec(statement).all()
    return results

@app.get("/urls/{id}")
async def get_single_url(id: str, session: Session = Depends(get_session)):
	statement = select(Urls).where(Urls.id == id)
	result = session.exec(statement).one()
	return result

# CREATE data (CRUD)
@app.post("/urls/add")
async def add_url(
    payload: Urls, session: Session = Depends(get_session)
    ):
    new_url = Urls(
         title=payload.title,
         long_url=payload.long_url,
         short_url=payload.short_url,
         user_id=payload.user_id
	)
    session.add(new_url)
    session.commit()
    session.refresh(new_url) # Allows getting update value instantly
    return {"message": f"Added new url with ID: {new_url.id}"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)