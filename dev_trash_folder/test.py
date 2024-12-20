import json
import os
from pathlib import Path

p = Path(__file__).parents[0]

cv = json.loads(open(os.path.join(p, "test.txt"), "r").read())

# List of file paths to check
file_paths = []

for i in cv["obj"]["cv"]:
    file_paths.append("assets/" + i[1:])

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

count_existing = 0
count_not_existing = 0
list_not_existing = []

# Loop through the list and check if each file exists
for relative_path in file_paths:
    # Create the full path to the file
    full_path = os.path.join(script_dir, relative_path)
    
    # Check if the file exists
    if os.path.isfile(full_path):
        print(f"File exists: {relative_path}")
        count_existing += 1
    else:
        print(f"File not found: {relative_path}")
        count_not_existing += 1
        list_not_existing.append(relative_path)

print(count_existing)
print(count_not_existing)

with open(os.path.join(p, "output.json"), 'w') as file:
    file.write(json.dumps(list_not_existing))