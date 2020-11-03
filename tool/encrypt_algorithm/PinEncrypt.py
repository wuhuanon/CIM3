import hashlib
import random
import string


def pinEncrypt(pin):
    mm = hashlib.md5()
    mm.update(pin.encode('utf-8'))
    md5_pin = mm.hexdigest()
    return md5_pin

def ramdomPin(count):
    src_digits = string.digits  # string_数字
    src_uppercase = string.ascii_uppercase  # string_大写字母
    src_lowercase = string.ascii_lowercase  # string_小写字母
    src_symbols = " ~!@#$%^&*()_+" #特殊字符
    for i in range(count):
        digits_num = random.randint(1, count//4)
        uppercase_num = random.randint(1, count//4)
        symbols_num = random.randint(1, count//4)
        lowercase_num = count - (digits_num + uppercase_num + symbols_num)

        # 生成字符串
        password = random.sample(src_digits, digits_num) + random.sample(src_uppercase,
                                                                         uppercase_num) + random.sample(
            src_lowercase, lowercase_num) + random.sample(src_symbols, symbols_num)

        # 打乱字符串
        random.shuffle(password)

        new_password = ''.join(password)

        return new_password

if __name__ == "__main__":
    print(pinEncrypt("B6+amDojzhyq"))