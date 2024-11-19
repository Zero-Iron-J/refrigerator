from fastapi import APIRouter, Body, Request, Form
from model.my_food import Food
import service.my_food as service
import service.user as user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

router = APIRouter(prefix = "/my_food")
#기본 템플릿 위치를 지정합니다
templates = Jinja2Templates(directory="templates")

@router.get("")
@router.get("/", response_class=HTMLResponse)
def get_all(request : Request):
    
    # 클라이언트가 보낸 토큰을 가져온다
    token = request.cookies["token"]
    user_name = user.get_current_user(token)
    if user_name:
        foods = service.get_food(user_name)
        return templates.TemplateResponse("index.html", {"request" : request, "foods" : foods})
    else:
        unauthed()

@router.post("/")
def create_customer(request : Request,
    food_name = Form(...),
    quantity = Form(...),
):  
    # 클라이언트가 보낸 토큰을 가져온다
    token = request.cookies["token"]

    # 토큰의 유효성을 판단한다
    if user_name:=user.get_current_user(token):
        service.create_food( Food(food_name =food_name, quantity = quantity, user = user_name) )
        return RedirectResponse("/my_food",status_code=302)
    else:
        unauthed()


@router.post("/update", response_class=HTMLResponse)
def modify_food(request : Request,
    food_name = Form(...),
    quantity = Form(...),
    ):
    # 클라이언트가 보낸 토큰을 가져온다
    token = request.cookies["token"]

    # 토큰의 유효성을 판단한다
    if user_name:=user.get_current_user(token):
        service.modify_food(Food(food_name = food_name, quantity = quantity, user = user_name))
        return RedirectResponse("/my_food",status_code=302)
    else:
        unauthed()

@router.post("/delete", response_class=HTMLResponse)
def delete_customer(request : Request,
    food_name = Form(...)):
    
    # 클라이언트가 보낸 토큰을 가져온다
    token = request.cookies["token"]

    # 토큰의 유효성을 판단한다
    if user.get_current_user(token):
        service.delete_food(food_name)
        return RedirectResponse("/my_food",status_code=302)
    else:
        unauthed()