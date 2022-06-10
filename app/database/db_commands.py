from datetime import date
from constants import (
    COIN_BALANCE_TABLE,
    DEPARTMENT_TABLE,
    EXCHANGE_REQUEST_TABLE,
    EXCHANGE_TYPE_TABLE,
    PRODUCT_DESCRIPTION_TABLE,
    PRODUCT_REQUEST_TABLE,
    PRODUCT_TABLE,
    REQUEST_STATUS_TABLE,
    TRANSFERFACT_TABLE,
    USER_TABLE,
    ROLE_TABLE
)
from schemas import Login, Register
from sqlalchemy import func
from sqlalchemy.future import select
from .models import (
    Product,
    CoinsBalance,
    TransferFact,
    User,
    ExchangeRequest,
    ProductRequest,
    Department,
    ExchangeType,
    ProductDescription,
    RequestStatus,
    Role
)



def register(user: Register) -> str:
    return f""" INSERT INTO {USER_TABLE} (user_nm, email, passwrd,
                dept_id, source_nm, role_id)
                VALUES ('{user.user_nm}',
                '{user.email}',
                '{user.passwd}',
                {user.dept_id},
                '{user.source}',
                1)"""


def login(user: Login) -> str:
    select = f"""SELECT U.user_id, user_nm, email, U.date_ts,
                role_nm AS role, coin_distribute_qty, coin_balance_qty, U.active_ind
                FROM {USER_TABLE} U 
                JOIN {COIN_BALANCE_TABLE} C  USING(user_id)
                JOIN {ROLE_TABLE} R USING(role_id) 
                WHERE C.active_ind = TRUE
                    AND U.EMAIL='{user.email}' 
                    AND U.PASSWRD='{user.passwd}'"""
    return select


# def find_user(user: Login) -> str:
#     return f"SELECT user_id FROM {USER_TABLE} WHERE email='{user.email}'"

def find_user(user: Login) -> str:
    return str(select(User).where(User.email == user.email))


def get_user_by_mail(email: str) -> str:
    select= f"""SELECT user_id, active_ind
                FROM {USER_TABLE}
                WHERE email = '{email}'"""
    return select


# def get_user_info(user_id: int) -> str:
#     select = f"""SELECT user_nm, email, U.date_ts,
#                 role_nm AS role, coin_distribute_qty,
#                 coin_balance_qty, U.active_ind,
#                 'picture_path' as picture_path,
#                 'location' as location
#                 FROM {USER_TABLE} U 
#                 JOIN {COIN_BALANCE_TABLE} C USING(user_id)
#                 JOIN {ROLE_TABLE} R USING(role_id)
#                 WHERE C.active_ind = TRUE 
#                     AND U.user_id = {user_id}
#                     AND U.active_ind = TRUE"""
#     return select

def get_user_info(user_id: int) -> str:
    statement = select(User).join(Role)
    print(statement)
    for i in CoinsBalance.__dict__:
        print(i)
    return


def get_user_struct_info(user_id: int) -> str:
    select = f"""SELECT U1.user_nm, U1.email, U2.user_nm as mngr_nm, dept_nm
                FROM {USER_TABLE} U1
                LEFT JOIN {USER_TABLE} U2 ON U1.mngr_id = U2.user_id 
                JOIN {DEPARTMENT_TABLE} D ON U1.dept_id = D.dept_id
                WHERE U1.user_id = {user_id}"""
    return select


def get_latest_transfers(user_id: int, latest: int) -> str:
    return f"""SELECT U1.user_nm as from_user, U2.user_nm to_user,
                T.coin_qty, T.comment_txt, T.date_ts, T.gift_ind,
                U1.user_id as from_user_id
                FROM {TRANSFERFACT_TABLE} T
                JOIN {USER_TABLE} U1 on T.from_user_id = U1.user_id
                JOIN {USER_TABLE} U2 ON T.to_user_id = U2.user_id
                WHERE from_user_id = {user_id} 
                    OR to_user_id = {user_id}
                ORDER BY date_ts DESC
                LIMIT {latest}"""


def get_transfers(user_id: int,
                  start_date: date = None,
                  end_date: date = None,
                  limit: int | None = None) -> str:
    if limit:
        return get_latest_transfers(user_id, limit)
    select = f"""SELECT U1.user_nm as from_user, U2.user_nm to_user,
                U1.user_id as from_user_id, T.coin_qty,
                T.comment_txt, T.date_ts, T.gift_ind
                FROM {TRANSFERFACT_TABLE} T
                JOIN {USER_TABLE} U1 on T.from_user_id = U1.user_id
                JOIN {USER_TABLE} U2 ON T.to_user_id = U2.user_id
                WHERE (from_user_id = {user_id}
                    OR to_user_id = {user_id}) """
    if start_date:
        select += f"AND date(T.date_ts) >= '{start_date}' "
    if end_date:
        select += f"AND date(T.date_ts) <= '{end_date}' "
    return select


def get_coins_balance(user_id: int) -> str:
    return f"""SELECT COIN_DISTRIBUTE_QTY, COIN_BALANCE_QTY
                FROM {COIN_BALANCE_TABLE} WHERE user_id={user_id} AND active_ind=true"""


def get_department(user_id: int) -> str:
    return f"""SELECT D.DEPT_NM as department FROM {USER_TABLE} U
                LEFT JOIN {DEPARTMENT_TABLE} D on D.DEPT_ID = U.DEPT_ID
                WHERE U.USER_ID = {user_id}"""


def get_manager(user_id: int) -> str:
    return f"""SELECT U2.user_nm as user_nm,
                'picture_path' as picture_path,
                FROM {USER_TABLE} U1
                LEFT JOIN {USER_TABLE} U2 ON U1.mngr_id = U2.user_id 
                WHERE U1.user_id = {user_id}"""


def get_coef() -> str:
    return f"SELECT type_nm, exchange_rate FROM {EXCHANGE_TYPE_TABLE}"


def get_exchange_req(user_id: int, req_id: int = 0, status_id: int = 0) -> str:
    select = f"""SELECT type_nm as type, req_id, req_ts, status_nm,
                    answer_ts, link, comment_txt,
                    answer_comment_txt, coin_qty as price_coin,
                    cash_qty as price_usd 
                FROM {EXCHANGE_REQUEST_TABLE} ER 
                JOIN {REQUEST_STATUS_TABLE} RS ON ER.status_id = RS.status_id
                JOIN {EXCHANGE_TYPE_TABLE} ET ON ER.type_id = ET.type_id
                WHERE user_id = {user_id}
                    AND ER.active_ind = true"""
    if req_id:
        return select + f"AND req_id = {req_id}"
    if status_id:
        return select + f"AND ER.status_id = {status_id} "
    return select


def get_product_req(user_id: int, req_id: int = 0, status_id: int = 0) -> str:
    select = f"""SELECT 'Product' as type, req_id, P.product_id, PD.title_txt as title,
                    price_amt, req_ts, status_nm,
                    answer_ts, product_qty, comment_txt,
                    answer_comment_txt, coin_total_qty as price_coin,
                    cash_total_qty as price_usd 
                FROM {PRODUCT_REQUEST_TABLE} AS PR
                JOIN {REQUEST_STATUS_TABLE} AS RS ON PR.status_id = RS.status_id
                JOIN {PRODUCT_TABLE} AS P on P.product_id = PR.product_id
                JOIN {PRODUCT_DESCRIPTION_TABLE} AS PD ON PD.vendor_code_txt = P.vendor_code_txt
                WHERE user_id = {user_id}
                    AND PR.active_ind = TRUE"""
    if req_id:
        return select + f"AND req_id = {req_id} "
    if status_id:
        return select + f"AND PR.status_id = {status_id} "
    return select


def get_product_req_account_statement(user_id: int,
                                      start_date: date = None,
                                      end_date: date = None,
                                      limit: int | None = None) -> str:
    select = f"""
        WITH req as (
            SELECT req_id, product_id, comment_txt, answer_comment_txt,
                status_id, coin_total_qty as coins, 'product' as type,
                CASE WHEN status_id = 1 THEN req_ts
                    ELSE answer_ts
                END as req_ts_res
            FROM {PRODUCT_REQUEST_TABLE}
            WHERE user_id = {user_id})
        SELECT *
        FROM req
        WHERE req.status_id in (1, 3) """
    
    if start_date:
        select += f"AND date(req.req_ts_res) >= '{start_date}' "
    if end_date:
        select += f"AND date(req.req_ts_res) <= '{end_date}' "
    if limit:
        return select + f"ORDER BY req.req_ts_res DESC LIMIT {limit}"
    return select


def get_exchange_req_account_statement(user_id: int,
                                       start_date: date = None,
                                       end_date: date = None,
                                       limit: int | None = None) -> str:
    select = f"""
        WITH req as (
            SELECT req_id, comment_txt, answer_comment_txt,
                status_id, coin_qty as coins, type_nm as type,
                CASE WHEN status_id = 1 THEN req_ts
                    ELSE answer_ts
                END as req_ts_res
            FROM {EXCHANGE_REQUEST_TABLE} ER
            JOIN {EXCHANGE_TYPE_TABLE} ET ON ER.type_id = ET.type_id
            WHERE user_id = {user_id})
        SELECT *
        FROM req
        WHERE status_id in (1, 3) """
    
    if start_date:
        select += f"AND date(req.req_ts_res) >= '{start_date}' "
    if end_date:
        select += f"AND date(req.req_ts_res) <= '{end_date}' "
    if limit:
        return select + f"ORDER BY req.req_ts_res DESC LIMIT {limit}"
    return select


def get_user_manager_email(dept_id: int) -> str:
    return f""" SELECT email as mngr_email
                FROM {USER_TABLE}
                WHERE dept_id = {dept_id}
                    AND role_id = 2"""


def get_best_friend(user_id: int):
    return f""" SELECT from_user_id, SUM(coin_qty) AS coins
                FROM {TRANSFERFACT_TABLE}
                WHERE to_user_id = {user_id}
                GROUP BY from_user_id"""
                
                
def get_name_from_id(user_id: int) -> str:
    return f"""SELECT user_nm FROM {USER_TABLE} WHERE user_id = {user_id}"""