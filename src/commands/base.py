from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def execute(self, args, options):
        """Абстрактный метод для выполнения команды"""
        pass

    @property
    @abstractmethod
    def name(self):
        """Абстрактное свойство для имени команды"""
        pass
