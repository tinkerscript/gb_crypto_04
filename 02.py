import sha1


def sha1_with_key(key, message):
    return sha1.sha1(key + message)


def main():
    mac = sha1_with_key(b'geek', b'brains')
    print(mac)


if __name__ == '__main__':
    main()
