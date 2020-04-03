from fishbase.fish_logger import logger
from fishbase.fish_random import gen_random_str

from .const import ERR_MSG


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

    def to_dict(self, custom_response_id=None):
        rv = dict(self.payload or ())
        rv['code'] = self.return_code
        if self.msg_dict is not None:
            s = ERR_MSG[self.return_code].format(**self.msg_dict)
        else:
            s = ERR_MSG[self.return_code]
        rv['message'] = s
        if custom_response_id:
            rv.update({'response_id': custom_response_id})
        else:
            rv.update({'response_id': gen_random_str(min_length=36, max_length=36, has_letter=True, has_digit=True)})
        s += ' [response_id:{}]'.format(rv['response_id'])
        logger.info(s)
        return rv
