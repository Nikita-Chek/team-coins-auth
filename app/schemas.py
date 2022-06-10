from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from email.mime import base
from enum import Enum
from typing import Union
from pydantic import BaseModel

class Coins(BaseModel):
    coin_balance_qty: Decimal
    to_ts: datetime


class Token(BaseModel):
    access_token: str = ""


class Source(str, Enum):
    telegram = "TELEGRAM"
    mobile = "MOBILE"
    web = "WEB"


class SortOrder(str, Enum):
    req_ts = "req_ts"
    price_coin = "price_coin"


class Register(BaseModel):
    email: str | None
    user_nm: str
    passwd: str
    dept_id: int | None
    source: Source


class Info(BaseModel):
    user_nm: str
    email: str
    role: str
    date_ts: datetime
    coin_distribute_qty: Decimal
    coin_balance_qty: Decimal
    active_ind: bool
    picture_path: str | None
    location: str | None


class Login(BaseModel):
    email: str = 'johndoe@ibagroup.eu'
    passwd: str = 'qwerty'


class LoginReturn(Info):
    tokens: dict


class Message(BaseModel):
    detail: str | None


class Department(BaseModel):
    department: str | None


class CoinsBalances(BaseModel):
    coin_balance_qty: Decimal
    coin_distribute_qty: Decimal


class CoinsCoefficient(BaseModel):
    coins: CoinsBalances
    coefficients: dict


class Manager(BaseModel):
    user_nm: str | None
    picture_path: str | None


class Transfer(BaseModel):
    from_user: str
    to_user: str
    coin_qty: Decimal
    gift_ind: bool
    comment_txt: str
    date_ts: datetime


class Transaction(BaseModel):
    coins: Decimal
    ts: datetime
    info: dict
    type: str


class ProductRequest(BaseModel):
    type: str
    req_id: int
    product_id: int
    title: str
    req_ts: datetime
    status_nm: str
    answer_ts: datetime | None
    product_qty: int
    comment_txt: str | None
    answer_comment_txt: str | None
    price_coin: Decimal
    price_usd: Decimal


class ExchangeRequest(BaseModel):
    type: str
    req_id: int
    req_ts: datetime
    status_nm: str
    answer_ts: datetime | None
    link: str
    comment_txt: str | None
    answer_comment_txt: str | None
    price_coin: Decimal
    price_usd: Decimal


class EmailBody(BaseModel):
    user_nm: str
    dept_nm: str
    mngr_nm: str

class Msg(BaseModel):
    topic: str
    message: str

class SupportBody(BaseModel):
    info: dict[str, EmailBody]
    content: dict[str, Msg]


class BestFriend(BaseModel):
    user_nm: str
    picture_path: str | None
    coins: Decimal  