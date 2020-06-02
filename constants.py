class ExtractRequestFields(object):
    class Input:
        USER = "user"
        REQUEST_ID = "request_id"
        VISIT_ID = "visitorId"
        USER_ID = "userId"
        MERCHANT = "merchant"
        MERCHANT_ID = "merchantId"
        MERCHANT_NAME = "merchantName"


class ExceptionMessage(object):
    BAD_REQUEST = "Input is malformed."


class Threshold(object):
    THRESHOLD = 50
