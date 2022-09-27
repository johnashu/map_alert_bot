from dotenv import dotenv_values, find_dotenv
import os


class Envs:
    def __init__(self, envFile: str = ".env", **kw):
        self.envFile = envFile
        self.load_envs()

    def load_envs(self):

        config = dotenv_values(find_dotenv(self.envFile))

        for k, v in config.items():
            print(k, v)
            # if not v:
            #     raise ValueError(f"No value for key {k} - Please update .env file!")
            try:
                setattr(self, k, int(v))
            except (SyntaxError, ValueError):
                setattr(
                    self,
                    k,
                    True
                    if v.lower() == "true"
                    else False
                    if v.lower() == "false"
                    else v,
                )
                os.environ[k] = v
                # print('set', k, v)
                # print(self.SECRET_KEY)