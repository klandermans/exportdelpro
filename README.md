# Simple SQL Server database exporter


Dumps all the data & specific queries to disk and upload them to Azure Storage. Can be used for the export of Delpro software but also for other sql server software. I scheduled this software through the windows task scheduler to run every day. 

# dependencies:
* Windows or Linux SQL server
* python 3x
* azure blob.storage package (pip3 install azure.storage.blob)
