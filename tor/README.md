# Tor Browser

Setup
----------
Install Tor through [brew](https://formulae.brew.sh/formula/tor)

    brew install tor

Hash a password for Tor (optional)

    tor --hash-password YourPassword

Setup tor config file (optional)

    cp /usr/local/etc/tor/torrc.sample /usr/local/etc/tor/torrc
    vi /usr/local/etc/tor/torrc (edit config file)

Install Python [Libraries](https://pypi.org/)

    pip install -r requirements.txt

Download GeoIP Database on [MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/)

Usage
----------
Launch Tor

    tor

Call webpage with cUrl through tor

    curl --socks4a localhost:9050 <url>

Call the Tor script

     python -m tor

Documentation
----------
[**Tor Project**](https://2019.www.torproject.org/)

[**Stem**](https://stem.torproject.org/)

[**Fake User-Agent**](https://pypi.org/project/fake-useragent/)
