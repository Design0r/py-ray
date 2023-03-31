import abc


class Object:
    @abc.abstractmethod
    def intersect(self, ray):
        raise NotImplementedError
