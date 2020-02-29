class WidgetManager:

    def __init__(self):
        self.__buttons = []
        self.__checkers = []

    def button(self, cls, args, kwargs):
        button = cls(*args, **kwargs)
        self.__buttons.append(button)
        return button

    def checker(self, cls, args, kwargs):
        checker = cls(*args, **kwargs)
        self.__checkers.append(checker)
        return checker

    @property
    def widgets(self):
        return {'buttons': self.__buttons.copy(), 'checkers': self.__checkers.copy()}
