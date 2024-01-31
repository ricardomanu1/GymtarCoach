from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os

avro_file_path = "1-1-01_1687343523.avro"   # 19 jun 2023 16:37:38  #(15 minutos de duracion)
# timestamp to human date (necesario)
output_dir = "1-1-01_1687343523"
## Read Avro file
reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
data= next(reader)
## Print the Avro schema
print(schema)
print(" ")

## Export sensors data to csv files

# Accelerometer
acc = data["rawData"]["accelerometer"]
timestamp = [round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
 for i in range(len(acc["x"]))]
with open(os.path.join(output_dir, 'accelerometer.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "x", "y", "z"])
 writer.writerows([[ts, x, y, z] for ts, x, y, z in zip(timestamp, acc["x"], acc["y"], acc["z"])])

# Gyroscope
gyro = data["rawData"]["gyroscope"]
timestamp = [round(gyro["timestampStart"] + i * (1e6 / gyro["samplingFrequency"]))
 for i in range(len(gyro["x"]))]
with open(os.path.join(output_dir, 'gyroscope.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "x", "y", "z"])
 writer.writerows([[ts, x, y, z] for ts, x, y, z in zip(timestamp, gyro["x"], gyro["y"], gyro["z"])])

 # Eda
eda = data["rawData"]["eda"]
timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
 for i in range(len(eda["values"]))]
with open(os.path.join(output_dir, 'eda.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "eda"])
 writer.writerows([[ts, eda] for ts, eda in zip(timestamp, eda["values"])])

# Temperature
tmp = data["rawData"]["temperature"]
timestamp = [round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
 for i in range(len(tmp["values"]))]
with open(os.path.join(output_dir, 'temperature.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "temperature"])
 writer.writerows([[ts, tmp] for ts, tmp in zip(timestamp, tmp["values"])])

# Tags
tags = data["rawData"]["tags"]
with open(os.path.join(output_dir, 'tags.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["tags_timestamp"])
 writer.writerows([[tag] for tag in tags["tagsTimeMicros"]])

# BVP
bvp = data["rawData"]["bvp"]
timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
 for i in range(len(bvp["values"]))]
with open(os.path.join(output_dir, 'bvp.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "bvp"])
 writer.writerows([[ts, bvp] for ts, bvp in zip(timestamp, bvp["values"])])

# Systolic peaks
sps = data["rawData"]["systolicPeaks"]
with open(os.path.join(output_dir, 'systolic_peaks.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["systolic_peak_timestamp"])
 writer.writerows([[sp] for sp in sps["peaksTimeNanos"]])

# Steps
steps = data["rawData"]["steps"]
timestamp = [round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
 for i in range(len(steps["values"]))]
with open(os.path.join(output_dir, 'steps.csv'), 'w', newline='') as f:
 writer = csv.writer(f)
 writer.writerow(["unix_timestamp", "steps"])
 writer.writerows([[ts, step] for ts, step in zip(timestamp, steps["values"])])