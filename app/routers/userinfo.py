from datetime import date
from heapq import merge
import database.db_commands as db_commands
from constants import SORT_ORDER, STATUS_CODES
from fastapi import APIRouter, Query, Security
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials as HAC, HTTPBearer
from jwt_token import id_from_access_token
from schemas import (
    CoinsBalances,
    CoinsCoefficient,
    Department,
    ExchangeRequest,
    Info,
    Manager,
    ProductRequest,
    SortOrder,
    Transaction,
    Transfer,
    BestFriend
)
import sqlalchemy


router = APIRouter()
security = HTTPBearer()
WALLET = {0: 'Distribute', 1: 'Balance'}


def request_process(requests: list) -> list:
    for i, request in enumerate(requests):
        comment = (
            request["comment_txt"] if request["status_id"] == 1
            else request["answer_comment_txt"]
        )
        coins = (
            -request["coins"] if request["status_id"] == 1
            else request["coins"]
        )

        requests[i] = {
            "coins": coins,
            "ts": request['req_ts_res'],
            "info": {
                "comment": comment
            },
            "type": request["type"].lower()
        }
    return requests


def transfer_process(transfers: list, user_id: int) -> list:
    for i, transfer in enumerate(transfers):
        info = {
            "comment": transfer["comment_txt"]
        }
        if transfer["from_user_id"] == user_id:
            info["user"] = transfer["to_user"]
            coins = -transfer["coin_qty"]
            info["wallet"] = WALLET[transfer["gift_ind"]]
        else:
            info["user"] = transfer["from_user"]
            coins = transfer["coin_qty"]
            info["wallet"] = WALLET[0] if transfer["from_user_id"] == 9999 else WALLET[1]
        transfers[i] = {
            "coins": coins,
            "ts": transfer["date_ts"],
            "info": info,
            "type": "transfer"
        }

    return transfers


@router.get("/userinfo/transactions", response_model=list[Transaction])
async def get_transactions(reverse: bool = True,
                           start_date: date | None = None,
                           end_date: date | None = None,
                           limit: int | None = None,
                           credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)

    transfers = await database_instance.fetchall(
        db_commands.
        get_transfers(user_id, start_date, end_date, limit))
    product_requests = await database_instance.fetchall(
        db_commands.
        get_product_req_account_statement(user_id, start_date, end_date, limit))
    exchange_requests = await database_instance.fetchall(
        db_commands.
        get_exchange_req_account_statement(user_id, start_date, end_date, limit))

    product_requests = request_process(product_requests)
    exchange_requests = request_process(exchange_requests)
    transfers = transfer_process(transfers, user_id)

    product_requests.sort(key=lambda x: x["ts"])
    exchange_requests.sort(key=lambda x: x["ts"])
    transfers.sort(key=lambda x: x["ts"])
    result = list(
        merge(
            transfers,
            merge(
                exchange_requests,
                product_requests,
                key=lambda x: x["ts"]),
            key=lambda x: x["ts"]))
    if reverse:
        result.reverse()
    if limit:
        return result[:limit]
    return result


@router.get("/userinfo/info", response_model=Info | None)
async def get_user_info(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_user_info(user_id))


@router.get("/userinfo/transfers", response_model=list[Transfer])
async def get_transfers_by_period(start_date: date | None = None,
                                  end_date: date | None = None,
                                  limit: int | None = None,
                                  credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    if limit:
        return await database_instance.fetchall(
            db_commands.get_transfers(user_id, limit=limit))
    result = await database_instance.fetchall(
        db_commands.get_transfers(user_id, start_date, end_date))
    result.sort(key=lambda x: x["date_ts"], reverse=True)
    return result


@router.get("/userinfo/coins", response_model=CoinsBalances)
async def get_coins_balance(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_coins_balance(user_id))


@router.get("/userinfo/coins-coefficients", response_model=CoinsCoefficient)
async def get_coefficients_coins(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    coins = await database_instance.fetchrow(db_commands.get_coins_balance(user_id))
    coefficients = await database_instance.fetchall(db_commands.get_coef())
    return jsonable_encoder({"coins": coins,
                             "coefficients": dict(coefficients)})


@router.get("/userinfo/department", response_model=Department)
async def get_department(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_department(user_id))


@router.get("/userinfo/manager", response_model=Manager)
async def get_manager(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_manager(user_id))


@router.get("/userinfo/requests/products", response_model=list[ProductRequest])
async def get_product_requests(status_id: int = Query(default=0, description=STATUS_CODES),
                               credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchall(
        db_commands.get_product_req(user_id, status_id=status_id))


@router.get("/userinfo/requests/product/{req_id}", response_model=ProductRequest)
async def get_product_request(req_id: int,
                              credentials: HAC = Security(security)):
    if req_id <= 0:
        return None
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_product_req(user_id, req_id=req_id))


@router.get("/userinfo/requests/exchanges", response_model=list[ExchangeRequest])
async def get_exchange_requests(status_id: int = Query(default=0, description=STATUS_CODES),
                                credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchall(
        db_commands.get_exchange_req(user_id, status_id=status_id))


@router.get("/userinfo/requests/exchange/{req_id}", response_model=ExchangeRequest)
async def get_exchange_requests(req_id: int,
                                credentials: HAC = Security(security)):
    if req_id <= 0:
        return None
    user_id = id_from_access_token(credentials)
    return await database_instance.fetchrow(
        db_commands.get_exchange_req(user_id, req_id=req_id))


@router.get("/userinfo/orders",
            response_model=list[ExchangeRequest | ProductRequest])
async def get_request_orders(status_id: int = Query(default=0,
                                                    description=STATUS_CODES),
                             sort_order: SortOrder = Query(default="req_ts",
                                                           description=SORT_ORDER),
                             reverse: bool = Query(default=True),
                             credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials)
    exchanges = await database_instance.fetchall(
        db_commands.get_exchange_req(user_id, status_id=status_id)
    )
    products = await database_instance.fetchall(
        db_commands.get_product_req(user_id, status_id=status_id)
    )
    orders = exchanges + products
    orders.sort(key=lambda x: x[sort_order], reverse=reverse)
    return orders


@router.get("/userinfo/best-friends", response_model=BestFriend | None)
async def get_best_friend(credentials: HAC = Security(security)):
    user_id = id_from_access_token(credentials) 
    friends = await database_instance.fetchall(
        db_commands.get_best_friend(user_id)
    )
    friends = [dict(friend) for friend in friends]
    best_friend = max(friends, key=lambda x: x["coins"])
    best_friend_id = best_friend.pop("from_user_id")
    name = await database_instance.fetchval(
        db_commands.get_name_from_id(best_friend_id)
    )
    best_friend["user_nm"] = name
    return best_friend
    
    