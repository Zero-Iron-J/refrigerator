from pydantic import BaseModel

class Food(BaseModel):
    food_name : str
    quantity : int | float
    user : str