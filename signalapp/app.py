from argparse import ArgumentParser
from dataclasses import dataclass
from random import randbytes
from typing import List

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


@dataclass
class SignatureAES:
    session_key: bytes
    nonce: bytes
    tag: bytes
    ciphertext: bytes


class Signal:
    def __init__(self, mode: int = AES.MODE_EAX, session_key_size: int = 16):
        self.mode = mode
        self.session_key_size = session_key_size

    @staticmethod
    def generate_key(key_size: int = 256) -> RSA:
        return RSA.generate(bits=key_size * 8)

    @staticmethod
    def import_key(filepath: str) -> RSA:
        return RSA.import_key(open(filepath).read())

    @staticmethod
    def get_private(key: RSA) -> str:
        """openssl genrsa -out private_key.pem 2048"""
        return key.export_key()

    @staticmethod
    def get_public(key: RSA) -> str:
        """openssl rsa -in private.pem -pubout -out public.pem"""
        return key.public_key().export_key()

    @staticmethod
    def __encrypt(any_key: RSA, message: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(any_key)
        return cipher.encrypt(message)

    @staticmethod
    def __decrypt(private_key: RSA, message: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(message)

    def __send(self, public_key: RSA, message: bytes) -> SignatureAES:
        # Generate an unique random session key
        session_key = get_random_bytes(self.session_key_size)

        # Encrypt the session key with the public RSA key
        enc_session_key = self.__encrypt(public_key, session_key)

        # Encrypt the data with the AES session key
        cipher = AES.new(session_key, self.mode)
        ciphertext, tag = cipher.encrypt_and_digest(message)

        return SignatureAES(enc_session_key, cipher.nonce, tag, ciphertext)

    def __receive(self, private_key: RSA, signature: SignatureAES) -> bytes:
        # Decrypt the session key with the private RSA key
        session_key = self.__decrypt(private_key, signature.session_key)

        # Decrypt the data with the AES session key, nonce avoids data tempering
        cipher = AES.new(session_key, self.mode, signature.nonce)
        return cipher.decrypt_and_verify(signature.ciphertext, signature.tag)

    def send(self, public_key: RSA, message: bytes, file_out: str) -> None:
        file_obj = open(file_out, "wb")
        [file_obj.write(x) for x in self.__send(public_key, message).__dict__.values()]
        file_obj.close()
        return

    def receive(self, private_key: RSA, file_in: str) -> bytes:
        file_obj = open(file_in, "rb")
        enc_session_key, nonce, tag, ciphertext = \
            [file_obj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

        return self.__receive(private_key, SignatureAES(
            ciphertext=ciphertext,
            tag=tag,
            nonce=nonce,
            session_key=enc_session_key
        ))

    def test_rsa(self, message: bytes = randbytes(n=214)):
        # Generate keys
        private_key = self.generate_key()
        public_key = private_key.public_key()

        # CipherText
        ciphertext = self.__encrypt(public_key, message)

        # Back to message
        return message == self.__decrypt(private_key, ciphertext)

    def test_signal(self, message: bytes = randbytes(n=500)):
        # Generate keys
        private_key = self.generate_key()
        public_key = private_key.public_key()

        # CipherText
        ciphertext = self.__send(public_key, message)

        # Back to message
        return message == self.__receive(private_key, ciphertext)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--key", "-k", type=str, required=True)
    parser.add_argument("--message", "-m", type=str, required=False)
    parser.add_argument("--file_in", "-i", type=str, required=False)
    parser.add_argument("--file_out", "-o", type=str, default="output.bin")
    args = parser.parse_args()

    signal_app = Signal()
    if not signal_app.test_rsa() or not signal_app.test_signal():
        raise Exception

    key = signal_app.import_key(args.key)

    if args.message:
        signal_app.send(key, args.message.encode("utf-8"), args.file_out)

    elif args.file_in:
        parsed = signal_app.receive(key, args.file_in)
        print(parsed.decode("utf-8"))
