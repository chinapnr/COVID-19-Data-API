import os

# 接口基本信息
VERSION = os.getenv("VERSION")
API_VERSION = os.getenv("API_VERSION")
PROJECT_NAME = os.getenv("PROJECT_NAME", "Covid")

# 数据库信息
DATABASE_URI = os.getenv("DATABASE_URI")

# 请求头认证信息
HEADER_KEY = os.getenv("HEADER_KEY")

# 邮件 SMTP 信息
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
SENDER = os.getenv("SENDER")
SUBJECT = os.getenv("SUBJECT")
