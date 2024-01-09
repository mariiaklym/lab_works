import random
import numpy as np

# Параметри
num_nodes = 150
num_ants = 35
alpha = 2
beta = 3
rho = 0.4
iterations = 1000
distance_range = (5, 50)

# Функція для генерації матриці відстаней
def generate_distance_matrix(num_nodes, distance_range):
    matrix = np.random.randint(distance_range[0], distance_range[1], size=(num_nodes, num_nodes))
    np.fill_diagonal(matrix, 0)
    return matrix

# Жадібний алгоритм для знаходження Lmin
def greedy_algorithm(distance_matrix, start_node=0):
    path = [start_node]
    total_distance = 0

    while len(path) < num_nodes:
        last_node = path[-1]
        next_node = np.argmin([distance_matrix[last_node][i] if i not in path else float('inf') for i in range(num_nodes)])
        path.append(next_node)
        total_distance += distance_matrix[last_node][next_node]

    total_distance += distance_matrix[path[-1]][path[0]]  # Повернення до початкової точки
    return total_distance

# Функція для розрахунку ймовірності
def calculate_probability(from_node, to_node, pheromone_matrix, distance_matrix):
    pheromone = pheromone_matrix[from_node][to_node] ** alpha
    inverse_distance = (1.0 / distance_matrix[from_node][to_node]) ** beta
    return pheromone * inverse_distance

# Клас мурахи
class Ant:
    def __init__(self):
        self.path = []
        self.total_distance = 0

  
    def find_path(self, distance_matrix, pheromone_matrix):
            self.path = [random.randint(0, num_nodes - 1)]
            self.total_distance = 0

            for _ in range(num_nodes - 1):
                current_node = self.path[-1]
                probabilities = [calculate_probability(current_node, i, pheromone_matrix, distance_matrix) if i not in self.path else 0 for i in range(num_nodes)]

                if sum(probabilities) > 0:
                    next_node = random.choices(range(num_nodes), probabilities, k=1)[0]
                else:
                    # Всі ймовірності рівні нулю, обираємо випадковий невідвіданий вузол
                    unvisited_nodes = [i for i in range(num_nodes) if i not in self.path]
                    next_node = random.choice(unvisited_nodes)

                self.path.append(next_node)
                self.total_distance += distance_matrix[current_node][next_node]

            # Повернення до початкової точки
            self.total_distance += distance_matrix[self.path[-1]][self.path[0]]

# Функція для оновлення феромону
def update_pheromone(pheromone_matrix, ants, rho):
    pheromone_matrix *= (1 - rho)  # Випаровування феромону
    for ant in ants:
        for i in range(num_nodes - 1):
            pheromone_matrix[ant.path[i]][ant.path[i+1]] += 1.0 / ant.total_distance

# Ініціалізація
distance_matrix = generate_distance_matrix(num_nodes, distance_range)
pheromone_matrix = np.ones_like(distance_matrix, dtype=float)
ants = [Ant() for _ in range(num_ants)]
best_path = None
best_distance = float('inf')

# Жадібний алгоритм для знаходження Lmin
lmin = greedy_algorithm(distance_matrix)

# Основний цикл алгоритму
for iteration in range(iterations):
    for ant in ants:
        ant.find_path(distance_matrix, pheromone_matrix)
        if ant.total_distance < best_distance:
            best_distance = ant.total_distance
            best_path = ant.path[:]

    update_pheromone(pheromone_matrix, ants, rho)

    if iteration % 20 == 0:
        print(f"Ітерація {iteration}: Краща відстань = {best_distance}")

# Вивід найкращого знайденого шляху
print(f"Найкращий шлях: {best_path}")
print(f"Найкраща відстань: {best_distance}")
