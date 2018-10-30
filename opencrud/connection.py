from .utils import get_connection_class


class WithOpenCrudConnection(object):
    """ Wrapper for DjangoObjectTypeOptions object. Adds model and connection_class """
    def __init__(self, model):
        self._model = model

    def __call__(self, cls):
        cls.model = self._model
        cls.connection_class = get_connection_class(self._model)
        return cls
