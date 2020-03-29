from fishbase.fish_logger import logger
from fishbase.fish_random import gen_random_str

from .const import ERR_MSG, HTTP_ERROR, VALIDATION_ERROR


class CustomException(Exception):
    status_code = 400

    def __init__(self, return_code=None, status_code=None, msg_dict=None, payload=None):
        Exception.__init__(self)
        self.return_code = return_code
        if status_code is not None:
            self.status_code = status_code
        if msg_dict is not None:
            self.msg_dict = msg_dict
        else:
            self.msg_dict = None
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.return_code
        if self.msg_dict is not None:
            s = ERR_MSG[self.return_code].format(**self.msg_dict)
        else:
            s = ERR_MSG[self.return_code]
        rv['message'] = s
        rv.update({'response_id': gen_random_str(min_length=36, max_length=36, has_letter=True, has_digit=True)})
        s += ' [response_id:{}]'.format(rv['response_id'])
        logger.info(s)
        return rv


def http422_error_handler(req, exc):
    logger.info(f"{req}: {exc}")
    return CustomException(VALIDATION_ERROR)


def http_error_handler(req, exc):
    logger.info(f"{req}: {exc}")
    return CustomException(HTTP_ERROR)
