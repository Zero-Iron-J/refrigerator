from pydantic import BaseModel

class User(BaseModel):
    name : str
    email : str

class DB_User(User):
    hashed_password : str