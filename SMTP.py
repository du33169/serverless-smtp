# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass
from email.utils import formataddr
from email.header import Header

@dataclass
class SMTP:
    server: str
    account: str
    password: str
    secure: bool = True
    port: int = 465

    def send_mail(self,SenderName:str, to_addrs:list[str], subject:str, content:str)->tuple[bool,str]:
        # check input
        if not isinstance(SenderName, str):
            msg=f'SenderName should be a string, but got {type(SenderName)}'
            print(msg)
            return False, msg
        if not isinstance(subject, str):
            msg=f'subject should be a string, but got {type(subject)}'
            print(msg)
            return False, msg
        if not isinstance(content, str):
            msg=f'content should be a string, but got {type(content)}'
            print(msg)
            return False, msg
        if not isinstance(to_addrs, list) or not all(isinstance(addr, str) for addr in to_addrs):
            msg='to_addrs should be a list of string'
            print(msg)
            return False, msg

        # build message
        msg = MIMEText(content, _subtype='plain', _charset='UTF-8')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        msg['From'] = formataddr((Header(SenderName, 'utf-8').encode(),self.account))  
        msg['To'] = Header(','.join(to_addrs), 'utf-8').encode()

        # connect smtp
        try:
            print(f'connecting to server {self.server} port {self.port}')
            if self.secure:
                print('SSL enabled')
                client = smtplib.SMTP_SSL(self.server, self.port)  
            else:
                print('SSL disabled')
                client = smtplib.SMTP(self.server, self.port)
        except Exception as e:
            msg=f'connection failed:{e}'
            print(msg)
            return False, msg
        try:
            print(f'logining as {self.account}')
            client.login(self.account, self.password)
        except Exception as e:
            msg=f'login failed:{e}'
            print(msg)
            return False, msg

        # send email
        try:
            print(f'sending email subject <{subject}> to {to_addrs}')
            client.sendmail(self.account, to_addrs, msg.as_string())
        except Exception as e:
            msg=f'sending email failed:{e}'
            print(msg)
            return False, msg
        client.quit()
        return True,'successfully sent email'
