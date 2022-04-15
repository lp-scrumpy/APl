import logging
from http import HTTPStatus
from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from backend.db import db_session
from backend.errors import AppError
from backend.views.users import user
from backend.views.plannings import planning
from backend.views.tasks import task_view

logger = logging.getLogger(__name__)


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def shutdown_session(exception=None):
    db_session.remove()


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("application started")
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/api/v1/users')
    app.register_blueprint(planning, url_prefix='/api/v1/plannings')
    app.register_blueprint(task_view, url_prefix='/api/v1/tasks')

    app.register_error_handler(HTTPException, handle_http_exceptions)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    app.teardown_appcontext(shutdown_session)
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == '__main__':
    main()
