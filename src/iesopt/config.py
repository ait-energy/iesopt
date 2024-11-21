from dotenv import dotenv_values


def _strtobool(val: str):
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    if val in ("n", "no", "f", "false", "off", "0"):
        return 0
    raise ValueError("Invalid truth value %r" % (val,))


class Config:
    DEFAULTS = {
        "IESOPT_JULIA": "1.11.1",
        "IESOPT_CORE": "2.0.1",
        "IESOPT_JUMP": "1.23.5",
        "IESOPT_SOLVER_HIGHS": "1.12.1",
        "IESOPT_MULTITHREADED": "no",  # yes, no
        "IESOPT_OPTIMIZATION": "latency",  # rapid, latency, normal, performance
    }
    _config = None

    @classmethod
    def init(cls):
        if cls._config is not None:
            return

        cls._config = {
            k[7:].lower(): v
            for (k, v) in {
                **cls.DEFAULTS,
                **dotenv_values(),
            }.items()
            if k.startswith("IESOPT_")
        }

    @classmethod
    def get(cls, key: str):
        value = cls._config[key]
        if key in ["multithreaded"]:
            return _strtobool(value)
        return value

    @classmethod
    def find(cls, prefix: str):
        for k in cls._config.keys():
            if k.startswith(prefix):
                yield k


Config.init()
