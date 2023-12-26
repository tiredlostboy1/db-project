from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import user, auth, post

app = FastAPI()

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(post.router, tags=['Posts'], prefix='/api/posts')


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}

