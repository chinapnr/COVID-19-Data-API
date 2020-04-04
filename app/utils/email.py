import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from fishbase.fish_logger import logger

from app.config.config import MAIL_HOST, MAIL_PASS, MAIL_USER, SUBJECT, SENDER, MAIL_PORT
from app.utils.singleTon import Singleton


@Singleton
class EmailUtils:
    def check_email(self, email):
        """
        校验邮箱格式
        :param email: email
        :return: bool
        """
        expression = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        return True if re.match(expression, email) else False

    def send_mail(self, msg, adds):
        """
        发送邮件
        :param msg: 邮件内容
        :param adds: 收件人信息
        :return: bool
        """
        receivers = adds
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(SENDER, 'utf-8')
        message['To'] = Header("", 'utf-8')
        subject = SUBJECT
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtp = smtplib.SMTP_SSL(host=MAIL_HOST)
            smtp.connect(MAIL_HOST, MAIL_PORT)
            smtp.login(MAIL_USER, MAIL_PASS)
            smtp.sendmail(SENDER, receivers, message.as_string())
            logger.error(f"send email notification successfully, the recipient is: {adds}. message: {msg}")
            return True
        except Exception as e:
            logger.error(f"Failed to send mail to: {adds}. error: {e}")
            return False
