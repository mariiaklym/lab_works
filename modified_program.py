import heapq
import os
import random
from datetime import datetime

# Генерація великого файлу з випадковими числами
def generate_large_file(filename, size_mb, number_range):
    
    size_in_bytes = size_mb * (1024**2)  # Налаштування розміру до 1000 МБ 
    current_size = 0
    with open(filename, 'w') as file:
        while current_size < size_in_bytes:
            number = random.randint(*number_range)
            line = f"{number}\n"
            file.write(line)
            current_size += len(line.encode('utf-8'))

# Зовншішнє сортування великого файлу
def external_sort(input_file, output_file, block_size_mb):
    start_time = datetime.now()
    # Крок 1: Розбиття на блоки та сортування
    blocks = []
    with open(input_file, 'r') as file:
        while True:
            numbers = []
            try:
                for _ in range(block_size_mb * 250000):  # Збільшення розміру блоку
                    line = file.readline()
                    if line:
                        numbers.append(int(line))
                    else:
                        break
            except MemoryError:
                break

            if not numbers:
                break

            numbers.sort()
            temp_filename = f"temp_{len(blocks)}.txt"
            with open(temp_filename, 'w') as temp_file:
                for num in numbers:
                    temp_file.write(f"{num}\n")
            blocks.append(temp_filename)

    # Крок 2: Багатошляхове злиття
    with open(output_file, 'w') as out_file:
        files = [open(block, 'r') for block in blocks]
        heap = [(int(file.readline()), i) for i, file in enumerate(files) if not file.closed]
        heapq.heapify(heap)

        while heap:
            min_val, file_idx = heapq.heappop(heap)
            out_file.write(f"{min_val}\n")
            next_val = files[file_idx].readline()
            if next_val:
                heapq.heappush(heap, (int(next_val), file_idx))

        for file in files:
            file.close()
            os.remove(file.name)

    end_time = datetime.now()
    duration = end_time - start_time
    minutes = duration.seconds // 60
    seconds = duration.seconds % 60

    print(f"Сортування завершено! Час початку: {start_time.strftime('%H:%M:%S')}, Час закінчення: {end_time.strftime('%H:%M:%S')}, Загальний час сортування: {minutes} хвилин {seconds} секунд")

# Генерація файлу розміром 1000 МБ
generate_large_file("large_file.txt", 1000, (0, 1000000))

# Сортування файлу зі збільшеним розміром блоку
external_sort("large_file.txt", "sorted_file.txt", 400)  # Збільшення розміру блоку для кращої продуктивності
