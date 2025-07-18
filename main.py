import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/urls")
async def get_all_urls():
    return {"message": "This will return all URLs"}

@app.get("/urls/{id}")
async def get_single_url(id: str):
    return { "message": id }

@app.post("/urls/add")
async def add_url(title: str, url: str):
    return {title: url}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)