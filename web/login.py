from fastapi import APIRouter, Body, HTTPException, Request, Form, Depends, Response
from model.user import User, DB_User
from service import user as service
from datetime import timedelta

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


router = APIRouter(prefix = "/login")

#기본값들을 설정한다
templates = Jinja2Templates(directory="templates")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 인증 에러를 쉽게 작성하기위해 에러 함수를 작성한다.
def unauthed():
    raise HTTPException(
        status_code= 401,
        detail = "아이디나 패스워드가 잘못되었습니다.",
        headers = {"WWW-Authenticate" : "Bearer"} 
    )

@router.get("")
@router.get("/", response_class=HTMLResponse)
def get_all(request : Request):
    return templates.TemplateResponse("login.html", {"request" : request})

@router.post("")
@router.post("/", response_class=HTMLResponse)
def create_customer(response : Response, request : Request, user_name = Form(...), user_password = Form(...)):
    # 인증 => 유저존재확인 + 비밀번호 확인의 총체
    user = service.auth_user(user_name, user_password)
    if not user:
        unauthed()

    # 토큰의 만료시간을 설정한다
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # 토큰을 발행한다
    access_token = service.create_access_token(
        data = {"sub" : user.name}, 
        expire = expire
    )
    response = RedirectResponse("/my_food",status_code=302)
    response.set_cookie(key="token", value=access_token)
    return response

@router.post("/create_user", response_class=HTMLResponse)
def create_user(request : Request,
    name = Form(...),
    email = Form(...),
    password = Form(...)):
    service.create_user(DB_User(name = name, email = email, hashed_password= password))
    return templates.TemplateResponse("login.html", {"request" : request})