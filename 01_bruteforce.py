import binascii
import time
import urllib.request


BASE_URL = 'http://localhost:8080'


def try_next(file_name, already_known, delay):
    length = 32 - len(already_known)
    expected = delay * len(already_known) + 0.01

    for byte in range(256):
        suffix = bytes([byte]) + (b'\x00' * (length - 1))
        signature = already_known + suffix
        candidate = binascii.hexlify(signature).decode('ascii')
        url = f'{BASE_URL}/?file={file_name}&signature={candidate}'
        start = time.perf_counter()
        response = urllib.request.urlopen(url)
        end = time.perf_counter()

        if response.status != 200:
            raise Exception(f'Error: {str(response.status)}')

        if end - start > expected + 0.8 * delay:
            return already_known + bytes([byte])

    raise Exception('Error')


if __name__ == '__main__':
    known_bytes = b''

    for i in range(33):
        known_bytes = try_next('foo', known_bytes, 0.05)
        print(binascii.hexlify(known_bytes))
