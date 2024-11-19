from data import my_food as data
from model.my_food import Food


def get_food(user_name) -> list[Food]:
    return data.get_food(user_name)

def create_food(food : Food) -> Food:
    return data.create_food(food)

def modify_food(food : Food) -> Food:
    return data.modify_food(food)

def delete_food(food_name : str):
    return data.delete_food(food_name)
    