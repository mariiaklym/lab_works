import time
import sys

# Функція для читання лабіринту з файлу та визначення стартової, кінцевої точок і самого лабіринту
def read_maze(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start = tuple(map(int, lines[0].split()))
        goal = tuple(map(int, lines[1].split()))
        maze = [[int(num) for num in line.split()] for line in lines[2:]]
    return maze, start, goal

# Функція для отримання наступників вузла в лабіринті
def get_successors(maze, node):
    successors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Вниз, Вправо, Вгору, Вліво
    for dx, dy in directions:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0:
            successors.append((x, y))
    return successors

# Функція для перевірки часового обмеження
def check_time_limit(start_time, time_limit_sec):
    if time.time() - start_time > time_limit_sec:
        print("Часове обмеження перевищено")
        sys.exit()

# Функція для пошуку в глибину з обмеженням
def dls(maze, node, goal, depth, max_depth=0, generated=0, start_time=None, time_limit_sec=None):
    check_time_limit(start_time, time_limit_sec)
    generated += 1
    if depth == 0 and node == goal:
        return [node], 1, generated
    if depth > 0:
        max_depth_reached = max_depth
        for successor in get_successors(maze, node):
            path, depth_reached, gen = dls(maze, successor, goal, depth - 1, max_depth_reached + 1, generated, start_time, time_limit_sec)
            max_depth_reached = max(max_depth_reached, depth_reached)
            generated = gen
            if path:
                return [node] + path, max_depth_reached, generated
    return [], max_depth, generated

# Функція для ітеративного поглиблення
def ids(maze, start, goal, max_depth=50, start_time=None, time_limit_sec=None):
    total_generated = 0
    for depth in range(max_depth):
        path, depth_reached, generated = dls(maze, start, goal, depth, start_time=start_time, time_limit_sec=time_limit_sec)
        total_generated += generated
        if path:
            return path, depth, depth_reached, total_generated
    return [], 0, 0, total_generated

# Функція для обчислення манхеттенської відстані
def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Функція для алгоритму A*
def a_star(maze, start, goal, start_time=None, time_limit_sec=None):
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    max_in_memory = 0
    total_generated = 0

    while open_set:
        check_time_limit(start_time, time_limit_sec)
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, len(path), max_in_memory, total_generated

        open_set.remove(current)
        for neighbor in get_successors(maze, current):
            total_generated += 1
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)
            max_in_memory = max(max_in_memory, len(open_set) + len(came_from))

    return [], 0, 0, 0

# Функція для виведення лабіринту з шляхом
def print_maze(maze, start, goal, path=None):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == goal:
                print("G", end=" ")
            elif path and (i, j) in path:
                print("·", end=" ")
            else:
                print("#" if val == 1 else " ", end=" ")
        print()

# Виконання алгоритмів
maze_file = 'maze.txt'  
maze, start, goal = read_maze(maze_file)

# Часові обмеження
start_time = time.time()
time_limit_sec = 30 * 60  # 30 хвилин

# Виконання алгоритмів IDS і A*
path_ids, steps_ids, memory_ids, generated_ids = ids(maze, start, goal, start_time=start_time, time_limit_sec=time_limit_sec)
path_a_star, steps_a_star, memory_a_star, generated_a_star = a_star(maze, start, goal, start_time=start_time, time_limit_sec=time_limit_sec)

# Виведення результатів
if len(maze) <= 20 and len(maze[0]) <= 20:
    print("Лабіринт:")
    print_maze(maze, start, goal)

print("Початкова точка:", start)
print("Кінцева точка:", goal)
print("IDS: шлях -", path_ids, "\nІтерації -", steps_ids, "\nВсього станів у пам'яті -", memory_ids, "\nКількість згенерованих станів -", generated_ids)
print("A*: шлях -", path_a_star, "\nІтерації -", steps_a_star, "\nВсього станів у пам'яті -", memory_a_star, "\nКількість згенерованих станів -", generated_a_star)
