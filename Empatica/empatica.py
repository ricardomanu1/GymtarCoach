import boto3
import glob
import os

BUCKET_NAME = "empatica-us-east-1-prod-data"
PREFIX = "v2/451/"
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(BUCKET_NAME)
bucket.objects.all()

def get_full_data(id_serial,date):    
    data_serial = id_serial + '_' + date + '_'

    files = [data_serial + "activity-classification.csv", data_serial + "eda.csv", data_serial + "movement-intensity.csv",
             data_serial + "prv.csv", data_serial + "pulse-rate.csv", data_serial + "respiratory-rate.csv",
             data_serial + "sleep-detection.csv", data_serial + "temperature.csv", data_serial + "wearing-detection.csv"]

    for my_bucket_object in bucket.objects.filter(Prefix = PREFIX):   
        print(my_bucket_object.key)     
        file_name = my_bucket_object.key.split('/')[-1]
        if file_name in files:             
            selected_file = file_name
            selected_key = my_bucket_object.key      
            s3_resource.meta.client.download_file(BUCKET_NAME, selected_key, selected_file)

def remove_full_data(id_serial,date):    
    data_serial_csv = id_serial + '_' + date + '*.csv'
    archivos = glob.glob(os.path.join('', data_serial_csv))
    for archivo in archivos:
        os.remove(archivo)

get_full_data('1-1-01','2023-06-21')    

#remove_full_data('1-1-01','2023-06-21')