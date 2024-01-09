import tkinter as tk # Імпорт Tkinter для створення графічного інтерфейсу користувача (GUI)
from tkinter import messagebox # Імпорт messagebox з Tkinter для відображення діалогових вікон
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Імпорт FigureCanvasTkAgg для інтеграції matplotlib з Tkinter GUI
from matplotlib.figure import Figure # Імпорт класу Figure з matplotlib для створення фігур
import networkx as nx # Імпорт бібліотеки NetworkX для роботи з графами та мережами
import random # Імпорт модулю random для генерації випадкових чисел
import matplotlib.pyplot as plt  # Імпорт pyplot з matplotlib для створення статичних, анімованих графіків та інтерактивних візуалізацій

""" Вузол AVL дерева. """
class AVLNode:
    def __init__(self, key, data):
        self.key = key # Ключ вузла
        self.data = data # Дані, що зберігаються у вузлі
        self.height = 1 # Висота вузла для балансування
        self.left = None # Лівий нащадок
        self.right = None # Правий нащадок

class AVLTree:
    """
    Реалізація AVL дерева для підтримки збалансованого бінарного дерева пошуку.
    """
    def __init__(self):
        self.root = None # Кореневий вузол AVL дерева
        self.comparison_count = 0 
    """
    Різні допоміжні методи для операцій AVL дерева, такі як висота, баланс,
    обертання, вставка, видалення тощо."""

    def height(self, node):
        if not node:
            return 0
        return node.height

    def update_height(self, node):
        if not node:
            return 0
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, key, data):
        if not self.root:
            self.root = AVLNode(key, data)
        else:
            self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        self.update_height(node)

        return self.balance_and_update(node)

    def delete(self, key):
        if not self.root:
            return None

        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self.find_min(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self._delete(node.right, temp.key)

        self.update_height(node)

        return self.balance_and_update(node)

    def find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def update(self, key, data):
        node = self._find(self.root, key)
        if node:
            node.data = data

    def search(self, key):
        self.comparison_count = 0  # Скидання лічильника порівнянь перед пошуком
        node = self._find(self.root, key)  # Виконання пошуку
        return node.data if node else None

    def _find(self, node, key):
        while node:
            self.comparison_count += 1  # Збільшуємо лічильник порівнянь
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def balance_and_update(self, node):
        if not node:
            return node

        balance_factor = self.balance(node)

        # Занадто велике відхилення вліво
        if balance_factor > 1:
            # Випадок ліво-правий
            if self.balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
            # Випадок ліво-лівий
            return self.right_rotate(node)

        # Занадто велике відхилення вправо
        if balance_factor < -1:
            # Випадок Право-Лівий
            if self.balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
             # Випадок Право-Правий
            return self.left_rotate(node)

        return node

    """
    Малює AVL дерево за допомогою networkx і matplotlib.
    """ 
    def plot_tree(self):
        G = nx.DiGraph()
        self._plot_tree(self.root, G)
        pos = self._generate_positions(G)

        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=True, arrows=False, node_size=700, node_color='skyblue', font_size=8, font_color='black', ax=ax)
        plt.show()

    def _plot_tree(self, node, G):
        if node:
            if node.left:
                G.add_edge(node.key, node.left.key)
                self._plot_tree(node.left, G)
            if node.right:
                G.add_edge(node.key, node.right.key)
                self._plot_tree(node.right, G)

    def _generate_positions(self, G):
        pos = nx.spring_layout(G)
        return pos

class SimpleDB:
    """
    Клас для створення графічного інтерфейсу для простої бази даних.
    Використовує AVL дерево для зберігання та обробки даних.
    """
    def __init__(self):
        self.avl_tree = AVLTree() # Ініціалізація AVL дерева для зберігання даних
        self.root = tk.Tk() # Ініціалізація головного вікна програми
        self.root.title("Simple DB")

        # Налаштування та розміщення графічних елементів (мітки, кнопки тощо)
        # GUI елементи
        self.label_key = tk.Label(self.root, text="Key:")
        self.entry_key = tk.Entry(self.root)
        self.label_data = tk.Label(self.root, text="Data:")
        self.entry_data = tk.Entry(self.root)
        
        self.button_add = tk.Button(self.root, text="Add Record", command=self.add_record)
        self.button_search = tk.Button(self.root, text="Search Record", command=self.search_record)
        self.button_delete = tk.Button(self.root, text="Delete Record", command=self.delete_record)
        self.button_update = tk.Button(self.root, text="Update Record", command=self.update_record)
        self.button_plot_tree = tk.Button(self.root, text="Plot AVL Tree", command=self.plot_avl_tree)

        self.result_label = tk.Label(self.root, text="Result:")
        
        # Розміщення елементів на GUI
        self.label_key.grid(row=0, column=0)
        self.entry_key.grid(row=0, column=1)
        self.label_data.grid(row=1, column=0)
        self.entry_data.grid(row=1, column=1)

        self.button_add.grid(row=2, column=0, columnspan=2, sticky="we")
        self.button_search.grid(row=3, column=0, columnspan=2, sticky="we")
        self.button_delete.grid(row=4, column=0, columnspan=2, sticky="we")
        self.button_update.grid(row=5, column=0, columnspan=2, sticky="we")
        self.button_plot_tree.grid(row=6, column=0, columnspan=2, sticky="we")
        
        self.result_label.grid(row=7, column=0, columnspan=2, sticky="we")

    # Методи, пов'язані з GUI, такі як add_record, search_record тощо.
    def add_record(self):
        key = int(self.entry_key.get())
        data = self.entry_data.get()
        self.avl_tree.insert(key, data)
        self.clear_entries()

    def search_record(self):
        key = int(self.entry_key.get())
        result = self.avl_tree.search(key)
        if result is not None:
            result_text = f"Data: {result}"
            self.display_result(result_text)
        else:
            self.display_result("Record not found")

    def delete_record(self):
        key = int(self.entry_key.get())
        self.avl_tree.delete(key)
        self.clear_entries()

    def update_record(self):
        key = int(self.entry_key.get())
        data = self.entry_data.get()
        self.avl_tree.update(key, data)
        self.clear_entries()

    def clear_entries(self):
        self.entry_key.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)

    def display_result(self, result):
        self.result_label.config(text=result)

    def plot_avl_tree(self):
        self.avl_tree.plot_tree()

    """
    Запускає основний цикл графічного інтерфейсу.
    """
    def run(self):
        self.root.mainloop()
        
"""Функція для вимірювання та виведення середнього числа порівнянь при пошуку в AVL дереві."""
def measure_comparisons(avl_tree, num_searches=15):
    total_comparisons = 0
    for i in range(num_searches):
        random_key = random.randint(1, 100000)
        avl_tree.search(random_key)
        comparisons = avl_tree.comparison_count
        total_comparisons += comparisons
        print(f"Спроба пошуку {i + 1}: Число порівнянь = {comparisons}")

    average = total_comparisons / num_searches
    print(f"Середнє число порівнянь: {average}")

# Випадкове заповнення бази даних
def fill_database(db, num_records):
    for _ in range(num_records):
        key = random.randint(1, 100000)
        data = f"Data_{key}"
        print(f"{key} : {data}")
        db.avl_tree.insert(key, data)

if __name__ == "__main__":
    db = SimpleDB()
    fill_database(db, 100)
    measure_comparisons(db.avl_tree)
    db.run()
