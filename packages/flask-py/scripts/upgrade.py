import os

with open('outdated.txt', 'r') as file:
    # Skip the header line
    next(file)
    for line in file:
        # Extract the package name (first column)
        package_name = line.split()[0]
        print(f"Upgrading {package_name}")
        os.system(f"pip install --upgrade {package_name}")
