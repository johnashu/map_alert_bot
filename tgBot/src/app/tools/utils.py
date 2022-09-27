#
# By Maffaz 2021 - maffaz.one
#
import logging
from os.path import join
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s", level=logging.INFO
)
msg_path = join(os.getcwd(), "messages")


def open_file(fn):
    pth = join(msg_path, fn)
    with open(pth, "r", encoding="utf-8") as f:
        data = f.read()
        logging.debug(data)
        return data


def readable_price(num, show_decimals=True):
    temp = []
    c = 1

    main, decimals = str(num).split(".")

    for d in reversed(main):
        temp.insert(0, d)
        if c == 3:
            temp.insert(0, ",")
            c = 1
        else:
            c += 1

    if not show_decimals:
        decimals = ""

    rtn_str = "".join(temp)
    rtn_str += f".{decimals}" if show_decimals else ""
    if rtn_str[0] == ",":
        rtn_str = rtn_str[1:]

    print(rtn_str)
    return rtn_str


def get_places(x):
    l = x.split(".")[-1]
    c = 0
    for x in l:
        c += 1
    return c
