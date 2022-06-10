SCHEME = "\"COIN_DB\"."
USER_TABLE = SCHEME + "USER_ACCOUNT"
TRANSFERFACT_TABLE = SCHEME + "TRANSFER_FACT"
DEPARTMENT_TABLE = SCHEME + "DEPT"
COIN_BALANCE_TABLE = SCHEME + "COIN_BALANCE"
ROLE_TABLE = SCHEME + "ROLE"
EXCHANGE_TYPE_TABLE = SCHEME + "EXCHANGE_TYPE"
EXCHANGE_REQUEST_TABLE = SCHEME + "EXCHANGE_REQ"
PRODUCT_TABLE = SCHEME + "PRODUCT"
PRODUCT_REQUEST_TABLE = SCHEME + "PRODUCT_REQ"
REQUEST_STATUS_TABLE = SCHEME + "REQ_STATUS"
PRODUCT_DESCRIPTION_TABLE = SCHEME + "PRODUCT_DESCRiPTION"
ROLE_TABLE = SCHEME + "ROLE"

ADMIN_EMAIL = "team.coins.iba@gmail.com"
ADMIN_PASS = "wqsddjgorqnbyyyq"

LAST_TRANSACTIONS = 5
TOP_USERS = 5
STATUS_CODES = """0 - all,
1 - under consideration,
2 - approved,
3 - rejected,
4 - delivered
"""
SORT_ORDER = "Sort by req_ts, price_coin"

PURCHASE_REASON = {
    "exchange": {
        1: "exchange request created",
        3: "exchange request rejected"
    },
    "product": {
        1: "product purchase created",
        3: "product purchase rejected"
    }
}
