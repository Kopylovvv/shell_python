from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def execute(self, args, options):
        """абстрактный метод для выполнения команды"""
        pass

    @property
    @abstractmethod
    def name(self):
        """абстрактное свойство для имени команды"""
        pass
