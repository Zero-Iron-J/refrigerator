from datetime import timedelta, datetime
from jose import jwt
import bcrypt
from data import user as data
from model.user import User, DB_User
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

# 시크릿 키를 설정
SECRET_KEY = "E9763BAC645EA54C7E8B06302635861CF95A99470A22C0A0CF9F92A5A8DC1F40"
ALGORITHM = "HS256"
oauth2 = OAuth2PasswordBearer(tokenUrl="/user/token")

# =========== 지원을 위한 기능들 ==============
# 유저를 찾는 기능
def find_user(username):
    # 데이터 계층에게 유저를 찾아오게 시킴
    # 유저가 없다면 None을 반환한다
    if (user := data.find_user(username)):
        return user
    return None
# 비밀번호를 확인하는 기능
def verify_password(password : str, hashed_password : str):
    password = password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    is_valid = bcrypt.checkpw(password, hashed_password)
    return is_valid

# 비밀번호를 해시하는 기능
def make_hash_password(password : str):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode("utf-8")


# +++++++++++ POST token ++++++++++++++++++++++++++++
def auth_user(username, password):
    # 유저를 확인한다
    user = find_user(username)
    if not user:
        return None
    # 비밀번호를 확인한다
    passsword_check = verify_password(password, user.hashed_password)
    if not passsword_check:
        return None
    # 둘다 확인이 끝난 정상 유저를 반환한다
    return user

def create_access_token(data : dict, expire : timedelta):
    data = data.copy()
    now = datetime.utcnow()
    data.update({"exp" : now + expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ++++++++++++ CRUD +++++++++++++++
# 조회는 상단에 find_user를 참조

def create_user(user : DB_User):
    user = DB_User(name = user.name, email = user.email, hashed_password = make_hash_password(user.hashed_password))
    return data.create_user(user)

# +++++++ 추가 기능 구현 ++++++++++++++++++++++++++++

# 유저를 검색한다


#   토큰을 분해한다
def decode_token(token : str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    if not (username := payload.get("sub")):
        return None
    return username

#   유저를 가져온다
def get_current_user(token:str):
    # 토큰을 분해하는 친구에게 분해를 요청하고
    username = decode_token(token)
    user = find_user(username)
    if not user:
        raise HTTPException(
            status_code= 401,
            detail = "올바르지 않은 인증 정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    # 분해가 된 데이터를 이용하여 유저의 정보를 가져온다.
    return user.name
#   가짜 DB에서 게시판 이용가능 여부를 확인한다
# fake_db
_fake_db = {"spongebob" : True, "jane" : False}

def check_usable(token : str):
    username = get_current_user(token)
    # 게시판 접근 여부를 조회했다(인가된 사항을 검토했다 가정)
    if _fake_db[username] :
        return True
    return False

#   게시판에 접근가능한 유저인지 결과를 web에 전송한다
def check_user(token:str):
    check = check_usable(token)
    return check