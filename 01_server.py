import web
import hmac
import time
import binascii
import hashlib


def insecure_compare(s1, s2):
    b1 = bytearray(binascii.unhexlify(s1))
    b2 = bytearray(binascii.unhexlify(s2))

    for i in range(len(min(b1, b2))):
        if b1[i] != b2[i]:
            return False

        time.sleep(0.05)

    return True


def calc_hmac(file_content, key):
    file_hmac = hmac.new(key.encode(), file_content.encode(), hashlib.sha256)
    return file_hmac.hexdigest()


def hmac_from_file(file_name, key):
    with open(file_name, 'r') as f:
        file_content = f.read()
    return calc_hmac(file_content, key)


KEY = 'YELLOW SUBMARINE'


class hello:
    def GET(self):
        params = web.input(_method='get')
        file_name = params['file'] if 'file' in params else None
        signature = params['signature'] if 'signature' in params else None

        if file_name and signature and len(signature) == 64:
            with open(file_name, 'r') as f:
                file_content = f.read()

            file_hmac = calc_hmac(file_content, KEY)

            if insecure_compare(file_hmac, signature):
                return file_content

        return 'Access denied...'


def main():
    file_hmac = hmac_from_file('foo', KEY)
    print(file_hmac)

    app = web.application(('/', 'hello'), globals())
    app.run()


if __name__ == '__main__':
    main()
