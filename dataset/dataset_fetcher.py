import requests
import json
import pandas as pd

# Check if dataset.json exists
# If it does, load the data from the file
# If it doesn't, fetch the data and save it to dataset.json
try:
    with open("dataset.json", "r") as file:
        data = json.load(file)
    print("Data loaded from dataset.json")
except FileNotFoundError:
    offset = 0
    limit = 100
    data = []

    while True:
        if offset == 15000:
            break
        if offset % 100 ==0:
            print(f"Fetching data from offset {offset}")
        url = f"https://datasets-server.huggingface.co/rows?dataset=corbt%2Fall-recipes&config=default&split=train&offset={offset}&length={limit}"
        response = requests.get(url)

        if response.status_code == 200:
            batch_data = response.json()
            data.extend(batch_data['rows'])
            offset += limit
            if len(batch_data['rows']) < limit:
                break
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    with open("dataset.json", "w") as file:
        json.dump(data, file)

    print("Data saved to dataset.json")





print(f"Total number of rows: {len(data)}")

salad_data = [row['row']['input'] for row in data if "salad" in row['row']['input'].lower()]
print(len(salad_data))

print(salad_data[0])
print(salad_data[-1])

# Convert the data to a pandas DataFrame
df = pd.DataFrame(salad_data)

print(df.head())

print(df.shape)

# Save the data to a CSV file
df.to_csv("salad_data.csv", index=False)