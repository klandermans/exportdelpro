# DairyCampus Data Exporter

This project automates the export of dairy farming data to Azure Storage from the DairyCampus database. It extracts various datasets related to body condition score (BCS), milk yield, and more, and uploads them to Azure Storage for further analysis and processing.

## Prerequisites

- Python 3.x
- Azure Blob Storage account
- Azure Storage connection string
- SQL Server Database credentials
- `azure-storage-blob` library (`pip install azure-storage-blob`)

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Replace `[your connection string]` in the script with your Azure Storage connection string.

## Usage

Run the script to export data from the DairyCampus database to Azure Storage.

```bash
python data_export.py
```

## Functionality

- BCS Data Export: Extracts body condition score (BCS) data and uploads it to Azure Storage.
- Raw BCS Data Export: Extracts raw BCS data and uploads it to Azure Storage.
- Milk Yield Data Export: Extracts milk yield data and uploads it to Azure Storage.
- Tables List Generation: Generates a list of tables from the database and stores it locally.
- Export from All Tables: Extracts data from all database tables and uploads each table's data to Azure Storage.

## Notes

Make sure to set up appropriate permissions and configurations for Azure Storage and the SQL Server Database.
Ensure that the script has the necessary permissions to execute database queries and upload files to Azure Storage.
Contributors

## License

This project is licensed under the MIT License - see the LICENSE file for details.
