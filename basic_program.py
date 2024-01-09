import heapq
import os
import random
import time

def generate_large_file(filename, size_mb, number_range):
    num_numbers = (size_mb * (1024**2)) // 4
    with open(filename, 'w') as file:
        for _ in range(num_numbers):
            file.write(f"{random.randint(*number_range)}\n")

def external_sort(input_file, output_file, block_size_mb):
    start_time = time.time()  # Початок засікування часу

    # Крок 1: Розбиття на блоки та їх сортування
    blocks = []
    with open(input_file, 'r') as file:
        while True:
            numbers = []
            for _ in range(block_size_mb * 250000):
                line = file.readline()
                if line:
                    numbers.append(int(line))
                else:
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

    end_time = time.time()  # Кінець засікування часу
    print(f"Сортування завершено! Час сортування: {end_time - start_time:.2f} секунд.")

# Приклад використання
generate_large_file("large_file.txt", 10, (0, 100000))
external_sort("large_file.txt", "sorted_file.txt", 1)
