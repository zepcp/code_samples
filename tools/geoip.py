import geoip2.database
import geoip2.errors


class GeoIP:
    """Countries and IP location Interface"""
    def __init__(self, filepath="GeoLite2-City.mmdb"):
        self.READER = geoip2.database.Reader(filepath)

    def ip_info(self, ip_address):
        return self.READER.city(ip_address)

    def country_code(self, ip_address):
        return self.ip_info(ip_address).country.iso_code

    def country(self, ip_address, language="en"):
        return self.ip_info(ip_address).country.names[language]

    def city(self, ip_address, language="en"):
        return self.ip_info(ip_address).city.names[language]

    def continent(self, ip_address, language="en"):
        return self.ip_info(ip_address).continent.names[language]

    def timezone(self, ip_address):
        return self.ip_info(ip_address).location.time_zone

    def coordinates(self, ip_address):
        return (self.ip_info(ip_address).location.latitude,
                self.ip_info(ip_address).location.longitude)

