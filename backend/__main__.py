import logging
from http import HTTPStatus

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from backend.errors import AppError
from backend.views.users import user

logger = logging.getLogger(__name__)


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("application started")
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/api/v1/users')
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == '__main__':
    main()
