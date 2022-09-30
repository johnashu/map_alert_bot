class Templates:
    @staticmethod
    def error_reply(header: str, msg: str) -> str:
        return f"<b>🚨 {header} 🚨</1b>\n\n➡️▶️💰🎓{msg}"

    GenericError = error_reply(
        "An Unkown Error Has Occurred. ",
        ' Please Contact <a href="tg://user?id=486589942">@Maffaz</a>',
    )


# print(Templates.GenericError)
