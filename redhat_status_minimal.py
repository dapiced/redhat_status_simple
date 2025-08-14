#!/usr/bin/env python3
"""
Red Hat Status Checker - Simple Version
A lightweight Python script to check Red Hat service status with global availability percentage.

Usage:
    python3 redhat_status.py quick           # Quick status with availability %
    python3 redhat_status.py simple          # Main services only
    python3 redhat_status.py full            # Complete structure
"""

import requests
import time
import argparse

# Configuration
API_URL = "https://status.redhat.com/api/v2/summary.json"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

def get_summary_data() -> dict:
    """Fetch summary data from Red Hat Status API"""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🌐 Fetching Red Hat Status data... (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                print(f"✅ Data received: {len(response.text)} characters")
                return response.json()
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break
            
        if attempt < MAX_RETRIES - 1:
            print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    
    print(f"❌ Failed to fetch data after {MAX_RETRIES} attempts")
    return None

def calculate_global_availability(components: list) -> tuple:
    """Calculate global availability percentage"""
    if not components:
        return 0.0, 0, 0
    
    total = len(components)
    operational = sum(1 for comp in components if comp.get('status') == 'operational')
    return (operational / total) * 100, operational, total

def get_status_icon(status: str, is_sub_service: bool = False) -> str:
    """Get status icon for a service"""
    icons = {
        'operational': '✅',
        'degraded_performance': '🟡',
        'partial_outage': '🟠',
        'major_outage': '🔴',
        'maintenance': '🔧'
    }
    icon = icons.get(status, '❓')
    return f"  ├─ {icon}" if is_sub_service else icon

def get_status_text(status: str) -> str:
    """Get human-readable status text"""
    texts = {
        'operational': '',
        'degraded_performance': ' - Performance Issues',
        'partial_outage': ' - Partial Outage',
        'major_outage': ' - Major Outage',
        'maintenance': ' - Under Maintenance'
    }
    return texts.get(status, f' - {status.title()}')

def fetch_and_validate_data():
    """Fetch data and return components if successful"""
    data = get_summary_data()
    if not data:
        print("❌ Unable to fetch status data")
        return None
    return data

def quick_status_check() -> None:
    """Quick status check with global availability percentage"""
    data = fetch_and_validate_data()
    if not data:
        return
    
    # Get basic info
    page_info = data.get('page', {})
    status_info = data.get('status', {})
    components = data.get('components', [])
    
    # Calculate global availability
    availability_percent, operational, total = calculate_global_availability(components)
    
    # Display results
    print("🚀 RED HAT GLOBAL STATUS")
    print("=" * 60)
    print(f"📍 Page: {page_info.get('name', 'Unknown')}")
    print(f"🔗 URL: {page_info.get('url', 'Unknown')}")
    print(f"🕒 Last Update: {page_info.get('updated_at', 'Unknown')}")
    print()
    print(f"🔧 STATUS: {status_info.get('description', 'Unknown')}")
    print(f"🏷️  Severity: {status_info.get('indicator', 'Unknown')}")
    print()
    print(f"🟢 GLOBAL AVAILABILITY: {availability_percent:.1f}% ({operational}/{total} services)")
    
    # Health indicator
    if availability_percent >= 99:
        health, icon = "EXCELLENT", "🏥"
    elif availability_percent >= 95:
        health, icon = "GOOD", "✅"
    elif availability_percent >= 90:
        health, icon = "FAIR", "⚠️"
    else:
        health, icon = "POOR", "❌"
    
    print(f"{icon} Overall Health: {health}")
    print()

def simple_check() -> None:
    """Show main services status"""
    data = fetch_and_validate_data()
    if not data:
        return
    
    components = data.get('components', [])
    main_services = [comp for comp in components if comp.get('group_id') is None]
    availability_percent, operational, total = calculate_global_availability(main_services)
    
    print("🔍 RED HAT MAIN SERVICES")
    print("=" * 60)
    print(f"�� Main Services Availability: {availability_percent:.1f}% ({operational}/{total})")
    print()
    
    for service in main_services:
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        icon = get_status_icon(status)
        text = get_status_text(status)
        print(f"{icon} {name}{text}")

def full_check() -> None:
    """Show complete service hierarchy"""
    data = fetch_and_validate_data()
    if not data:
        return
    
    components = data.get('components', [])
    availability_percent, operational, total = calculate_global_availability(components)
    
    print("🌍 RED HAT COMPLETE SERVICE STATUS")
    print("=" * 60)
    print(f"🟢 Global Availability: {availability_percent:.1f}% ({operational}/{total} services)")
    print()
    
    # Group services by parent
    main_services = []
    sub_services = {}
    
    for comp in components:
        if comp.get('group_id') is None:
            main_services.append(comp)
        else:
            group_id = comp.get('group_id')
            if group_id not in sub_services:
                sub_services[group_id] = []
            sub_services[group_id].append(comp)
    
    # Display hierarchical structure
    for service in main_services:
        service_id = service.get('id')
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        
        # Main service status
        icon = get_status_icon(status)
        print(f"{icon} {name}")
        
        # Sub-services
        if service_id in sub_services:
            for sub_service in sub_services[service_id]:
                sub_name = sub_service.get('name', 'Unnamed sub-service')
                sub_status = sub_service.get('status', 'unknown')
                sub_icon = get_status_icon(sub_status, is_sub_service=True)
                print(f"{sub_icon} {sub_name}")

def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Red Hat Status Checker - Simple Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s quick                # Quick status with global availability
  %(prog)s simple               # Main services only  
  %(prog)s full                 # Complete service hierarchy
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['quick', 'simple', 'full'],
        default='quick',
        help='Operation mode (default: quick)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Red Hat Status Checker - Simple v1.0'
    )
    
    return parser

def main():
    """Main function"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        if args.mode == "quick":
            quick_status_check()
        elif args.mode == "simple":
            simple_check()
        elif args.mode == "full":
            full_check()
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
