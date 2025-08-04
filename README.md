# Red Hat Status Checker - Simple Versions

A lightweight Python utility to monitor Red Hat service status with global availability tracking and comprehensive reporting capabilities.

## 📋 Overview

This project provides two versions of a Red Hat status monitoring tool:
- **Version 1 (v1)**: Standalone script with built-in configuration
- **Version 2 (v2)**: Enhanced version with external configuration support

Both versions fetch real-time status data from Red Hat's official status API and provide various output formats including quick status checks, detailed service hierarchies, and data export capabilities.

## ✨ Features

- 🌐 **Global Availability Tracking**: Calculate and display overall service availability percentage
- 📊 **Multiple Display Modes**: Quick, simple, full hierarchical, and export modes
- 🔄 **Smart Caching**: 5-minute cache to reduce API calls and improve performance
- 📁 **Data Export**: Export status data to JSON and text summary files
- 🎯 **Health Indicators**: Visual health status with emoji indicators
- ⚙️ **Configurable**: Version 2 supports external configuration files
- 🔁 **Retry Logic**: Automatic retry with exponential backoff for API failures
- 🎨 **Rich Output**: Color-coded status indicators and structured formatting

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- `requests` library

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

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your preferred settings
source .env
```

### Basic Usage

#### Version 1 (Standalone)
```bash
# Quick status with global availability
python3 redhat_status_simple_v1.py quick

# Quiet mode (minimal output)
python3 redhat_status_simple_v1.py quick --quiet

# Main services only
python3 redhat_status_simple_v1.py simple

# Complete service hierarchy
python3 redhat_status_simple_v1.py full

# Export data to files
python3 redhat_status_simple_v1.py export
```

#### Version 2 (Configurable)
```bash
# Same commands as v1, but uses config_simple.json for settings
python3 redhat_status_simple_v2.py quick
python3 redhat_status_simple_v2.py simple
python3 redhat_status_simple_v2.py full
python3 redhat_status_simple_v2.py export
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

### Version 1 Commands (redhat_status_simple_v1.py)

| Command | Description | Output |
|---------|-------------|---------|
| `python3 redhat_status_simple_v1.py --help` | Display help message and usage examples | Shows all available modes and flags |
| `python3 redhat_status_simple_v1.py --version` | Show version information | `Red Hat Status Checker - Simple v1.0` |
| `python3 redhat_status_simple_v1.py quick` | Quick status with global availability (default) | Global status, availability %, health indicator |
| `python3 redhat_status_simple_v1.py quick --quiet` | Minimal output with just availability | Essential info only (availability % and status) |
| `python3 redhat_status_simple_v1.py simple` | Main services only | List of 20 main Red Hat services with status |
| `python3 redhat_status_simple_v1.py full` | Complete hierarchical structure | All 139 services in hierarchical tree format |
| `python3 redhat_status_simple_v1.py export` | Export data to files | Creates timestamped JSON and TXT files |

### Version 2 Commands (redhat_status_simple_v2.py)

| Command | Description | Output |
|---------|-------------|---------|
| `python3 redhat_status_simple_v2.py --help` | Display help message with enhanced options | Shows all modes, flags, and examples |
| `python3 redhat_status_simple_v2.py --version` | Show version information | `Red Hat Status Checker Simple v2.0` |
| `python3 redhat_status_simple_v2.py --setup` | Create/update configuration file | Interactive setup for config_simple.json |
| `python3 redhat_status_simple_v2.py quick` | Enhanced quick status with branding | Detailed global status with v2 formatting |
| `python3 redhat_status_simple_v2.py quick --quiet` | Minimal output mode | Essential availability and status info |
| `python3 redhat_status_simple_v2.py simple` | Enhanced main services display | Global status + main services with statistics |
| `python3 redhat_status_simple_v2.py full` | Complete structure with group stats | All services with group availability percentages |
| `python3 redhat_status_simple_v2.py export --output test_exports` | Export to custom directory | Creates JSON file in specified directory |
| `python3 redhat_status_simple_v2.py all` | Comprehensive display (all features) | Global + main + full + export in one command |

### Additional Version 2 Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--output DIR` / `-o DIR` | Specify output directory for exports | `--output ./reports` |
| `--setup` | Interactive configuration setup | Creates/updates config_simple.json |

## �📊 Output Examples

### Quick Status (Default)
```
🚀 RED HAT GLOBAL STATUS
============================================================
📍 Page: Red Hat Status
🔗 URL: https://status.redhat.com
🕒 Last Update: 2025-08-04T10:30:00Z

🟢 STATUS: All Systems Operational
🏷️  Severity: All Systems Operational

🟢 GLOBAL AVAILABILITY: 98.5% (127/129 services)
🏥 Overall Health: EXCELLENT
```

### Simple Mode (Main Services)
```
🔍 RED HAT MAIN SERVICES
============================================================
🟢 Main Services Availability: 100.0% (12/12)

✅ Red Hat Enterprise Linux
✅ Red Hat OpenShift Online
✅ Red Hat Customer Portal
🟡 Red Hat Insights - Performance Issues
✅ Red Hat Satellite
```

### Full Mode (Hierarchical)
```
🌍 RED HAT COMPLETE SERVICE STATUS
============================================================
🟢 Global Availability: 98.5% (127/129 services)

✅ Red Hat Enterprise Linux
  ├─ ✅ RHEL 8
  ├─ ✅ RHEL 9
  ├─ 🟡 RHEL 7 Extended Support

✅ Red Hat OpenShift
  ├─ ✅ OpenShift Online
  ├─ ✅ OpenShift Dedicated
```

## ⚙️ Configuration

### Version 2 Configuration (config_simple.json)

```json
{
  "api": {
    "url": "https://status.redhat.com/api/v2/summary.json",
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 2
  },
  "output": {
    "default_directory": ".",
    "timestamp_format": "%Y%m%d_%H%M%S"
  },
  "display": {
    "show_percentages": true,
    "show_health_indicator": true,
    "show_group_summaries": true
  }
}
```

### Environment Variables (.env)

```bash
export REDHAT_STATUS_API_URL="https://status.redhat.com/api/v2/summary.json"
export REDHAT_STATUS_TIMEOUT=15
export REDHAT_STATUS_MAX_RETRIES=5
export REDHAT_STATUS_RETRY_DELAY=3
```

## 📁 File Structure

```
redhat_summary_status_simple/
├── README.md                              # This file
├── redhat_status_simple_v1.py             # Standalone version
├── redhat_status_simple_v2.py             # Configurable version
├── config_simple.json                     # Configuration file (v2)
├── .env.example                           # Environment variables template
├── .cache/                                # Cache directory (auto-created)
│   └── summary_data.json                  # Cached API responses
└── exports/                               # Export files (auto-created)
    ├── redhat_status_YYYYMMDD_HHMMSS.json
    └── redhat_summary_YYYYMMDD_HHMMSS.txt
```

## 🔧 Technical Details

### API Endpoint
- **URL**: `https://status.redhat.com/api/v2/summary.json`
- **Method**: GET
- **Response**: JSON with service status information

### Caching
- **Duration**: 5 minutes (300 seconds)
- **Location**: `.cache/summary_data.json`
- **Behavior**: Automatic cache validation and refresh

### Status Mapping
| API Status | Display | Icon |
|------------|---------|------|
| `operational` | Operational | ✅ |
| `degraded_performance` | Performance Issues | 🟡 |
| `partial_outage` | Partial Outage | 🟠 |
| `major_outage` | Major Outage | 🔴 |
| `maintenance` | Under Maintenance | 🔧 |

### Health Indicators
- **EXCELLENT** (≥99%): 🏥
- **GOOD** (95-98.9%): ✅
- **FAIR** (90-94.9%): ⚠️
- **POOR** (<90%): ❌

## 🐛 Troubleshooting

### Common Issues

1. **Network Connection Errors**
   ```
   ❌ Network error: Connection timeout
   ```
   - Check internet connectivity
   - Verify firewall settings
   - Try increasing timeout in configuration

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
python3 -v redhat_status_simple_v1.py quick
```

## 📈 Version Differences

| Feature | Version 1 | Version 2 |
|---------|-----------|-----------|
| Configuration | Hard-coded | External JSON config |
| Setup Complexity | Simple | Moderate |
| Customization | Limited | Highly configurable |
| Dependencies | requests only | requests only |
| File Size | Smaller | Larger |
| Best For | Quick usage | Production deployments |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source. Please check the repository for specific license details.

## 🔗 Related Links

- [Red Hat Status Page](https://status.redhat.com)
- [Red Hat Status API Documentation](https://status.redhat.com/api/v2/)
- [Python Requests Documentation](https://docs.python-requests.org/)

## 📞 Support

For issues, questions, or contributions:
- Open an issue in the repository
- Check existing documentation
- Review troubleshooting section above

---

**Last Updated**: August 2025  
**Compatible Python Versions**: 3.6+  
**API Version**: v2

