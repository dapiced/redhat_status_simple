# Red Hat Status Checker - Simple

A lightweight Python utility to monitor Red Hat service status with global availability tracking and co## 📖 Complete Command Reference

**Version:** 1.0 - Lightweight Edition

## 📋 Overview

This project provides a standalone Red Hat status monitoring tool that fetches real-time status data from Red Hat's official status API and provides various output formats including quick status checks, detailed service hierarchies, and data export capabilities.

Redhat status page is based on the software https://www.atlassian.com/software/statuspage

Redhat status API
- https://status.redhat.com/api/v2/
- https://status.redhat.com/api/v2/summary.json

### Full Featured Version (`redhat_status.py`)

| Command | Description | Output |
|---------|-------------|---------|
| `python3 redhat_status.py --help` | Display help message and usage examples | Shows all available modes and flags |
| `python3 redhat_status.py --version` | Show version information | `Red Hat Status Checker - Simple v1.0` |
| `python3 redhat_status.py quick` | Quick status with global availability (default) | Global status, availability %, health indicator |
| `python3 redhat_status.py quick --quiet` | Minimal output with just availability | Essential info only (availability % and status) |
| `python3 redhat_status.py simple` | Main services only | List of 20 main Red Hat services with status |
| `python3 redhat_status.py full` | Complete hierarchical structure | All 139 services in hierarchical tree format |
| `python3 redhat_status.py export` | Export data to files | Creates timestamped JSON and TXT files |

### Minimalist Version (`redhat_status_minimal.py`)

| Command | Description | Output |
|---------|-------------|---------|
| `python3 redhat_status_minimal.py --help` | Display help message and usage examples | Shows available modes |
| `python3 redhat_status_minimal.py --version` | Show version information | `Red Hat Status Checker - Simple v1.0` |
| `python3 redhat_status_minimal.py quick` | Quick status with global availability (default) | Global status, availability %, health indicator |
| `python3 redhat_status_minimal.py simple` | Main services only | List of main Red Hat services with status |
| `python3 redhat_status_minimal.py full` | Complete hierarchical structure | All services in hierarchical tree format |eporting capabilities.

## 📁 Available Scripts

### `redhat_status.py` - Full Featured Version
The complete version with all features including caching, export functionality, and quiet mode.

### `redhat_status_minimal.py` - Minimalist Version  
A simplified version for users who want just the essential functionality without:
- ❌ Caching system
- ❌ `--quiet` flag  
- ❌ Export functionality

Perfect for users who prefer a clean, simple script with only the core monitoring options: `quick`, `simple`, and `full`.

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

### Choose Your Version

**Full Featured (`redhat_status.py`):**
- Includes caching, export functionality, and quiet mode
- Best for regular monitoring and data export needs

**Minimalist (`redhat_status_minimal.py`):**  
- Essential functionality only (quick, simple, full modes)
- No caching, export, or quiet mode
- Perfect for simple status checks

### Configuration variables inside redhat_status.py

- API_URL = "https://status.redhat.com/api/v2/summary.json"
- REQUEST_TIMEOUT = 10
- MAX_RETRIES = 3
- RETRY_DELAY = 2
- CACHE_TTL = 300  # 5 minutes (full version only)
- CACHE_DIR = ".cache" (full version only)

### Configuration variables inside redhat_status_minimal.py

- API_URL = "https://status.redhat.com/api/v2/summary.json"
- REQUEST_TIMEOUT = 10
- MAX_RETRIES = 3
- RETRY_DELAY = 2

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

**Full Featured Version (`redhat_status.py`):**
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

**Minimalist Version (`redhat_status_minimal.py`):**
```bash
# Quick Status Check (default)
python3 redhat_status_minimal.py quick

# Main services only
python3 redhat_status_minimal.py simple

# Complete service hierarchy
python3 redhat_status_minimal.py full
```

## 🎛️ Command Line Options

### Available Modes (Both Versions)

| Mode | Description |
|------|-------------|
| `quick` | Quick status check with global availability percentage (default) |
| `simple` | Display main services only |
| `full` | Complete hierarchical service structure |

### Additional Modes (Full Version Only)

| Mode | Description |
|------|-------------|
| `export` | Export status data to JSON and text files |

### Flags (Full Version Only)

| Flag | Description |
|------|-------------|
| `--quiet` / `-q` | Minimal output mode (works with quick mode) |
| `--version` / `-v` | Show version information |
| `--help` / `-h` | Display help message |

### Flags (Both Versions)

| Flag | Description |
|------|-------------|
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

### Caching (Full Version Only)
- **Duration**: 5 minutes (300 seconds)
- **Location**: `.cache/summary_data.json`
- **Behavior**: Automatic cache validation and refresh

### Key Differences Between Versions

| Feature | Full Version | Minimalist Version |
|---------|-------------|-------------------|
| Caching | ✅ 5-minute cache | ❌ No caching |
| Export functionality | ✅ JSON & TXT export | ❌ No export |
| Quiet mode | ✅ `--quiet` flag | ❌ No quiet mode |
| Core modes (quick/simple/full) | ✅ | ✅ |
| API retry logic | ✅ | ✅ |
| Global availability calculation | ✅ | ✅ |

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
