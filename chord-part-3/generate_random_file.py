import os
import sys
import random
import string

def create_random_text_file(file_path, file_size):
    # Generate random content
    with open(file_path, 'w') as file:
        remaining_size = file_size
        while remaining_size > 0:
            # Generate a random string of size min(remaining_size, chunk_size)
            chunk_size = min(1024, remaining_size)  # Write in chunks of 1 KB
            random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=chunk_size))
            file.write(random_text)
            remaining_size -= chunk_size

kbs = int(sys.argv[1])
file_name = sys.argv[2]

# Usage
target_size = kbs * 1024  # KBs to bytes
create_random_text_file(file_name, target_size)
print(f"File '{file_name}' of size {target_size} bytes created.")
