import os

from fishbase import SingleTon, conf_as_dict

basedir = os.path.dirname(__file__)


class CovidConfig(SingleTon):
    dt = dict()

    def __init__(self):
        CovidConfig.get_config_info()

    @staticmethod
    def get_config_info():
        config_path = os.path.join(basedir, "config.conf")
        conf_info_tuple = conf_as_dict(config_path)
        CovidConfig.dt = conf_info_tuple[1] if conf_info_tuple[0] else {}


CovidConfig = CovidConfig()
env_status = CovidConfig.dt["server"]["status"]
conf_info = CovidConfig.dt[env_status]

# 将配置信息和 FastAPI 分开
# 接口基本信息
VERSION = conf_info["version"] or os.getenv("VERSION")
API_VERSION = conf_info["api_version"] or os.getenv("API_VERSION")
PROJECT_NAME = conf_info["project_name"] or os.getenv("PROJECT_NAME", "Covid")

# 数据库信息
DATABASE_URI = conf_info["database_uri"] or os.getenv("DATABASE_URI")

# 请求头认证信息
HEADER_KEY = conf_info["header_key"] or os.getenv("HEADER_KEY")

# 邮件 SMTP 信息
MAIL_HOST = conf_info["mail_host"] or os.getenv("MAIL_HOST")
MAIL_USER = conf_info["mail_user"] or os.getenv("MAIL_USER")
MAIL_PASS = conf_info["mail_pass"] or os.getenv("MAIL_PASS")
MAIL_PORT = conf_info["mail_port"] or os.getenv("MAIL_PORT")
SENDER = conf_info["sender"] or os.getenv("SENDER")
SUBJECT = conf_info["subject"] or os.getenv("SUBJECT")

# 加载本地配置文件
try:
    from .local_config import *
except Exception as _:
    pass
