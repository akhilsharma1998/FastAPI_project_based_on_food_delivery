from pydantic import BaseModel
from typing import Optional

class SignupModel(BaseModel):
    id : Optional[int]
    username : str
    email : str
    passwored : str
    is_active : Optional[bool]
    is_staff : Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example" : {
                "username":"akhil1998",
                "email":"akhil1998@gmail.com",
                "passwored":"sharma123",
                "is_active" : "True",
                "is_staff" : "False"
            }
        }


class Settings(BaseModel):
    authjwt_secret_key = '2e7de04c7c5978fcce1d248e9eb5c8eba1c586c45016d17b878a68035312b4f6'
  

class LoginModel(BaseModel):
    username : str
    passwored : str

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE",
            }
        }

class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }

