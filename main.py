#필수 프레임워크를 가져온다.
from fastapi import FastAPI
import uvicorn

# 여기서부터 파일 import
from web import my_food
from web import user
from web import login

# app을 실행한다.
app = FastAPI()

# 이부분에 web에 작성된 router를 연결한다.
app.include_router(my_food.router)
app.include_router(user.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)