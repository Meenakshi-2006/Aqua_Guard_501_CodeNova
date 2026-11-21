
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "The requested API endpoint does not exist."
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.exception("Internal server error")
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "Something went wrong on the server."
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "The request contains invalid data."
        }), 400
