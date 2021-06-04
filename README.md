# Simple SQL Server database exporter


Dumps all the data & specific queries to disk and upload them to Azure Storage. Can be installed on the Deplro computer and schedulled with windows task scheduler or can be used on an restored backup. 

# dependencies:
* Windows or Linux SQL server
* python 3x
* azure blob.storage package (pip3 install azure.storage.blob)
