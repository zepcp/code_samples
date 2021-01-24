# Generic Tools

Setup
----------
Install Python [Libraries](https://pypi.org/)

    pip install -r requirements.txt

Usage
----------
SMTP Mail tool

    from mail import Mail

    mail = Mail(<host>, <email>, <password>)
    mail.send_mail(<subject>, <message>, <to_address>)

Openssl encryption tool

    from openssl import OpenSSL

    openssl = OpenSSL()
    openssl.encrypt(<text>, <password>)
    openssl.decrypt(<encrypted_text>, <password>)
    openssl.encrypt_file(<input>, <output>, <password>)
    openssl.decrypt_file(<input>, <output>, <password>)

GeoIp tool

    from geoip import GeoIP

    geoip = GeoIP()
    geoip.ip_info(<ip_address>)
    geoip.country_code(<ip_address>)
    geoip.country(<ip_address>)
    geoip.city(<ip_address>)
    geoip.continent(<ip_address>)
    geoip.timezone(<ip_address>)
    geoip.coordinates(<ip_address>)

Captcha tool

    from captcha import Captcha

    captcha = Captcha()
    captcha.create(<user>)
    captcha.validate_answer(<user>)
    captcha.validate_answer(<user>, <answer>)
    captcha.validate_timediff(<user>)
    captcha.delete(<user>)
