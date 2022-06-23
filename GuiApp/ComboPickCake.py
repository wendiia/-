from PyQt5.QtWidgets import QComboBox


class ComboPickCake(QComboBox):
    """Класс ComboPickCake переобределяет родительский класс QComboBox , для назначения своих стилей
    parent: OrderSystem.OrderSystem
        класс OrderSystem
    id_cakes: dict
        словарь, в котором ключ: название торта, значение: id торта
    """
    def __init__(self, parent, id_cakes):
        super().__init__(parent)
        self.addItems(list(id_cakes.keys()))
        self.setStyleSheet("""QComboBox {
                            font: 15pt "Microsoft YaHei UI Light";
                            font-weight: bold;
                            background-color: rgb(255, 244, 246);
                            border: none;
                            }""")
