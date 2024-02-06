from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtWidgets import QWidget

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

import datetime
import calendar

from database_manager import DBManager


def sort_data(dates) -> tuple:
    today: datetime = datetime.datetime.today()
    current_month: int = today.month
    month_colors: list[str] = list(map(lambda x: 'green' if x <= current_month else 'red', range(1, 13)))
    number_of_validations: list[int] = [0] * 12

    for date_data in dates:
        date: datetime = datetime.datetime.strptime(date_data[0], '%Y-%m-%d')
        if date.month != current_month or today.year == date.year:
            number_of_validations[date.month - 1] += 1

    months: Sequence[str] = calendar.month_name[1:]
    swap_months = lambda x: x[current_month:] + x[:current_month]

    return swap_months(months), swap_months(number_of_validations), swap_months(month_colors)


class Histogram(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        loadUi('ui/histogram.ui', self)

        self.save_button.clicked.connect(self.save_histogram)
        self.close_button.clicked.connect(self.close_histogram)
        self.setStyleSheet(open('ui/histogram.css').read())

        self.database: DBManager = DBManager()

    def get_data(self) -> list[tuple[any]]:
        query: str = "SELECT date FROM validations WHERE date >= date('now', '-1 year') AND date <= date('now')"
        return self.database.execute_query(query)

    def close_histogram(self) -> None:
        self.clear_layout()
        self.close()

    def clear_layout(self) -> None:
        while self.histogram.count() > 0:
            self.histogram.itemAt(0).widget().setParent(None)

    def plot_histogram(self) -> None:
        self.hide()
        self.clear_layout()

        dates: list[tuple[any]] = self.get_data()

        months, values, colors = sort_data(dates)
        fig, ax = plt.subplots()

        ax.set_ylim(0, max(values) + 1)
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(months, rotation=45, ha='right')
        ax.set_xlabel('Mesiac')
        ax.set_ylabel('Počet')
        ax.set_title('História validácii')
        ax.bar(months, values)

        for i, label in enumerate(ax.get_xticklabels()):
            label.set_color(colors[i])

        canvas: FigureCanvasQTAgg = FigureCanvasQTAgg(fig)
        self.histogram.addWidget(canvas)
        self.show()

    def save_histogram(self) -> None:
        # path = QFileDialog.getExistingDirectory(self, 'Select location', '../../resources/pdf')
        save_path, _ = QFileDialog.getSaveFileName(None, 'Save Figure', '', 'PNG files (*.png);;All Files (*)')
        if save_path:
            plt.savefig(save_path)

        self.close_histogram()
