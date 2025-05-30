# Switchboard Parts Script

A Python script that generates detailed parts reports for switchboard assemblies. The script calculates the required pieces for each section of a switchboard and generates a professional PDF report.

## Features

- Calculate parts for multiple switchboard sections
- Support for both standard (S) and corner (L) sections
- Generate professional PDF reports with detailed breakdowns
- Track dimension totals for width, height, and depth pieces
- Docker support for easy deployment

## Requirements

- Python 3.11
- Docker (optional)

## Installation

### Using Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t switchboardpartsscript .
```

2. Run the script:

**Easy Option for Windows Users:**
Simply double-click one of these batch files:
- `run-downloads.bat` - Saves PDFs to your Downloads folder
- `run-local.bat` - Saves PDFs to the project output directory

**Manual Docker Commands:**

**Option 1: Save to your Downloads folder (Recommended for Windows):**
```bash
docker run -it -v "//c/Users/YOUR_USERNAME/Downloads:/app/output" switchboardpartsscript
```
Note: Replace `YOUR_USERNAME` with your actual Windows username (e.g., johnparadise)

**Option 2: Save to project directory:**

For Windows:
```bash
docker run -it -v "//c/Users/YOUR_USERNAME/programming/switchboardPartsScript/output:/app/output" switchboardpartsscript
```
Note: Replace `YOUR_USERNAME` with your Windows username and adjust the path to match your project location.

For Linux/Mac:
```bash
docker run -it -v ${PWD}/output:/app/output switchboardpartsscript
```

The PDF will be saved in your specified directory (Downloads folder or project output directory).

### Manual Installation

1. Install Python 3.11
2. Install required packages:
```bash
pip install reportlab
```

## Usage

1. Run the script
2. Enter the required information when prompted:
   - Sales Order Number
   - Customer Name
   - Job Name/Address
   - Switchboard Name
   - Number of Sections
   - Section Dimensions
   - Section Types (S or L)
3. The script will generate a PDF report with all the parts information

## Report Format

The generated PDF report includes:
- Switchboard details
- Section-by-section breakdown
- Dimension totals for width, height, and depth pieces
- Separate tracking for standard and corner pieces