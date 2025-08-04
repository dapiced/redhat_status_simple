#!/usr/bin/env python3
"""
Red Hat Status Checker - Simple Version
A lightweight Python script to check Red Hat service status with global availability percentage.

Features:
- Quick status check with global availability percentage
- Simple service listing
- Full hierarchical service structure
- Data export capabilities
- Basic caching for performance

Usage:
    python3 redhat_summary_status_simple.py quick           # Quick status with availability %
    python3 redhat_summary_status_simple.py quick --quiet   # Quiet mode with just availability %
    python3 redhat_summary_status_simple.py simple          # Main services only
    python3 redhat_summary_status_simple.py full            # Complete structure
    python3 redhat_summary_status_simple.py export          # Export to files
"""

import requests
import json
import os
import time
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
API_URL = "https://status.redhat.com/api/v2/summary.json"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2
CACHE_TTL = 300  # 5 minutes
CACHE_DIR = ".cache"

def get_cache_file() -> Path:
    """Get cache file path"""
    cache_dir = Path(CACHE_DIR)
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / "summary_data.json"

def is_cache_valid(cache_file: Path) -> bool:
    """Check if cache is valid and not expired"""
    if not cache_file.exists():
        return False
    
    try:
        file_age = time.time() - cache_file.stat().st_mtime
        return file_age < CACHE_TTL
    except Exception:
        return False

def load_from_cache() -> dict:
    """Load data from cache if valid"""
    cache_file = get_cache_file()
    
    if is_cache_valid(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                print("📋 Using cached data")
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Cache read error: {e}")
    
    return None

def save_to_cache(data: dict) -> None:
    """Save data to cache"""
    try:
        cache_file = get_cache_file()
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️  Cache write error: {e}")

def get_summary_data() -> dict:
    """Fetch summary data from Red Hat Status API"""
    # Try cache first
    cached_data = load_from_cache()
    if cached_data:
        return cached_data
    
    # Fetch from API
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🌐 Fetching Red Hat Status data... (attempt {attempt + 1}/{MAX_RETRIES})")
            
            response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Data received: {len(response.text)} characters")
                
                # Save to cache
                save_to_cache(data)
                
                return data
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break
    
    print(f"❌ Failed to fetch data after {MAX_RETRIES} attempts")
    return None

def calculate_global_availability(components: list) -> tuple:
    """Calculate global availability percentage"""
    if not components:
        return 0.0, 0, 0
    
    total_services = len(components)
    operational_services = sum(1 for comp in components if comp.get('status') == 'operational')
    availability_percentage = (operational_services / total_services) * 100
    
    return availability_percentage, operational_services, total_services

def quick_status_check(quiet_mode: bool = False) -> None:
    """Quick status check with global availability percentage"""
    data = get_summary_data()
    if not data:
        print("❌ Unable to fetch status data")
        return
    
    # Get basic info
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
    
    # Full quick mode output
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
        health = "EXCELLENT"
        icon = "🏥"
    elif availability_percent >= 95:
        health = "GOOD" 
        icon = "✅"
    elif availability_percent >= 90:
        health = "FAIR"
        icon = "⚠️"
    else:
        health = "POOR"
        icon = "❌"
    
    print(f"{icon} Overall Health: {health}")
    print()

def simple_check() -> None:
    """Show main services status"""
    data = get_summary_data()
    if not data:
        print("❌ Unable to fetch status data")
        return
    
    components = data.get('components', [])
    
    # Filter main services (those without group_id)
    main_services = [comp for comp in components if comp.get('group_id') is None]
    
    # Calculate availability for main services
    availability_percent, operational, total = calculate_global_availability(main_services)
    
    print("🔍 RED HAT MAIN SERVICES")
    print("=" * 60)
    print(f"🟢 Main Services Availability: {availability_percent:.1f}% ({operational}/{total})")
    print()
    
    for service in main_services:
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        
        if status == "operational":
            print(f"✅ {name}")
        elif status == "degraded_performance":
            print(f"🟡 {name} - Performance Issues")
        elif status == "partial_outage":
            print(f"🟠 {name} - Partial Outage")
        elif status == "major_outage":
            print(f"🔴 {name} - Major Outage")
        elif status == "maintenance":
            print(f"🔧 {name} - Under Maintenance")
        else:
            print(f"❓ {name} - {status.title()}")

def full_check() -> None:
    """Show complete service hierarchy"""
    data = get_summary_data()
    if not data:
        print("❌ Unable to fetch status data")
        return
    
    components = data.get('components', [])
    
    # Calculate global availability
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
        status_icon = {
            'operational': '✅',
            'degraded_performance': '🟡', 
            'partial_outage': '🟠',
            'major_outage': '🔴',
            'maintenance': '🔧'
        }.get(status, '❓')
        
        print(f"{status_icon} {name}")
        
        # Sub-services
        if service_id in sub_services:
            for sub_service in sub_services[service_id]:
                sub_name = sub_service.get('name', 'Unnamed sub-service')
                sub_status = sub_service.get('status', 'unknown')
                
                sub_icon = {
                    'operational': '  ├─ ✅',
                    'degraded_performance': '  ├─ 🟡',
                    'partial_outage': '  ├─ 🟠', 
                    'major_outage': '  ├─ 🔴',
                    'maintenance': '  ├─ 🔧'
                }.get(sub_status, '  ├─ ❓')
                
                print(f"{sub_icon} {sub_name}")

def export_to_file() -> None:
    """Export status data to files"""
    data = get_summary_data()
    if not data:
        print("❌ Unable to fetch status data")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export JSON
    json_filename = f"redhat_status_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Exported JSON: {json_filename}")
    
    # Export summary
    components = data.get('components', [])
    availability_percent, operational, total = calculate_global_availability(components)
    
    summary_filename = f"redhat_summary_{timestamp}.txt"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write("RED HAT STATUS SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Global Availability: {availability_percent:.1f}% ({operational}/{total})\n\n")
        
        # Main services
        main_services = [comp for comp in components if comp.get('group_id') is None]
        f.write("MAIN SERVICES:\n")
        f.write("-" * 20 + "\n")
        
        for service in main_services:
            name = service.get('name', 'Unnamed')
            status = service.get('status', 'unknown')
            f.write(f"• {name}: {status.upper()}\n")
    
    print(f"📄 Exported Summary: {summary_filename}")

def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Red Hat Status Checker - Simple Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s quick                # Quick status with global availability
  %(prog)s quick --quiet        # Quiet mode with just availability
  %(prog)s simple               # Main services only  
  %(prog)s full                 # Complete service hierarchy
  %(prog)s export               # Export data to files
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['quick', 'simple', 'full', 'export'],
        default='quick',
        help='Operation mode (default: quick)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode - minimal output (works with quick mode)'
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
            quick_status_check(quiet_mode=args.quiet)
        elif args.mode == "simple":
            simple_check()
        elif args.mode == "full":
            full_check()
        elif args.mode == "export":
            export_to_file()
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
