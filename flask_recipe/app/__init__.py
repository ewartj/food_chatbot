import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    from app.query import bp as query_bp
    app.register_blueprint(query_bp)

    from app.intro import bp as intro_bp
    app.register_blueprint(intro_bp)

    if not app.debug and not app.testing:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/chatbot.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Chatbot startup')

    return app