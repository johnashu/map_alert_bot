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


def flatten(d: dict) -> None:
    """Flatten a nested dictionary.
    Args:
        d (dict): nested dictionary to flatten
    Returns:
        dict: flattened dictionary.
    """
    out = {}
    if d:
        if isinstance(d, str):
            import ast

            try:
                d = ast.literal_eval(d)
            except (ValueError, SyntaxError):
                pass
        try:
            for key, val in d.items():
                print(key)
                if key == "chat":
                    out["chat_id"] = val["id"]
                if key == "from":
                    out["user_id"] = val["id"]
                if isinstance(val, dict):
                    val = [val]
                if isinstance(val, list):
                    for subdict in val:
                        deeper = flatten(subdict).items()
                        out.update(
                            {
                                key2: val2
                                for key2, val2 in deeper
                                if key2 not in out.keys()
                            }
                        )
                else:
                    out[key] = val

        except AttributeError as e:
            pass
    return out


def parse_data(context: dict) -> None:
    cols_required = [
        "update_id",
        "chat_id",
        "user_id",
        "first_name",
        "username",
        "text",
        "message_id",
        "date",
        "language_code",
        "is_bot",
        "pub_key",
        "is_validator",
    ]
    parsed = {}
    for key, val in context.items():
        if key in cols_required:
            print(key)
            parsed[key] = val
    return parsed


def build_dict(msg, update_id, value) -> dict:
    from datetime import datetime as dt

    return {
        "value": value,
        "update_id": update_id,
        "chat_id": msg.chat.id,
        "user_id": msg["from"].id,
        "first_name": msg.chat.first_name,
        "username": msg.chat.username,
        "text": msg.text,
        "message_id": msg.message_id,
        "language_code": msg["from"].language_code,
        "is_bot": msg["from"].is_bot,
    }


# d = flatten(tg_data)
# print(d)
# parse_data(d)
