import time
import logging
import newrelic.agent


from flask import Flask, request, jsonify, Response
import uuid

from flask_sqlalchemy import SQLAlchemy
from voluptuous import Invalid

from analytics.tasks import _create_user_visit, _get_visit_by_id, _get_merchant_visit
from constants import ExceptionMessage
from validator.request_validator import (
    validate_extract_create_user_visit_input,
    validate_extract_all_user_visit_input,
    validate_extract_get_visit_input
)
from database import metadata, get_db_session

app = Flask(__name__)

db = SQLAlchemy(metadata=metadata)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("app.py")


@app.route('/healthz')
def healthz():
    return 'Health Check Complete'


@app.route('/ready')
def ready():
    return 'Ready Check Complete'


@app.route('/api/v1/users/<user_id>/visits', methods=['POST'])
@newrelic.agent.function_trace()
def create_user_visit(user_id):
    request_id = uuid.uuid4()
    try:
        # data = validate_extract_create_user_visit_input(request)
        log.info("[{}] User visits requested for user: {}".format(request_id, user_id))
        return jsonify(_create_user_visit(get_db_session(), request_id, user_id, request.json['merchant']))
    except Invalid as e:
        log.warning("[{}] Malformed input: {}".format(request_id, str(e)))
        return Response(ExceptionMessage.BAD_REQUEST, status=406)


@app.route('/api/v1/users/<user_id>/visits', methods=['GET'])
@newrelic.agent.function_trace()
def get_merchant_visit(user_id):
    request_id = uuid.uuid4()
    try:
        # data = va
        # lidate_extract_all_user_visit_input(request)
        log.info("[{}] User visits requested for user: {}".format(request_id, user_id))
        return jsonify(_get_merchant_visit(get_db_session(), request_id, user_id, request.args.get('searchString')))
    except Invalid as e:
        log.warning(" Malformed input: {}".format(str(e)))
        return Response(ExceptionMessage.BAD_REQUEST, status=406)


@app.route('/api/v1/visit/<visit_id>', methods=['GET'])
@newrelic.agent.function_trace()
def get_single_visit_by_id(visit_id):
    request_id = uuid.uuid4()
    try:
        # data = validate_extract_get_visit_input(request)
        log.info("[{}] User visits requested for visit ID: {}".format(request_id, visit_id))
        return jsonify(_get_visit_by_id(get_db_session(), request_id, visit_id))
    except Invalid as e:
        log.warning(" Malformed input: {}".format(str(e)))
        return Response(ExceptionMessage.BAD_REQUEST, status=406)

