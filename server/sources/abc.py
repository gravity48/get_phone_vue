from typing import Dict


class Specification:

    def is_satisfy(self, item) -> bool:
        raise NotImplementedError


class DataSources:
    """
    Предназначен для фильтрации входных данных и при необходимости сохранения из
    различных источников для их последующей обработки процессами
    """

    def get_source(self, specification: Specification) -> iter:
        raise NotImplementedError()


__all__ = ['DataSources', 'Specification']
