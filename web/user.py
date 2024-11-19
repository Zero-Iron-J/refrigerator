from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from model.user import User, DB_User
from service import user as service
from error import Duplicate, Missing

#기본 라우터를 정의한다.
router = APIRouter(prefix="/user")

# JWT에 사용할(넘겨줄) 기본데이터를 설정한다.
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2 = OAuth2PasswordBearer(tokenUrl="/user/token")

# 인증 에러를 쉽게 작성하기위해 에러 함수를 작성한다.
def unauthed():
    raise HTTPException(
        status_code= 401,
        detail = "아이디나 패스워드가 잘못되었습니다.",
        headers = {"WWW-Authenticate" : "Bearer"} 
    )

# OAuth2가 사용할 POST접근을 생성해준다.
@router.post("/token")
async def create_access_token(
    form_data : OAuth2PasswordRequestForm = Depends()
):
    # username과 password를 OAuth양식에서 꺼낸뒤 JWT토큰을 반환한다.
    # 인증 => 유저존재확인 + 비밀번호 확인의 총체
    user = service.auth_user(form_data.username, form_data.password) # 서비스에서 유저를 인증한다

    # 유저가 있으면 유저를 사용하면 되고 없으면? 에러를 발생시킨다.
    if not user:
        unauthed()
    
    # 유저가 존재한다. => 인증완료된 사용자이면 토큰 발급을 진행한다
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data = {"sub" : user.name}, 
        expire = expire
    )
    return {"access_token" : access_token, "token_type" : "bearer"}

# ============== 추가 기능 구현 ============================================
# 유저 데이터 생성
@router.post("/")
def create_user(user : DB_User):
    try:
        return service.create_user(user)
    except Duplicate as E:
        raise HTTPException(status_code=401, detail= E.msg)




