import time
import uuid
import logging

from analytics.util import get_matching_merchants
from models.merchant import Merchant
from models.user import User
from models.visit import Visit

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("analytics.tasks")


def _create_user_visit(sess, request_id, user_obj_id, merchant_data):
    merchant = Merchant.get_and_check_else_new(sess, merchant_data['merchant_id'], merchant_data['merchant_name'])
    user = User.get_and_check_else_new(sess, user_obj_id)
    visit_id = uuid.uuid4()
    timestamp = int(time.time())
    Visit.new(sess, visit_id, timestamp, user.pk, merchant.pk)
    log.info("[{}] New visit created for user: {}".format(request_id, user.pk))
    return {
        'visitId': visit_id,
        'timestamp': timestamp,
        'merchant': {
            'merchantId': merchant.merchant_id,
            'merchantName': merchant.merchant_name
        },
        'user': {
            'userId': user.user_obj_id
        }
    }


def _get_merchant_visit(sess, request_id, user_id, search_string):
    user = User.get_by_id(sess, user_id)
    visits = sess.query(Visit).filter_by(user_obj_pk=user.pk).all()
    return get_matching_merchants(sess, request_id, user_id, visits, search_string, threshold=80)


def _get_visit_by_id(sess, request_id, visit_id):
    visit = Visit.get_by_id(sess, visit_id)
    merchant = Merchant.get_by_pk(sess, visit.merchant_pk)
    user = User.get_by_pk(sess, visit.user_obj_pk)
    log.info("[{}] Found visit by user: {}".format(request_id, user.pk))
    return {
        'visitId': visit_id,
        'timestamp': visit.timestamp,
        'merchant': {
            'merchantId': merchant.merchant_id,
            'merchantName': merchant.merchant_name
        },
        'user': {
            'userId': user.user_obj_id
        }
    }
