import os

# 邮件信息
EMAIL_HEADER = "Welcome to chinapnr/COVID-19-Data-API project"
EMAIL_CONTENT = """
Welcome to chinapnr/COVID-19-Data-API project.

Your API Key:
{_Token}

Documentation :  https://covid-19.adapay.tech/redoc

Swagger APIs : https://covid-19.adapay.tech/docs

Source code : https://github.com/chinapnr/COVID-19-Data-API
"""

# 接口基本信息
VERSION = os.getenv("VERSION")
API_VERSION = os.getenv("API_VERSION")
PROJECT_NAME = os.getenv("PROJECT_NAME", "COVID-19 Data API")

# 数据库信息
DATABASE_URI = os.getenv("DATABASE_URI")

# 请求头认证信息
HEADER_KEY = os.getenv("HEADER_KEY")

# 邮件 SMTP 信息
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")
MAIL_PORT = int(os.getenv("MAIL_PORT") or 465)
SENDER = os.getenv("SENDER")
SUBJECT = EMAIL_HEADER or os.getenv("SUBJECT")

try:
    from .local_config import *
except Exception as e:
    pass
