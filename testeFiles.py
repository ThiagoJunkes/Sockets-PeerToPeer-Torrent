import os

local = os.path.dirname(os.path.realpath(__file__))

files_client = []

for file in os.listdir(local):
    
    if file.endswith(".txt"):
        files_client.append(str(file))
        print(os.path.join("arquivos: ", file))

for file in files_client:
    print(file)