import time
import getpass
import requests

from fake_useragent import UserAgent
from stem import Signal
from stem.util import term
from stem.control import Controller
from stem.process import launch_tor_with_config, launch_tor
from stem.connection import IncorrectPassword, MissingPassword 

import geoip2.database
import geoip2.errors

SOCKS_PORT = 9050
CONTROL_PORT = 9051

HASH_PWD = "16:0CA9528CFE8FF72160F586AD12E486CF9419D357C2D513A33BF68020DB"

PROXIES = {"http": "socks5://127.0.0.1:" + str(SOCKS_PORT),
           "https": "socks5://127.0.0.1:" + str(SOCKS_PORT)}

URL_TEST_CONNECTION = "https://check.torproject.org/"
URL_GET_IP = "https://api.ipify.org"

GEOIP_FILEPATH = "GeoLite2-City.mmdb"

READER = geoip2.database.Reader(GEOIP_FILEPATH)


def ipcountry(ip_address, ip_database=READER):
    """Returns the country for the respective ip address"""
    try:
        aux = ip_database.city(ip_address).country.iso_code
        if not aux:
            aux = u''
    except ValueError:
        aux = u'BAD_IP'
    except geoip2.errors.AddressNotFoundError:
        aux = u''

    return aux


def print_colored_lines(line, color=term.Color.BLUE):
    """Print init lines when launching Tor"""
    print(term.format(line, color))


def start_tor(password):
    """Launch Tor process"""
    # tor_process = launch_tor(torrc_path="/usr/local/etc/tor/torrc")
    try:
        tor_process = launch_tor_with_config(
            config = {
                "ExitNodes": "{ru},{us}",
                "StrictNodes": "1",
                "ExcludeExitNodes": "{pt}",
                "SocksPort": str(SOCKS_PORT),
                "ControlPort": str(CONTROL_PORT),
                "HashedControlPassword": HASH_PWD,
            },
            init_msg_handler = print_colored_lines,
        )
    except OSError as e:
        print_colored_lines(str(e), color=term.Color.RED)
        exit()
    controller = Controller.from_port(address="127.0.0.1", port=CONTROL_PORT)
    try:
        controller.authenticate(password = password)
    except (IncorrectPassword, MissingPassword) as e:
        stop_tor(tor_process, controller)
        # raise Exception("Couldnt Authenticate: {}".format(e))
        print_colored_lines(str(e), color=term.Color.RED)
        exit()

    return tor_process, controller, UserAgent().random


def new_identity(controller):
    """Update IP Address"""
    controller.signal(Signal.NEWNYM)
    if controller.is_newnym_available() == False:
        time.sleep(controller.get_newnym_wait())
    return UserAgent().random


def stop_tor(tor_process, controller):
    """Stop Tor process"""
    controller.close()
    tor_process.kill()
    return True


def test_connection():
    res = requests.get(URL_TEST_CONNECTION, proxies=PROXIES).text
    if "Congratulations" not in res:
        print_colored_lines("Tor connection failed", color=term.Color.RED)
        return False

    try:
        start = res.find("<strong>")
        end = res.find("</strong>")
        ip_address = res[start+len("<strong>"):end]
        for integer in ip_address.split("."): int(integer)
    except ValueError:
        print_colored_lines("Couldnt determine IP", color=term.Color.RED)
        return False
    return ip_address


if __name__ == "__main__":
    password = getpass.getpass("Insert TOR Password:")
    tor_process, controller, user_agent = start_tor(password)

    ip = test_connection()
    country = ipcountry(ip)
    print_colored_lines("Tor connection successful: {} - {}".format(country, ip),
        color=term.Color.GREEN)

    user_agent = new_identity(controller)

    headers = {"User-Agent": user_agent}
    ip2 = requests.get(URL_GET_IP, proxies=PROXIES, headers=headers).text
    country = ipcountry(ip2)

    if ip == ip2:
        print_colored_lines("Couldnt renew identity", color=term.Color.RED)
    else:
        print_colored_lines("Identity renewal successful: {} - {}".format(country, ip2),
                            color=term.Color.GREEN)

    stop_tor(tor_process, controller)
