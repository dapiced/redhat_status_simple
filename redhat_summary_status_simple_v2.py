import requests
import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configuration constants
DEFAULT_CONFIG = {
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
        "show_percentages": True,
        "show_health_indicator": True,
        "show_group_summaries": True
    }
}

def load_config() -> Dict[str, Any]:
    """Load configuration from config_simple.json or use defaults"""
    config_file = os.path.join(os.path.dirname(__file__), 'config_simple.json')
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            for section, values in user_config.items():
                if section in config:
                    config[section].update(values)
                else:
                    config[section] = values
            
            return config
        except Exception as e:
            print(f"⚠️  Warning: Could not load config file ({e}), using defaults")
            return DEFAULT_CONFIG
    
    return DEFAULT_CONFIG

# Load configuration
CONFIG = load_config()
API_URL = CONFIG["api"]["url"]
REQUEST_TIMEOUT = CONFIG["api"]["timeout"]
MAX_RETRIES = CONFIG["api"]["max_retries"]
RETRY_DELAY = CONFIG["api"]["retry_delay"]

def get_summary_data() -> Optional[Dict[str, Any]]:
    """Retrieve and parse summary.json with native json library"""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🌐 Fetching Red Hat Status data... (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()  # Native JSON parsing!
                print(f"✅ Data received: {len(response.text)} characters")
                return data
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                    import time
                    time.sleep(RETRY_DELAY)
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                import time
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                import time
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break
    
    print(f"❌ Failed to fetch data after {MAX_RETRIES} attempts")
    return None

def calculate_global_availability(components: List[Dict[str, Any]]) -> tuple:
    """Calculate global availability percentage"""
    if not components:
        return 0.0, 0, 0
    
    total_services = len(components)
    operational_services = sum(1 for comp in components if comp.get('status') == 'operational')
    availability_percentage = (operational_services / total_services) * 100
    
    return availability_percentage, operational_services, total_services

def quick_status_check(quiet_mode: bool = False) -> None:
    """1. Global status - PYTHON3 VERSION with global availability percentage"""
    data = get_summary_data()
    if not data:
        return
    
    # Direct access to JSON data
    page_info = data.get('page', {})
    status_info = data.get('status', {})
    components = data.get('components', [])
    
    # Calculate global availability
    availability_percent, operational, total = calculate_global_availability(components)
    
    if quiet_mode:
        # Quiet mode: just show the essential info
        print(f"🌐 Global Availability: {availability_percent:.1f}% ({operational}/{total} services)")
        print(f"📍 Status: {status_info.get('description', 'Unknown')}")
        return
    
    # Full output mode
    print("\n" + "="*60)
    print("🚀 RED HAT GLOBAL STATUS")
    print("="*60)
    
    print(f"📍 Page: {page_info.get('name', 'N/A')}")
    print(f"🔗 URL: {page_info.get('url', 'N/A')}")
    print(f"🕒 Last Update: {page_info.get('updated_at', 'N/A')}")
    
    indicator = status_info.get('indicator', 'unknown')
    description = status_info.get('description', 'No description')
    
    # Status mapping with emojis
    status_map = {
        "none": ("🟢", "All Systems Operational"),
        "minor": ("🟡", "Minor Issues"),
        "major": ("🔴", "Major Outage"),
        "critical": ("🚨", "Critical Issues"),
        "maintenance": ("🔧", "Service Under Maintenance")
    }
    
    emoji, status_text = status_map.get(indicator, ("⚪", f"Unknown Status ({indicator})"))
    print(f"\n{emoji} STATUS: {description}")
    print(f"🏷️  Severity: {status_text}")
    print()
    print(f"🟢 GLOBAL AVAILABILITY: {availability_percent:.1f}% ({operational}/{total} services)")
    
    # Health indicator
    if availability_percent >= 99:
        health = "EXCELLENT"
        health_icon = "🏥"
    elif availability_percent >= 95:
        health = "GOOD" 
        health_icon = "✅"
    elif availability_percent >= 90:
        health = "FAIR"
        health_icon = "⚠️"
    else:
        health = "POOR"
        health_icon = "❌"
    
    print(f"{health_icon} Overall Health: {health}")

def simple_check_only() -> Optional[List[Dict[str, Any]]]:
    """2. Main services - PYTHON3 VERSION"""
    print("\n" + "="*60)
    print("🏢 RED HAT MAIN SERVICES")
    print("="*60)
    
    data = get_summary_data()
    if not data:
        return None
    
    components = data.get('components', [])
    print(f"📊 Total components in API: {len(components)}")
    
    # Filter main services (group_id is null)
    main_services = [comp for comp in components if comp.get('group_id') is None]
    
    print(f"🎯 Main services found: {len(main_services)}")
    print("-" * 60)
    
    operational_count = 0
    problem_count = 0
    
    for service in main_services:
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        
        if status == "operational":
            print(f"✅ {name}")
            operational_count += 1
        else:
            print(f"❌ {name} - {status.upper()}")
            problem_count += 1
    
    print("-" * 60)
    print(f"📈 SUMMARY: {operational_count} operational, {problem_count} with issues")
    
    # Calculate and display percentage
    total_services = operational_count + problem_count
    if total_services > 0 and CONFIG["display"]["show_percentages"]:
        percentage = (operational_count / total_services) * 100
        print(f"📊 Availability: {percentage:.1f}%")
    
    return main_services

def full_check_with_services() -> None:
    """3. ALL services with hierarchy - PYTHON3 VERSION"""
    print("\n" + "="*80)
    print("🏗️  COMPLETE RED HAT STRUCTURE - ALL SERVICES")
    print("="*80)
    
    data = get_summary_data()
    if not data:
        return
    
    components = data.get('components', [])
    
    # Organize by hierarchy
    main_services = {}
    sub_services = {}
    
    # Create dictionaries to facilitate organization
    for comp in components:
        comp_id = comp.get('id')
        name = comp.get('name', 'Unnamed service')
        status = comp.get('status', 'unknown')
        group_id = comp.get('group_id')
        
        if group_id is None:
            # Main service
            main_services[comp_id] = {
                'name': name,
                'status': status,
                'id': comp_id
            }
        else:
            # Sub-service
            if group_id not in sub_services:
                sub_services[group_id] = []
            sub_services[group_id].append({
                'name': name,
                'status': status,
                'id': comp_id
            })
    
    print(f"📊 STATISTICS:")
    print(f"   • Main services: {len(main_services)}")
    print(f"   • Sub-service groups: {len(sub_services)}")
    print(f"   • Total components: {len(components)}")
    print()
    
    total_operational = 0
    total_problems = 0
    service_details = []  # For summary statistics
    
    # Display hierarchical structure
    for service_id, service_info in main_services.items():
        name = service_info['name']
        status = service_info['status']
        
        # Main service
        if status == "operational":
            print(f"🟢 {name}")
            total_operational += 1
            service_details.append({'name': name, 'status': 'operational', 'type': 'main'})
        else:
            print(f"🔴 {name} - {status.upper()}")
            total_problems += 1
            service_details.append({'name': name, 'status': status, 'type': 'main'})
        
        # Display sub-services of this group
        if service_id in sub_services:
            sub_list = sub_services[service_id]
            print(f"   📁 {len(sub_list)} sub-services:")
            
            sub_operational = 0
            sub_problems = 0
            
            for sub in sub_list:
                sub_name = sub['name']
                sub_status = sub['status']
                
                if sub_status == "operational":
                    print(f"      ✅ {sub_name}")
                    total_operational += 1
                    sub_operational += 1
                    service_details.append({'name': sub_name, 'status': 'operational', 'type': 'sub'})
                else:
                    print(f"      ❌ {sub_name} - {sub_status.upper()}")
                    total_problems += 1
                    sub_problems += 1
                    service_details.append({'name': sub_name, 'status': sub_status, 'type': 'sub'})
            
            # Sub-group summary
            if sub_operational + sub_problems > 0 and CONFIG["display"]["show_group_summaries"]:
                sub_percentage = (sub_operational / (sub_operational + sub_problems)) * 100
                print(f"   📈 Group availability: {sub_percentage:.1f}%")
        
        print()  # Empty line between groups
    
    # Display "orphan" sub-services (groups without identified parent)
    orphan_groups = set(sub_services.keys()) - set(main_services.keys())
    if orphan_groups:
        print("🔧 OTHER SERVICES:")
        for group_id in orphan_groups:
            sub_list = sub_services[group_id]
            print(f"   📁 Group {group_id[:8]}... ({len(sub_list)} services):")
            
            for sub in sub_list:
                sub_name = sub['name']
                sub_status = sub['status']
                
                if sub_status == "operational":
                    print(f"      ✅ {sub_name}")
                    total_operational += 1
                    service_details.append({'name': sub_name, 'status': 'operational', 'type': 'orphan'})
                else:
                    print(f"      ❌ {sub_name} - {sub_status.upper()}")
                    total_problems += 1
                    service_details.append({'name': sub_name, 'status': sub_status, 'type': 'orphan'})
    
    print("=" * 80)
    print(f"📊 TOTAL OVERALL: {total_operational} operational, {total_problems} with issues")
    
    # Calculate percentage
    total_services = total_operational + total_problems
    if total_services > 0:
        percentage = (total_operational / total_services) * 100
        if CONFIG["display"]["show_percentages"]:
            print(f"📈 Availability rate: {percentage:.1f}%")
        
        # Additional statistics
        if CONFIG["display"]["show_group_summaries"]:
            main_count = len([s for s in service_details if s['type'] == 'main'])
            sub_count = len([s for s in service_details if s['type'] == 'sub'])
            orphan_count = len([s for s in service_details if s['type'] == 'orphan'])
            
            print(f"🔢 Service breakdown: {main_count} main, {sub_count} sub-services, {orphan_count} other")
        
        # Health indicator
        if CONFIG["display"]["show_health_indicator"]:
            if percentage >= 95:
                print("🟢 Overall health: EXCELLENT")
            elif percentage >= 90:
                print("🟡 Overall health: GOOD")
            elif percentage >= 80:
                print("🟠 Overall health: FAIR")
            else:
                print("🔴 Overall health: POOR")

def export_to_file(output_dir: str = ".") -> None:
    """Bonus: Export data to file"""
    print("\n💾 DATA EXPORT")
    print("-" * 40)
    
    data = get_summary_data()
    if not data:
        return
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
    filename = os.path.join(output_dir, f"redhat_status_{timestamp}.json")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Get file size
        file_size = os.path.getsize(filename)
        file_size_kb = file_size / 1024
        
        print(f"✅ Data exported to: {filename}")
        print(f"📊 File size: {file_size_kb:.1f} KB ({file_size} bytes)")
        print(f"📅 Export time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Also create a summary report if configured
        if CONFIG["output"]["create_summary_report"]:
            summary_filename = os.path.join(output_dir, f"redhat_summary_{timestamp}.txt")
            create_summary_report(data, summary_filename)
        
    except Exception as e:
        print(f"❌ Export error: {str(e)}")

def create_summary_report(data: Dict[str, Any], filename: str) -> None:
    """Create a human-readable summary report"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RED HAT STATUS SUMMARY REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Page info
            page_info = data.get('page', {})
            f.write(f"Page: {page_info.get('name', 'N/A')}\n")
            f.write(f"URL: {page_info.get('url', 'N/A')}\n")
            f.write(f"Last Update: {page_info.get('updated_at', 'N/A')}\n\n")
            
            # Status info
            status_info = data.get('status', {})
            f.write(f"Status: {status_info.get('description', 'No description')}\n")
            f.write(f"Indicator: {status_info.get('indicator', 'unknown')}\n\n")
            
            # Components summary
            components = data.get('components', [])
            operational = sum(1 for comp in components if comp.get('status') == 'operational')
            total = len(components)
            issues = total - operational
            
            f.write(f"Components Summary:\n")
            f.write(f"  Total: {total}\n")
            f.write(f"  Operational: {operational}\n")
            f.write(f"  With Issues: {issues}\n")
            if total > 0:
                percentage = (operational / total) * 100
                f.write(f"  Availability: {percentage:.1f}%\n")
            
            f.write(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"📋 Summary report created: {filename}")
        
    except Exception as e:
        print(f"❌ Error creating summary report: {str(e)}")

def create_config_file() -> None:
    """Create or update config_simple.json file with default settings"""
    config_file = os.path.join(os.path.dirname(__file__), 'config_simple.json')
    
    print("🔧 SIMPLE VERSION CONFIGURATION SETUP")
    print("=" * 50)
    
    if os.path.exists(config_file):
        print(f"📄 Configuration file already exists: {config_file}")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response not in ['y', 'yes']:
            print("⏹️  Setup cancelled")
            return
    
    try:
        config_data = {
            "_comment": "Configuration file for Red Hat Status Checker Simple Versions (v1 and v2)",
            "_note": "This is a simplified configuration with only essential settings",
            "_versions": "redhat_summary_status_simple_v1.py (uses no config), redhat_summary_status_simple_v2.py (uses this config)",
            
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
                "show_percentages": True,
                "show_health_indicator": True,
                "show_group_summaries": True
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration file created: {config_file}")
        print("📋 Configuration summary:")
        print(f"   • API URL: {config_data['api']['url']}")
        print(f"   • Timeout: {config_data['api']['timeout']} seconds")
        print(f"   • Max retries: {config_data['api']['max_retries']}")
        print(f"   • Show percentages: {config_data['display']['show_percentages']}")
        print(f"   • Show health indicators: {config_data['display']['show_health_indicator']}")
        print("\n🎯 You can now run the simple v2 script with configuration support!")
        
    except Exception as e:
        print(f"❌ Error creating configuration file: {str(e)}")

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Red Hat Status Checker - Monitor Red Hat services status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --setup            # Create config_simple.json file
  %(prog)s                    # Interactive mode
  %(prog)s quick              # Quick status only
  %(prog)s simple             # Main services check
  %(prog)s full               # Complete structure
  %(prog)s export             # Export data to files
  %(prog)s all                # Display everything
  %(prog)s export --output ./reports  # Export to specific directory
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['quick', 'simple', 'full', 'export', 'all'],
        default=None,
        help='Operation mode (if not specified, interactive mode is used)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory for exported files (default: current directory)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode - minimal output'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Create or update config_simple.json configuration file'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Red Hat Status Checker Simple v2.0'
    )
    
    return parser

def main():
    """Main function with improved argument handling"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Handle setup mode first
    if args.setup:
        create_config_file()
        return
    
    if not args.quiet:
        print("🎯 RED HAT STATUS CHECKER - SIMPLE VERSION v2.0")
        print("=" * 60)
    
    mode = args.mode
    
    # Interactive mode if no arguments provided
    if mode is None:
        print("Available modes:")
        print("  quick    - Global status only")
        print("  simple   - Main services")
        print("  full     - Complete structure")
        print("  export   - Export data")
        print("  all      - Display all")
        print()
        mode = input("Choose a mode (or press Enter for 'all'): ").lower()
        if not mode:
            mode = "all"
        
        # Validate interactive input
        if mode not in ['quick', 'simple', 'full', 'export', 'all']:
            print(f"❌ Mode '{mode}' not recognized")
            return
    
    try:
        if mode == "quick":
            quick_status_check(quiet_mode=args.quiet)
        elif mode == "simple":
            quick_status_check(quiet_mode=args.quiet)
            simple_check_only()
        elif mode == "full":
            quick_status_check(quiet_mode=args.quiet)
            simple_check_only()
            full_check_with_services()
        elif mode == "export":
            export_to_file(args.output)
        elif mode == "all":
            quick_status_check(quiet_mode=args.quiet)
            simple_check_only()
            full_check_with_services()
            export_to_file(args.output)
            
        if not args.quiet:
            print(f"\n✅ Operation completed successfully!")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()