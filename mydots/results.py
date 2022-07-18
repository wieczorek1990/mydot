import abc

from mydots import abstract


class Result(abstract.Singleton, abc.ABC):
    pass


class Empty(Result):
    pass
