import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

districts_villages = {
    "Nashik": ["Sinnar", "Igatpuri", "Yeola", "Nandgaon", "Dindori", "Trimbakeshwar"],
    "Pune": ["Haveli", "Baramati", "Indapur", "Shirur", "Mulshi", "Maval"],
    "Nagpur": ["Katol", "Kamptee", "Hingna", "Umred", "Parseoni", "Ramtek"],
    "Thane": ["Bhiwandi", "Kalyan", "Ulhasnagar", "Shahapur", "Murbad", "Ambernath"],
    "Aurangabad": ["Paithan", "Gangapur", "Kannad", "Khultabad", "Vaijapur", "Soegaon"],
    "Solapur": ["Mohol", "Pandharpur", "Barshi", "Akkalkot", "North Solapur", "Malshiras"],
    "Kolhapur": ["Karvir", "Panhala", "Radhanagari", "Hatkanangle", "Kagal", "Gadhinglaj"],
    "Amravati": ["Achalpur", "Chandur Bazar", "Morshi", "Anjangaon", "Warud", "Dhamangaon"],
    "Nanded": ["Ardhapur", "Bhokar", "Biloli", "Degloor", "Hadgaon", "Kinwat"],
    "Jalgaon": ["Amalner", "Bhusawal", "Chopda", "Erandol", "Muktainagar", "Pachora"],
}

rows = []

# Normal usage (Label = 0) - 500 samples
for _ in range(500):
    district = random.choice(list(districts_villages.keys()))
    village = random.choice(districts_villages[district])
    voltage = round(random.uniform(215, 235), 1)
    current = round(random.uniform(3, 10), 2)
    power = round(voltage * current * random.uniform(0.85, 0.98))
    time = round(random.uniform(8, 24), 1)
    meter_diff = round(power * time / 1000 * random.uniform(0.9, 1.1), 2)
    rows.append(["Maharashtra", district, village, voltage, current, power, time, meter_diff, 0])

# Theft usage (Label = 1) - 500 samples
for _ in range(500):
    district = random.choice(list(districts_villages.keys()))
    village = random.choice(districts_villages[district])
    theft_type = random.randint(1, 4)

    if theft_type == 1:  # Direct hooking - high current, low voltage
        voltage = round(random.uniform(180, 210), 1)
        current = round(random.uniform(18, 30), 2)
        power = round(voltage * current * random.uniform(0.5, 0.7))
        time = round(random.uniform(1, 5), 1)
        meter_diff = round(power * time / 1000 * random.uniform(0.1, 0.3), 2)  # meter barely moves

    elif theft_type == 2:  # Meter tampering - high consumption, low meter diff
        voltage = round(random.uniform(215, 235), 1)
        current = round(random.uniform(15, 25), 2)
        power = round(voltage * current * random.uniform(0.85, 0.98))
        time = round(random.uniform(8, 20), 1)
        meter_diff = round(power * time / 1000 * random.uniform(0.05, 0.2), 2)  # tampered

    elif theft_type == 3:  # Bypass - sudden power spike
        voltage = round(random.uniform(235, 260), 1)
        current = round(random.uniform(20, 35), 2)
        power = round(random.uniform(5000, 9000))
        time = round(random.uniform(2, 6), 1)
        meter_diff = round(power * time / 1000 * random.uniform(0.4, 0.6), 2)

    else:  # Illegal connection - very short time, high power
        voltage = round(random.uniform(215, 235), 1)
        current = round(random.uniform(12, 22), 2)
        power = round(random.uniform(3500, 6000))
        time = round(random.uniform(0.5, 2.0), 1)
        meter_diff = round(power * time / 1000 * random.uniform(0.2, 0.5), 2)

    rows.append(["Maharashtra", district, village, voltage, current, power, time, meter_diff, 1])

df = pd.DataFrame(rows, columns=["State", "District", "Village", "Voltage", "Current", "Power", "Time", "MeterDiff", "Label"])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("dataset.csv", index=False)
print(f"Dataset generated: {len(df)} rows, {df['Label'].sum()} theft cases")
