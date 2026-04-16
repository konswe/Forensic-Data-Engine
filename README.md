# Forensic Data Engine

## Overview
Forensic Data Engine is a professional-grade ETL (Extract, Transform, Load) pipeline designed for the automated processing and analysis of Windows Event Logs (.evtx). The system enables security analysts to ingest large batches of forensic samples, parse them into a relational structure, and perform threat hunting through an interactive dashboard.

## System Architecture
The project utilizes a hybrid architecture designed for security and scalability:

1. Local Workstation (ETL Module):
   - Extraction: Recursively scans directories for binary .evtx files.
   - Transformation: Parses raw binary data and flattens nested XML structures into structured DataFrames.
   - Loading: Transports cleaned data to the remote database via encrypted SSH tunnels, ensuring the database remains isolated from the public internet.

2. Azure Infrastructure (Storage and Analytics):
   - Database: A containerized PostgreSQL instance for persistent storage of security events.
   - Frontend: A Streamlit-based web application providing real-time data visualization and filtering capabilities.

## Deployment Instructions

### 1. Remote Infrastructure (Azure)
Deploy the database engine on the remote server using the provided configuration:
- Command: docker-compose up -d

### 2. Local Environment (ETL Pipeline)
Configure the local environment located in the /src directory:
- Installation: pip install -r requirements.txt
- Execution: python load.py (Note: Ensure the SSH tunnel to the Azure VM is active)

### 3. Analytics Interface
Run the dashboard on the server to access the analytical interface:
- Location: /dashboard
- Installation: pip install -r requirements.txt
- Execution: streamlit run dashboard.py

## Functional Capabilities
The system provides a structured workflow for analyzing Windows Event Logs:
- Data Ingestion: Processes all event records from provided .evtx files, ensuring a complete dataset is available for analysis.
- Relational Storage: Converts unstructured XML event data into a queryable PostgreSQL database.
- Interactive Analysis: The dashboard allows users to filter the entire dataset by Computer Name, Event ID, and Source File.
- Contextual Mapping: Every record is tagged with its original filename to maintain context during multi-file analysis.

## Technical Stack
- Programming Language: Python 3
- Data Processing: Pandas, python-evtx, xmltodict
- Database Management: PostgreSQL, Docker, SQLAlchemy
- Visualization: Streamlit
- Security: SSH Tunneling, .gitignore credential management

## Acknowledgments & Data Source
The sample EVTX files used to build, test, and demonstrate this pipeline were sourced from the community repository created by Samir Bousseaden:
- [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) - A comprehensive dataset of Windows Event Logs mapped to specific MITRE ATT&CK techniques.
