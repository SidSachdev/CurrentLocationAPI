from fuzzywuzzy import fuzz

from models.merchant import Merchant

from constants import Threshold
from models.user import User


def get_matching_merchants(sess, request_id, user_id, visits, searchString, threshold=None):
    result = []
    if not threshold:
        threshold=Threshold.THRESHOLD
    for visit in visits:
        merchant = Merchant.get_by_pk(sess, visit.merchant_pk)
        if fuzz.ratio(merchant.merchant_name, searchString) > threshold:
            result.append(
                {
                    'visitId': visit.visit_id,
                    'timestamp': visit.timestamp,
                    'merchant': {
                        'merchantId': merchant.merchant_id,
                        'merchantName': merchant.merchant_name
                    },
                    'user': {
                        'userId': user_id
                    }
                }
            )
    return result
