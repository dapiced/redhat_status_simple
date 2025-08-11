# Red Hat Status Checker - Simple

A lightweight Python utility to monitor Red Hat service status with global availability tracking and comprehensive reporting capabilities.

**Version:** 1.0 - Lightweight Edition

## 📋 Overview

This project provides a standalone Red Hat status monitoring tool that fetches real-time status data from Red Hat's official status API and provides various output formats including quick status checks, detailed service hierarchies, and data export capabilities.

## 📋 Démo CLI Redhat Status

![Démo CLI Redhat Status](./redhat_status.svg)

## ✨ Features

- 🌐 **Global Availability Tracking**: Calculate and display overall service availability percentage
- 📊 **Multiple Display Modes**: Quick, simple, full hierarchical, and export modes
- 🔄 **Smart Caching**: 5-minute cache to reduce API calls and improve performance
- 📁 **Data Export**: Export status data to JSON and text summary files
- 🎯 **Health Indicators**: Visual health status with emoji indicators
- 🔁 **Retry Logic**: Automatic retry with exponential backoff for API failures
- 🎨 **Rich Output**: Color-coded status indicators and structured formatting

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- `requests` library

### Configuration variables inside redhat_status.py

- API_URL = "https://status.redhat.com/api/v2/summary.json"
- REQUEST_TIMEOUT = 10
- MAX_RETRIES = 3
- RETRY_DELAY = 2
- CACHE_TTL = 300  # 5 minutes
- CACHE_DIR = ".cache"

### Installation

1. Clone or download the repository:
```bash
git clone <repository-url>
cd redhat_summary_status_simple
```

2. Install dependencies:
```bash
pip install requests
```

### Basic Usage

```bash
# Quick Status Check
python3 redhat_status.py quick

# Quiet mode (minimal output)
python3 redhat_status.py quick --quiet

# Main services only
python3 redhat_status.py simple

# Complete service hierarchy
python3 redhat_status.py full

# Export data to files
python3 redhat_status.py export
```

## 🎛️ Command Line Options

### Available Modes

| Mode | Description |
|------|-------------|
| `quick` | Quick status check with global availability percentage (default) |
| `simple` | Display main services only |
| `full` | Complete hierarchical service structure |
| `export` | Export status data to JSON and text files |

### Flags

| Flag | Description |
|------|-------------|
| `--quiet` / `-q` | Minimal output mode (works with quick mode) |
| `--version` / `-v` | Show version information |
| `--help` / `-h` | Display help message |

## � Complete Command Reference

### Available Commands

| Command | Description | Output |
|---------|-------------|---------|
| `python3 redhat_status.py --help` | Display help message and usage examples | Shows all available modes and flags |
| `python3 redhat_status.py --version` | Show version information | `Red Hat Status Checker - Simple v1.0` |
| `python3 redhat_status.py quick` | Quick status with global availability (default) | Global status, availability %, health indicator |
| `python3 redhat_status.py quick --quiet` | Minimal output with just availability | Essential info only (availability % and status) |
| `python3 redhat_status.py simple` | Main services only | List of 20 main Red Hat services with status |
| `python3 redhat_status.py full` | Complete hierarchical structure | All 139 services in hierarchical tree format |
| `python3 redhat_status.py export` | Export data to files | Creates timestamped JSON and TXT files |

## 🔧 Technical Details

### API Endpoint
- **URL**: `https://status.redhat.com/api/v2/summary.json`
- **Method**: GET
- **Response**: JSON with service status information

### Caching
- **Duration**: 5 minutes (300 seconds)
- **Location**: `.cache/summary_data.json`
- **Behavior**: Automatic cache validation and refresh

## 🐛 Troubleshooting

### Common Issues

1. **Network Connection Errors**
   ```
   ❌ Network error: Connection timeout
   ```
   - Check internet connectivity
   - Verify firewall settings
   - Modify timeout values directly in the script if needed

2. **API Rate Limiting**
   ```
   ❌ HTTP Error: 429
   ```
   - Wait before retrying
   - Cache is automatically used to reduce API calls

3. **Permission Errors**
   ```
   ⚠️  Cache write error: Permission denied
   ```
   - Check write permissions in script directory
   - Ensure `.cache` directory is writable

### Debug Mode

For verbose output, you can modify the scripts to add debug logging or run with Python's verbose flag:

```bash
python3 -v redhat_status.py quick
```
---
