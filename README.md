# Property Data Export Tool

A streamlined web application for managing, viewing, editing, and exporting property data from Azure Synapse Analytics.

## Overview

The Property Data Export Tool is a Streamlit-based application that allows users to:

- View property data with filtering capabilities by year-month and property ID
- Edit property details including occupancy rates, total rent, and comments
- Mark specific records as edited
- Export data to Excel or CSV formats
- Save changes back to Azure Synapse Analytics

## Features

- **User Authentication**: Secure login system
- **Data Filtering**: Filter by Year-Month or Property ID
- **Interactive Data Editor**: Edit property data with validation
- **Manual Editing Tracking**: Users must check the "Edited" box for rows they modify
- **Export Options**: Download data as Excel or CSV
- **Database Integration**: Updates to Azure Synapse Analytics

## Technical Details

### Data Refresh Workflow

1. **Initial Load**: 
   - On application start, data is loaded from Azure Synapse Analytics (`[dbo].[PropertyExport]` table)
   - Falls back to sample data if database connection fails

2. **Filter-based Refresh**:
   - Data refreshes when users change Year-Month or Property ID filters
   - Only filtered data is displayed in the editor

3. **Save Operation**:
   - Data is written to the database only when the "Save" button is clicked
   - Only rows marked with the "Edited" checkbox are updated
   - The "Last Modified By" field is automatically updated with the current username

### Database Schema

The application uses the following table structure:

```sql
[dbo].[PropertyExport] (
    [Year-Month] NVARCHAR(7),
    [Property ID] INT,
    [Property Name] NVARCHAR(255),
    [Unit Count] INT,
    [Occupancy Rate] FLOAT,
    [Total Rent] FLOAT,
    [Comment] NVARCHAR(255),
    [Last Modified By] NVARCHAR(255),
    [Edited] BIT
)
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Azure Synapse Analytics instance
- ODBC Driver 17 for SQL Server

### Environment Variables

Configure the following environment variables:

```
SYNAPSE_ENV=dev|prod
SYNAPSE_SERVER=your-synapse-server.sql.azuresynapse.net
SYNAPSE_USERNAME=your-username
SYNAPSE_PASSWORD=your-password
SYNAPSE_DATABASE=your-database
SYNAPSE_TABLE=[dbo].[PropertyExport]
```

### Installation

1. Clone the repository
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the application:

```powershell
streamlit run property_export_app.py
```

## User Guide

1. **Login**: Enter your credentials on the login screen
2. **Filter Data**: Use the Year-Month and Property ID dropdowns to filter data
3. **Edit Data**: Modify property details in the data grid
4. **Mark Edits**: Check the "Edited" box for any rows you've modified
5. **Save**: Click the "Save" button to commit changes to the database
6. **Export**: Use the Excel or CSV buttons to export data

## Important Notes

- Always check the "Edited" box for any rows you've modified before saving
- The "Property ID" and "Last Modified By" fields are read-only
- Filter selections are not preserved after a save operation

## Troubleshooting

- If database connection fails, check your environment variables
- Ensure you have proper permissions to access the Synapse database
- Check for proper ODBC driver installation if experiencing connection issues

## Contributors

- Stronghold Invest AB team

## License

Internal use only - Stronghold Invest AB
