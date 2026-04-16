# Forensic Data Engine

## Overview
Forensic Data Engine is a professional-grade ETL (Extract, Transform, Load) pipeline designed for the automated processing and analysis of Windows Event Logs (.evtx). The system enables security analysts to ingest large batches of forensic samples, parse them into a relational structure, and perform threat hunting through an interactive dashboard.

## Technical Stack
- Programming Language: Python 3
- Data Processing: Pandas, python-evtx, xmltodict
- Database Management: PostgreSQL, Docker, SQLAlchemy
- Visualization: Streamlit
- Security: SSH Tunneling, .gitignore credential management, python-dotenv

## Dashboard Preview
<p align="center">
  <img src="https://github.com/user-attachments/assets/f5ffe61e-2f68-4cd4-922e-fa0e3f79b384" width="90%" alt="Detailed Logs View" />
  <br>
  <em>Figure 1: Detailed event view with source attribution and timestamp normalization.</em>
</p>

## System Architecture
The project utilizes a hybrid architecture designed for security and scalability:

1. Local Workstation (ETL Module):
   - Extraction: Recursively scans directories for binary .evtx files.
   - Transformation: Parses raw binary data and flattens nested XML structures into structured DataFrames.
   - Loading: Transports cleaned data to the remote database via encrypted SSH tunnels, ensuring the database remains isolated from the public internet.

2. Azure Infrastructure (Storage and Analytics):
   - Database: A containerized PostgreSQL instance for persistent storage of security events.
   - Frontend: A Streamlit-based web application providing real-time data visualization and filtering capabilities.

## Functional Capabilities

### Interactive Analysis
The system provides a structured workflow for analyzing Windows Event Logs through a multi-layered filtering approach.

<table>
  <thead>
    <tr>
      <th width="70%">Feature Details</th>
      <th width="30%">UI Preview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <strong>Data Ingestion</strong><br>
        Processes all event records from provided .evtx files without pre-filtering, ensuring a complete dataset is available for analysis.
      </td>
      <td rowspan="4" align="center" valign="middle">
        <img src="https://github.com/user-attachments/assets/488b08b8-cbef-4248-88e1-c3aa4299e377" width="280" alt="Threat Filters" />
      </td>
    </tr>
    <tr>
      <td>
        <strong>Relational Storage</strong><br>
        Converts unstructured XML event data into a queryable PostgreSQL database via SQLAlchemy.
      </td>
    </tr>
    <tr>
      <td>
        <strong>Contextual Mapping</strong><br>
        Every record is tagged with its original filename to maintain context during multi-file analysis.
      </td>
    </tr>
    <tr>
      <td>
        <strong>Visual Distribution</strong><br>
        Immediate visualization of Event ID frequency to spot anomalies like log clearing or mass logons.
      </td>
    </tr>
  </tbody>
</table>

---

### Visual Insights
The analytical dashboard provides a high-level overview of the ingested forensic samples, highlighting anomalies across the entire dataset.

<p align="center">
  <img src="https://github.com/user-attachments/assets/407d334f-3012-4139-a166-2bf5c0bf0cda" width="95%" alt="Event Distribution Chart" />
  <br>
  <em>Figure 2: Statistical distribution of identified Event IDs across the selected timeframe.</em>
</p>

## Deployment Instructions

### 1. Remote Infrastructure (Azure)
Deploy the database engine on the remote server using the provided configuration:
- Command: `docker-compose up -d`

### 2. Local Environment (ETL Pipeline)
Configure the local environment located in the `/src` directory to ingest logs:
- **Installation**: `pip install -r requirements-etl.txt`
- **Configuration**: Open `load.py` and update the `target_dir` variable with the path to your source `.evtx` files (e.g., `target_dir = "C:/Logs/InvestigatedCase"`).
- **Execution**: `python load.py`
- **SSH Tunnel (Data Ingestion):** An active SSH tunnel to the Azure VM forwarding **Port 5432** is required. This enables the local Python environment to securely communicate with the isolated PostgreSQL container.

### 3. Analytics Interface
Deploy the analytical interface on the remote server to enable real-time visualization:
- Location: `/dashboard`
- Installation: `pip install -r requirements-dashboard.txt`
- Execution: `streamlit run dashboard.py`
- **SSH Tunnel (UI Access):** To access the dashboard locally, establish an SSH tunnel forwarding **Port 8501** (e.g., `ssh -L 8501:localhost:8501 user@azure-ip`). This allows you to interact with the engine via `http://localhost:8501` in your browser while keeping the server's ports closed to the public internet.

## Acknowledgments & Data Source
The sample EVTX files used to build, test, and demonstrate this pipeline were sourced from the community repository created by Samir Bousseaden:
- [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES) - A comprehensive dataset of Windows Event Logs mapped to specific MITRE ATT&CK techniques.
