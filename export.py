import os
from azure.storage.blob import BlobServiceClient

# Function to upload file to Azure Storage
def upload_to_azure(source, destination):
    blob_client = blob_service_client.get_blob_client(container='dairycampus', blob=destination)
    with open(source, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

# Connect to Azure Storage
blob_connection_string = "[your connection string]"
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

# Export Body Condition Score data
sql_bcs = 'select dateandtime as date, (select number from basicanimal as a where a.oid=Animal and birthdate<dateandtime and (ExitDate is null or exitdate>dateandtime )) as cow, bcsvalue from bcsdailydata as bcs order by date desc'
cmd_bcs = "bcp \"" + sql_bcs + "\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999 -b 10000 -a 10000 -k -T"
os.system(cmd_bcs)
upload_to_azure('export\\wurbcs.csv', 'datain/laval_robot/wurbcs.csv')

# Export raw condition score data
sql_raw_bcs = "SELECT [DateAndTime], (select number from basicanimal as a where a.oid=Animal and birthdate<[DateAndTime] and (ExitDate is null or exitdate>[DateAndTime] )) as cow ,[BcsRawValue], [Quality], [BcsCamera], [OptimisticLockField], [GCRecord] FROM [DDM].[dbo].[BcsCameraRawData]"
cmd_raw_bcs = "bcp \"" + sql_raw_bcs + "\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999 -b 10000 -a 10000 -k -T"
os.system(cmd_raw_bcs)
upload_to_azure('export\\wurbcs.csv', 'datain/laval_robot/wurrawbcs.csv')

# Export Milk Yield data
sql_milk = 'SELECT (select number from basicanimal as a where a.oid=Animal and birthdate<[DayDate] and (ExitDate is null or exitdate>[DayDate] )) as cow, * FROM [DDM].[dbo].[HistoryAnimalDailyData] order by daydate desc'
cmd_milk = "bcp \"" + sql_milk + "\" queryout export\\wurbcs.csv -dDDM -c -t, -m 9999 -b 10000 -a 10000 -k -T"
os.system(cmd_milk)
upload_to_azure('export\\wurbcs.csv', 'datain/laval_robot/wurmilk.csv')

# Generate and store tables list
os.system('sqlcmd <sqlexport.sql>tables.txt')
tables = open('tables.txt', "r").read()
tables = tables.split('--------------------------------------------------------------------------------------------------------------------------------')
tables = tables[1].split('\n\n')
tables = tables[0].split('\n')

# Export data from all tables
for table in tables:
    table = table.rstrip(' ')
    if table == "":
        continue
    cmd = "bcp dbo." + table + " out export\\" + table + ".csv -dDDM -c -t, -m 9999 -b 10000 -a 10000 -k -T"
    os.system(cmd)
    upload_to_azure('export\\' + table + '.csv', 'datain/laval_robot/' + table)
