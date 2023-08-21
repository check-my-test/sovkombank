import sys
from decimal import Decimal
import timeit
import tracemalloc
import unittest

"""
Задача 1 Долевое строительство
1. Сложность: O(n), пиковое использование памяти: 9.745 KB.
2. Ограничение на размер входных данных для выполнения кода менее 5 секунд:
Реальная скорость будет зависеть от мощности устройства. Исходя из теоретической скорости выполнения кода 
(5 * 10^7 операций за 5 сек) ограничение будет 12_500_000 элементов (выполняется 4 операции для каждого элемента).
3. Сложность - 1. Затраченное время 1 час (Дольше считал память и макс. размер данных).
"""

def task1(decimals=None):
    if decimals is not None:  # Для оценки времени
        shares = [Decimal(k) for k in decimals]
    else:
        count = int(input())
        shares = [Decimal(input()) for _ in range(count)]
    sum_shares = sum(shares)
    normalized_list = [(share / sum_shares).quantize(Decimal("1.000")) for share in shares]
    for norm_share in normalized_list:
        if decimals is None:
            print(norm_share)

    # current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print(f"Текущее использование памяти: {current_memory / 10 ** 3} KB")
    # print(f"Пиковое использование памяти: {peak_memory / 10 ** 3} KB")


tracemalloc.start()
task1()
tracemalloc.stop()


"""
Задача 2 Мегатрейдер
1. Сложность: O(n * m), где n - общее количество облигаций, m - количество разных стоймостей лотов 
(кол-во шт * цену, меньшую S), пиковое использование памяти: 9.595 KB
2. Ограничение на размер входных данных для выполнения кода менее 5 секунд:
Реальная скорость будет зависеть от мощности устройства. Исходя из теоретической скорости выполнения кода 
(5 * 10^7 операций за 5 сек) ограничение будет около 1960 элементов-облигаций 
(путем решения уравнения 13n^2 + 17n - 50_000_000 = 0, которое получилось при 
приблизительном подсчете количества элементарных операций в алгоритме).
3. Сложность - 6. Затраченное время 7 часов.
"""


def task2_logic(s, sum_prices, dataset, test=False):
    def find_best_lot_index(j, price_lot, crit_prices):
        rest_money = crit_prices[j] - price_lot
        best_index = j - 1
        # Находим индекс столбца, в котором лежит самая выгодная покупка за оставшиеся деньги
        while best_index >= 0:
            if rest_money >= crit_prices[best_index]:
                break
            best_index -= 1
        return best_index

    def merge_lots(lot1, lot2):
        return [x + y for x, y in zip(lot1, lot2)]

    # Реализуем алгоритм динамического программирования: столбцы - отсортированная стоимость лотов и доступные средства
    null_elem = [0, 0, ""]
    crit_prices = [price for price in sorted(sum_prices) if price <= s]  # Убираем лоты, которые не сможем купить
    # Добавим в заготовку по 1 лишней строке и столбцу
    template = [[null_elem] * (len(crit_prices) + 1) for _ in range(len(dataset) + 1)]
    for i in range(len(dataset)):
        price_lot = dataset[i][0]
        for j in range(len(crit_prices)):
            # Если можем купить лот в заявленную цену, обрабатываем таблицу
            if price_lot <= crit_prices[j]:
                # Если в предыдущей строке нет данных, вставляем текущую покупку
                if template[i][j + 1] == null_elem:
                    template[i + 1][j + 1] = dataset[i]
                else:
                    # Находим индекс самого выгодного лота за оставшиеся деньги, если совершим покупку текущего лота
                    k = find_best_lot_index(j, price_lot, crit_prices)
                    # Выбираем и заносим максимум между покупкой текущего лота с докупкой наиболее выгодного лота
                    # за оставшиеся деньги и предыдущей самой выгодной покупкой
                    template[i + 1][j + 1] = max(
                        merge_lots(template[i][j + 1], null_elem),
                        merge_lots(template[i][k + 1], dataset[i]),
                        key=lambda x: x[1]
                    )
            else:
                template[i + 1][j + 1] = template[i][j + 1]
    # Конечный результат находится в последнем элементе двумерного списка
    result = template[-1][-1]
    print(result[1])
    if result[2] == "":
        result[2] = "\n"
    print(result[2])
    if test:
        return result[1], result[2]


def get_price_value(n, s, input_data):
    dataset = []
    sum_prices = {s}
    for elem in input_data:
        day, name, price, count = elem.split()
        price_lot = Decimal(price) * 10 * int(count)
        value = (n + 30 - int(day) - (Decimal(price) - 100) * 10) * int(count)
        dataset.append([price_lot, value, elem + "\n"])
        sum_prices.add(price_lot)
    return sum_prices, dataset


def task2():
    first_row_split = input().split()
    s = Decimal(first_row_split[2])
    n, m = (int(i) for i in first_row_split[:2])
    elem = input()
    if not elem:
        print(0)
        print()
        return
    input_data = []
    while elem:
        input_data.append(elem)
        elem = input()
    sum_prices, dataset = get_price_value(n, s, input_data)
    task2_logic(s, sum_prices, dataset)

    # current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print(f"Текущее использование памяти: {current_memory / 10 ** 3} KB")
    # print(f"Пиковое использование памяти: {peak_memory / 10 ** 3} KB")


tracemalloc.start()
task2()
tracemalloc.stop()



class TestTask2(unittest.TestCase):

    def test_standart_input(self):
        n, m, s = 2, 2, 8000
        input_data = ["1 alfa-05 100.2 2", "2 alfa-05 101.5 5", "2 gazprom-17 100.0 2"]
        sum_prices, dataset = get_price_value(n, s, input_data)
        profit, bonds = task2_logic(s, sum_prices, dataset, test=True)
        self.assertEqual(profit, 135)
        self.assertEqual(bonds, "2 alfa-05 101.5 5\n2 gazprom-17 100.0 2\n")

    def test_cant_buy_anything(self):
        n, m, s = 2, 2, 500
        input_data = ["1 alfa-05 100.2 2", "2 alfa-05 101.5 5", "2 gazprom-17 100.0 2"]
        sum_prices, dataset = get_price_value(n, s, input_data)
        profit, bonds = task2_logic(s, sum_prices, dataset, test=True)
        self.assertEqual(profit, 0)
        self.assertEqual(bonds, "\n")

    def test_cant_buy_one_bond(self):
        n, m, s = 2, 2, 5000
        input_data = ["1 alfa-05 100.2 2", "2 alfa-05 101.5 5", "2 gazprom-17 100.0 2"]
        sum_prices, dataset = get_price_value(n, s, input_data)
        profit, bonds = task2_logic(s, sum_prices, dataset, test=True)
        self.assertEqual(profit, 118)
        self.assertEqual(bonds, "1 alfa-05 100.2 2\n2 gazprom-17 100.0 2\n")

    def test_no_input(self):
        pass  # task2 do print() and return None


# if __name__ == '__main__':
#     unittest.main()