import typing


class Singleton:
    __instances: dict[str, typing.Any] = {}

    def __new__(cls, *args, **kwargs) -> "Singleton":
        cls_name = cls.__name__
        if cls_name not in cls.__instances:
            cls.__instances[cls_name] = super().__new__(cls, *args, **kwargs)
        return cls.__instances[cls_name]
