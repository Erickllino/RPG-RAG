# This module is responsible to read all data in the Data folder
# it should read all txt files and send them in a structured way to the main app
import os
data = dict()
for dirpath, dirnames, filenames in os.walk("Data/Ekalia"):
    for filename in filenames:
        if filename.endswith(".txt"):
            file_path = os.path.join(dirpath, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Process the content as needed
                
                context = {
                    "file name": file_path[12:],  # relative path from Data folder
                    "content": content
                }
                data[context['file name']] = context


                print(f"Read file: {context['file_path']} with content length: {len(content)}")


import pandas as pd
df = pd.DataFrame.from_dict(data, orient='index')
print(df.head())