from dropbox.oauth import BadRequestException
from dropbox.oauth import NotApprovedException
from dropbox.oauth import CsrfException
from flask import jsonify


class APIError(Exception):
    status_code = 400

    def __init__(self, originalException, status_code=None, payload=None):
        Exception.__init__(self)
        self.originalException = originalException
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.originalException.args[0]
        rv['msg'] = ("We apologize for the inconvenience, "
                     "but an error occurred. Please try again.")
        rv['success'] = False
        return rv
