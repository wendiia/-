from functools import wraps


class Singleton:
    """Класс Singleton создает паттерн singleton, не позволяя создавать более 1 экземпляра
    """
    def __init__(self):
        self.instances = {}

    def __call__(self, ui_class):
        """Реализует паттерн singleton
        Parameters
        ----------
        ui_class: sip.wrappertype
            класс события мыши
        """
        @wraps(ui_class)
        def getinstance(*args, **kwargs):
            if ui_class not in self.instances:
                self.instances[ui_class] = ui_class(*args, **kwargs)
            return self.instances[ui_class]

        return getinstance
