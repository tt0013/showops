from django.apps import AppConfig


class PublicConfig(AppConfig):
    name = 'public'
    #邮件
    Mail = {
        "host": "mail.sinashow.com",
        "user": "monitor@sinashow.com",
        "pswd": "monitor",
        "postfix": "sinashow.com",
        "adminurl": "http://127.0.0.1:8000/itom"
    }
