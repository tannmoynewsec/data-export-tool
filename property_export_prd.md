# Product Requirements Document (PRD)

## 1. Product Title
**Property Management Data Export Tool**

---

## 2. Purpose
To streamline the monthly review, correction, commenting, and export of property management data. The tool enables users to edit tabular property data in a spreadsheet-like interface, attach comments for review, and export it to Excel/CSV formats and/or save it directly to Microsoft Fabric Lakehouse or Data Warehouse tables.

---

## 3. Target Users

| User Role        | Responsibilities                                    |
| ---------------- | --------------------------------------------------- |
| Property Manager | View and correct property data, add comments        |
| Finance Team     | Download approved monthly data in required formats  |
| Data Engineer    | Validate/save monthly data into Lakehouse/DW tables |
| Admin/Reviewer   | Lock monthly data, verify comments and changes      |

---

## 4. Key Features

| Feature                     | Description                                                             |
| --------------------------- | ----------------------------------------------------------------------- |
| Excel-like Table View       | Editable grid displaying property data                                  |
| Row-level Commenting        | Inline comment field for suggested corrections                          |
| Data Validation             | Option to validate fields (e.g., numeric rent, mandatory fields)        |
| Monthly Export              | Export current state to Excel, CSV, or Text file (for SAP system integration) with timestamped filename |
## | Save to Fabric Lakehouse/DW | Push final version to a predefined Fabric storage (Lakehouse or SQL DW) |
| Save to DW | Push final version to a predefined storage (SQL DW) |
| Edit History/Audit Trail    | Optional feature to track changes and user who made them                |
| Access Control (Optional)   | Restrict actions based on user role (view-only, edit, export, save)     |

---

## 5. Data Model

The following data model is designed to be modular and reusable across multiple internal projects, and supports dynamic extension—fields can be added or modified as needed to align with project-specific requirements or schema changes.

### Shared Data Model - Property Records

| Field Name       | Type    | Required | Description                    |
| ---------------- | ------- | -------- | ------------------------------ |
| Property ID      | Integer | Yes      | Unique ID of property          |
| Property Name    | String  | Yes      | Property name                  |
| Unit Count       | Integer | Yes      | Number of active units         |
| Occupancy Rate   | Decimal | No       | Occupancy rate (percentage)    |
| Total Rent       | Decimal | Yes      | Total monthly rent             |
| Comment          | String  | No       | Comment for this record        |
| Last Modified By | String  | No       | (Optional) Logged-in user name |

The same schema can be exported or referenced via shared model files for consistency across applications.

### Field Extensibility for Export Scenarios

The data model supports dynamic schema adjustments. Fields can be added, modified, or excluded based on export target requirements (e.g., SAP), project variations, or changes in the Fabric Lakehouse schema.

---

## 6. User Workflow

1. User logs into the internal web app  
2. Loads existing monthly data (auto-fetch from underlying Fabric table or user upload if unavailable)  
3. Views & edits data inline via grid  
4. Adds row-level comments (if needed)  
5. Exports data to Excel, CSV, or Text file (for SAP)  
6. Optionally submits edited data to update Microsoft Fabric Lakehouse/Data Warehouse  

---

## 7. Functional Requirements

| ID   | Requirement                                                                   |
|------|-------------------------------------------------------------------------------|
| FR1  | The system shall allow users to edit data inline in a grid format            |
| FR2  | The system shall support adding comments per record                          |
| FR3  | The system shall export data to Excel and CSV and text formats                        |
| FR4  | The system shall generate filenames with the format `property_export_YYYY-MM`|
| FR5  | The system shall push data to Fabric Lakehouse or DW on request              |
| FR6  | The system shall validate required fields before saving or exporting         |
| FR7  | The system shall be accessible internally via web browser                    |
| FR8  | The system shall allow users to submit edited records to update the underlying Fabric Lakehouse/Data Warehouse table |

---

## 8. Non-Functional Requirements

| ID   | Requirement                                                             |
|------|-------------------------------------------------------------------------|
| NFR1 | App shall support at least 5 concurrent users                           |
| NFR2 | Response time for data load/edit/export shall be under 2 seconds        |
| NFR3 | Exported files shall be downloadable via browser                        |
| NFR4 | All operations must comply with company’s internal data security policy |

---

## 9. Integration Requirements

### Microsoft Fabric Lakehouse
### - Method: Via Spark API or REST endpoint or direct blob write

### Data Warehouse (Azure Synapse / SQL DW)
- Method: `pyodbc`, `SQLAlchemy`, or Azure SDK-based connection

---

## 10. Milestones & Timeline

| Milestone               | Target Date  |
|-------------------------|--------------|
| Requirements Finalized  | XXXXXX, 2025 |
| MVP Build (UI + Export) | XXXXXX, 2025 |
| Fabric Integration      | XXXXXX, 2025 |
| UAT/Testing             | XXXXXX, 2025 |
| Go Live                 | XXXXXX, 2025 |

---

## 11. Backend Data Source Integration

### Objective
Fetch property-related data monthly from a backend **Fabric Lakehouse table** to auto-populate the data grid.

| ID  | Requirement                                                                 |
|-----|-----------------------------------------------------------------------------|
| BE1 | The backend shall connect to a Fabric Lakehouse table via Spark or REST API |
| BE2 | The backend shall query the lakehouse table filtered by a `year`and `month` columns|
| BE3 | The response data shall populate the Streamlit grid                         |
| BE4 | If query fails or returns no data, user shall see an appropriate message    |

**Data Fields from Fabric Table:**
- Property ID
- Property Name
- Unit Count
- Occupancy Rate
- Total Rent
- (Optional) Comment (if previously stored)

---