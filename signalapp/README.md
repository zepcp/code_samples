# Signal App
P2P messaging secured by RSA public-private key pairs.

RSA encryption has limited message size (e.g. a key with 256 bytes can encrypt message up to 214 bytes).

Thus, a random session key is used to encrypt an unlimited message content. Then, that session key is encrypted using RSA.

Setup
----------
Install Python Library [Libraries](https://pypi.org/)

    pip install -r requirements.txt

Generate a public-private key pair

    openssl genrsa -out private.pem 2048
    openssl rsa -in private.pem -pubout -out public.pem

Usage
----------
Share your **public key**, with it one may send you messages

    python -m app --key public.pem --message 'test msg' --file_out output.bin
    openssl rsautl -encrypt -in <filename> -out output.bin -inkey public.pem -pubin

Which can only be decrypted with your **private key**

    python -m app --key private.pem --file_in output.bin
    openssl rsautl -decrypt -in output.bin -inkey private.pem

Documentation
----------
[**PyCryptoDome PyPi**](https://pypi.org/project/pycryptodome/)

[**PyCryptoDome Docs**](https://www.pycryptodome.org/en/latest/)

[**PyCryptoDome Source**](https://github.com/Legrandin/pycryptodome/)
