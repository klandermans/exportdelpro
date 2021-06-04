# Simple SQL database exporter

# Dumps all the data & specific queries to disk and upload them to Azure Storage.
# Can be used for the export of delpro software but also for other sql server software. I scheduled this software through the windows task scheduler to run every day. 

# dependencies:
# Windows or Linux SQL server
# python 3x
# azure blob.storage package (pip3 install azure.storage.blob)

import os
import os, uuid

# Azure dependendies for uploading to storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.common.models import LocationMode
from azure.storage.common.retry import (
    ExponentialRetry,
    LinearRetry,
    no_retry,
)

#generic upload function
def upload(source, destination):
    blob_client2 = blob_service_client.get_blob_client(container='dairycampus', blob=destination)
    # Upload the created file
    with open(source, "rb") as data:
        print('Uploading source')
        blob_client2.upload_blob(data,overwrite=True)

#connect with azure storage
blob_service_client = False
blob_connection_string = "[your connection string]"
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

#export Body Condition sore
sql = 'select  dateandtime as date,      (select number from basicanimal as a  where a.oid=Animal and birthdate<dateandtime and (ExitDate is null or exitdate>dateandtime )) as cow,     bcsvalue from bcsdailydata as bcs order by date desc'
cmd = "bcp \""+sql+"\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999  -b 10000   -a 10000 -k  -T"
os.system(cmd)
upload('export\\wurbcs.csv','datain/laval_robot/wurbcs.csv')

#export raw condition score
sql = "SELECT [DateAndTime],(select number from basicanimal as a  where a.oid=Animal and birthdate<[DateAndTime] and (ExitDate is null or exitdate>[DateAndTime] )) as cow ,[BcsRawValue]  ,[Quality]   ,[BcsCamera]   ,[OptimisticLockField] ,[GCRecord] FROM [DDM].[dbo].[BcsCameraRawData]"
cmd = "bcp \""+sql+"\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999  -b 10000   -a 10000 -k  -T"
os.system(cmd)
upload('export\\wurbcs.csv','datain/laval_robot/wurrawbcs.csv')

#export Milk Yield
sql = 'SELECT (select number from basicanimal as a  where a.oid=Animal and birthdate<[DayDate] and (ExitDate is null or exitdate>[DayDate] )) as cow, * FROM [DDM].[dbo].[HistoryAnimalDailyData]   order by daydate desc'
cmd = "bcp \""+sql+"\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999  -b 10000   -a 10000 -k  -T"
os.system(cmd)
upload('export\\wurbcs.csv','datain/laval_robot/wurmilk.csv')

#create tables.txt and store file on disk
os.system('sqlcmd <sqlexport.sql>tables.txt')

#clean tables.txt
tables = open('tables.txt', "r").read()
tables = tables.split('--------------------------------------------------------------------------------------------------------------------------------')
tables = tables[1].split('\n\n')
tables = tables[0].split('\n')

#export all tables
for table in tables:
    table = table.rstrip(' ')
    #skip empty lines
    if table =="":
        continue
    #dump data using microsofts Bulk command line tool 
    cmd = "bcp dbo."+table+" out export\\"+table+".csv -dDDM -c -t, -m 9999  -b 10000   -a 10000 -k  -T"
    os.system(cmd)
    upload('export\\'+table+'.csv','datain/laval_robot/'+table)
