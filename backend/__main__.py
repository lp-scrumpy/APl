import logging
from flask import Flask
from backend.views.users import user

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("application started")
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/api/v1/users')
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == '__main__':
    main()