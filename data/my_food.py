from model.my_food import Food
import sqlite3
from .init import conn, curs

curs.execute(""" create table if not exists refrigerator(
    food_name text primary key,
    quantity int,
    user forigen key references user(name)
    )"""
    )

# 데이터 변환에 사용할 함수들
def row_to_model(row : tuple) -> Food:
    food_name, quantity, user = row
    return Food(
        food_name = food_name,
        quantity = quantity,
        user = user
    )

def model_to_dict(food : Food) -> dict:
    return food.model_dump()

# CRUD 구현
    
def get_food(user_name) -> list[Food]:
    sql = "SELECT * FROM refrigerator WHERE user = :user"
    params = {"user" : user_name}
    curs.execute(sql, params)
    datas = curs.fetchall()
    return [row_to_model(data) for data in datas]

def create_food(food : Food):
    sql = "INSERT INTO refrigerator (food_name, quantity, user)  values (:food_name, :quantity, :user)"
    params = model_to_dict(food)
    curs.execute(sql, params)
    conn.commit()

def modify_food(food : Food):
    sql = "UPDATE refrigerator set food_name=:food_name, quantity=:quantity WHERE food_name=:food_name"
    params = model_to_dict(food)
    curs.execute(sql, params)
    conn.commit()

def delete_food(food_name : str):
    sql = "DELETE FROM refrigerator WHERE food_name = :food_name"
    params = {"food_name" : food_name}
    curs.execute(sql, params)
    conn.commit()
    