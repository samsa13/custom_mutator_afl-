import random

import random


def init(seed):
    random.seed(seed)


def deinit():
    pass


def fuzz(buf, add_buf, max_size):
    mutators = [
        insert_box,
        type_change,
        scramble,
        scramble2,
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(buf)


def insert_box(buf):
    ret = bytearray(buf)
    rand = random.randint(0, len(buf) - 2)
    inserted_len = 0
    for i in range(rand, len(buf) - 2):
        i += inserted_len
        for k in range(0, random.randint(0, 5)):
            if buf[i] == ord('/') and buf[i + 1] == ord('>'):
                j = i + 2
                insert = bytearray('\n' + "<box top='" + str(random.randint(0, 5000)) + "' left='" + str(random.randint(0, 5000)) +
                                   "' width='" + str(random.randint(0, 5000)) + "' height='" + str(random.randint(0, 5000)) + "'/>", 'UTF-8')
                buf = buf[0:j] + insert + buf[j:]
                inserted_len += len(insert)
    ret = buf
    return ret


def type_change(buf):
    ret = bytearray(buf)
    if len(buf) > 20:
        length = len(buf) - 20
    else:
        length = len(buf) - 1
    rand = random.randint(0, length)
    inserted_len = 0
    for i in range(rand, length):
        i += inserted_len
        if buf[i] == ord('t') and buf[i + 1] == ord('y'):
            j = i + 6
            insert = bytearray('3GP/ZIP/', 'UTF-8')
            buf = buf[0:j] + insert + buf[j + 8:]
            inserted_len += len(insert)
    ret = buf
    return ret
    """def fuzz(buf, add_buf, max_size):
    buf_str = buf.decode('UTF-8', errors='ignore')
    res_buf = buf_str
    width_arr = re.findall(r'(?<=width=\')\d+', buf_str, flags=re.MULTILINE)
    height_arr = re.findall(r'(?<=height=\')\d+', buf_str, flags=re.MULTILINE)
    iterator = re.finditer(r'(?<=\\\>)\d*', buf_str, flags=re.MULTILINE)
    j = 1
    for i in iterator:
        pos = i.end()
        rand_top = random.randint(0, 500)
        rand_left = random.randint(0, 500)
        rand_top = rand_top if rand_top < height_arr[j] else height_arr[j]
        rand_top = rand_left if rand_left < width_arr[j] else width_arr[j]
        insert = "<box top='" + str(rand_top) + "' left='" + str(rand_left)+"' width='" + str(
            width_arr[j] - rand_left) + "' height='" + str(height_arr[j] - rand_top) + "'/>"
        res_buf = buf_str[0:pos + 1] + insert + buf_str[pos + 1:]
        j += 1
    return bytearray(res_buf, 'UTF-8')"""


def scramble(buf: bytearray) -> bytearray:
    pos = random.randint(0, len(buf) - 1)
    buf[pos] = (buf[pos] * 0xcc9e2d51) % 255
    (buf[pos] >> 17) | (buf[pos] << 15)
    buf[pos] = (buf[pos] * 0x1b873593) % 255
    return buf


def scramble2(buf: bytearray) -> bytearray:
    pos1 = random.randint(0, len(buf) - 1)
    buf[pos1] ^= scramble(buf)[pos1]
    buf[pos1] ^= buf[pos1] >> 13
    return buf


def delete_random_character(buf: bytearray) -> bytearray:
    if (buf == ""):
        return buf
    pos = random.randint(0, len(buf) - 1)
    return buf[:pos] + buf[pos + 1:]


def insert_random_character(buf: bytearray) -> bytearray:
    pos = random.randint(0, len(buf) - 1)
    random_character = chr(random.randrange(32, 127))
    return buf[:pos] + bytearray(ord(random_character)) + buf[pos:]


def flip_random_character(buf):
    if (buf == ""):
        return buf
    pos = random.randint(0, len(buf) - 1)
    c = buf[pos]
    bit = 1 << random.randint(0, 6)
    new_c = c ^ bit
    return buf[:pos] + buf[pos + 1:]