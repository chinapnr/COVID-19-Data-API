import smtplib
from email.header import Header
from email.mime.text import MIMEText
from fishbase.fish_logger import logger
from app.utils.singleTon import Singleton
from app.config.config import MAIL_HOST, MAIL_PASS, MAIL_USER, SUBJECT, SENDER, MAIL_PORT


@Singleton
class EmailUtils:
    def send_mail(self, msg, adds):
        """
        发送邮件
        :param msg:
        :param adds:
        :return:
        """
        receivers = adds
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(SENDER, 'utf-8')
        message['To'] = Header("", 'utf-8')
        subject = SUBJECT
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtp = smtplib.SMTP_SSL()
            smtp.connect(MAIL_HOST, MAIL_PORT)
            smtp.login(MAIL_USER, MAIL_PASS)
            smtp.sendmail(SENDER, receivers, message.as_string())
            logger.error(f"send email notification successfully, the recipient is: {adds}. message: {msg}")
            return True
        except Exception as e:
            logger.error(f"Failed to send mail to: {adds}. error: {e}")
            return False
