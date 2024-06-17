import pandas as pd
import matplotlib.pyplot as plt
import re

# Read the text file
with open('chat.txt', 'r') as file:
    data = file.readlines()

# Extract timestamps and create a DataFrame
timestamps = []
for line in data:
    match = re.match(r'(\d{1,2}:\d{2}) \|', line)
    if match:
        timestamps.append(match.group(1))

# Create a DataFrame
df = pd.DataFrame(timestamps, columns=['timestamp'])

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%M:%S')

# Count the number of messages per timestamp
message_counts = df['timestamp'].value_counts().sort_index()

# Plot the quantity of messages over time
plt.figure(figsize=(10, 5))
plt.plot(message_counts.index, message_counts.values, marker='o')
plt.xlabel('Time')
plt.ylabel('Number of Messages')
plt.title('Quantity of Messages Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
