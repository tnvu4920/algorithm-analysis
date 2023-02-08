from algorithm import Algorithm
from design import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import matplotlib
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
from prettytable import PrettyTable
from random_string import RandomString


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Расстояние Левенштейна')

        self.algorithms = {
            'lev_mat': Algorithm('levenshtein_matrix'),
            'lev_rec': Algorithm('levenshtein_recursively'),
            'lev_rec_cache': Algorithm('levenshtein_recursively_cache'),
            'dam_lev': Algorithm('damerau_levenshtein')
        }
        self.cur_algorithm = 'lev_mat'

        self.lev_mat.setChecked(True)
        self.lev_mat.clicked.connect(lambda: self.change_algorithm('lev_mat'))
        self.lev_rec.clicked.connect(lambda: self.change_algorithm('lev_rec'))
        self.lev_rec_cache.clicked.connect(lambda: self.change_algorithm('lev_rec_cache'))
        self.dam_lev.clicked.connect(lambda: self.change_algorithm('dam_lev'))

        self.edit_str_1.textChanged.connect(self.init_result_string)
        self.edit_str_2.textChanged.connect(self.init_result_string)

        self.search.clicked.connect(self.get_distance)

        matplotlib.use('Qt5Agg')
        self.graph = None
        self.graph_lev_cache.clicked.connect(self.graphics_lev_cache)
        self.graph_lev_dam.clicked.connect(self.graphics_lev_dam)
        self.graph_rec_cache.clicked.connect(self.graphics_rec_cache)

        self.get_peak_memory.clicked.connect(self.peak_memory)

    def change_algorithm(self, new_algorithm):
        self.cur_algorithm = new_algorithm

    def init_result_string(self):
        self.result_string.setText('Редакционное расстояние = ?')

    def get_distance(self):
        distance = self.algorithms[self.cur_algorithm].execute(
            self.edit_str_1.text(), self.edit_str_2.text()
        )
        self.result_string.setText(f'Редакционное расстояние = {distance}')

    def init_graphics_labels(self, n):
        self.graph = plt.figure(n)
        plt.title('График зависимости времени от размера строк')
        plt.xlabel('Процессорное время выполнения алгоритма, сек')
        plt.ylabel('Размер строк')

    def graphics_lev_cache(self):
        x_lev_mat = []
        x_lev_rec_cache = []
        y = []

        for n in range(10, 101, 10):
            str_1, str_2 = RandomString(n), RandomString(n)
            x_lev_mat.append(self.algorithms['lev_mat'].get_time(str_1, str_2))
            x_lev_rec_cache.append(self.algorithms['lev_rec_cache'].get_time(str_1, str_2))
            y.append(n)

        if self.graph:
            self.graph.clear()
        plt.close(1)
        plt.close(2)
        plt.close(3)
        self.init_graphics_labels(1)
        plt.plot(x_lev_mat, y, marker='o', color='red', label='Левенштейн - матрично')
        plt.plot(x_lev_rec_cache, y, marker='o', color='green', label='Левенштейн - рекурсвино с кэшем')
        plt.legend()
        plt.show()

    def graphics_lev_dam(self):
        x_lev_rec = []
        x_dam_lev = []
        y = []

        for n in range(2, 11):
            str_1, str_2 = RandomString(n), RandomString(n)
            x_lev_rec.append(self.algorithms['lev_rec'].get_time(str_1, str_2))
            x_dam_lev.append(self.algorithms['dam_lev'].get_time(str_1, str_2))
            y.append(n)

        if self.graph:
            self.graph.clear()
        plt.close(1)
        plt.close(2)
        plt.close(3)
        self.init_graphics_labels(2)
        plt.plot(x_lev_rec, y, marker='o', color='blue', label='Левенштейн - рекурсивно')
        plt.plot(x_dam_lev, y, marker='o', color='black', label='Дамерау-Левенштейн - рекурсвино')
        plt.legend()
        plt.show()

    def graphics_rec_cache(self):
        x_lev_rec = []
        x_lev_rec_cache = []
        y = []

        for n in range(2, 11):
            str_1, str_2 = RandomString(n), RandomString(n)
            x_lev_rec.append(self.algorithms['lev_rec'].get_time(str_1, str_2))
            x_lev_rec_cache.append(self.algorithms['lev_rec_cache'].get_time(str_1, str_2))
            y.append(n)

        if self.graph:
            self.graph.clear()
        plt.close(1)
        plt.close(2)
        plt.close(3)
        self.init_graphics_labels(3)
        plt.plot(x_lev_rec, y, marker='o', color='brown', label='Левенштейн - рекурсивно')
        plt.plot(x_lev_rec_cache, y, marker='o', color='darkblue', label='Левенштейн - рекурсвино с кэшем')
        plt.legend()
        plt.show()

    def peak_memory(self):
        print(help(memory_usage))

    def peak_memory1(self):
        max_len = 10
        mat, rec, rec_cache, dam = [], [], [], []
        nums = [i for i in range(1, max_len)]

        for n in range(1, max_len):
            str_1, str_2 = RandomString(n), RandomString(n)
            mat.append(self.algorithms['lev_mat'].get_memory(str_1, str_2))
            rec.append(self.algorithms['lev_rec'].get_memory(str_1, str_2))
            rec_cache.append(self.algorithms['lev_rec_cache'].get_memory(str_1, str_2))
            dam.append(self.algorithms['dam_lev'].get_memory(str_1, str_2))

        print('Пиковые значения памяти')
        names = ['Размер строк', 'Левенштейн - матрично', 'Левенштейн - рекурсивно',
                 'Левенштейн - рекурсивно с кэшем', 'Дамерау-Левенштейн - рекурсивно']
        result = PrettyTable(names)

        for row in zip(nums, mat, rec, rec_cache, dam):
            result.add_row(row)

        print(result)
