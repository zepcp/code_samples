import os
import uuid
import subprocess


class OpenSSL:
    def __init__(self, encryption="-aes-256-cbc", encoding="-base64", salt="-salt"):
        self.encryption = encryption
        self.encoding = encoding
        self.salt = salt

    @staticmethod
    def _check_file(file):
        if not os.path.isfile(file):
            if os.path.exists(file):
                raise TypeError("Input is not a file")
            raise ValueError("Input file not found")

    def _manage_file(self, action, file, output, password):
        self._check_file(file)
        subprocess.call(["openssl", "enc", action,
                         self.encryption, self.encoding, self.salt,
                         "-in", file,
                         "-out", output,
                         "-pass", "pass:"+password])

    def encrypt_file(self, file, output, password):
        self._manage_file("-e", file, output, password)

    def decrypt_file(self, file, output, password):
        self._manage_file("-d", file, output, password)

    def _manage_string(self, action, text, filename, password):
        file = open(filename, "w")
        file.write(text)
        file.close()
        self._manage_file(action, filename, filename+".new", password)
        result = subprocess.check_output(["cat", filename+".new"])
        os.remove(filename)
        os.remove(filename+".new")
        return result.decode('utf8')

    def encrypt(self, text, password):
        return self._manage_string("-e", text, uuid.uuid4().hex, password)

    def decrypt(self, text, password):
        return self._manage_string("-d", text, uuid.uuid4().hex, password)
