#!/usr/bin/env python3
"""
AWS Cost Widget - Desktop application for monitoring AWS spending.

A minimal, cross-platform widget that displays:
- Month-to-date AWS costs
- Budget progress with color-coded thresholds
- Top 5 spending services

Run with: python main.py
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config
from cost_fetcher import fetch_simulated_costs, fetch_aws_costs, fetch_november_costs
from widget import AWSCostWidget
from scheduler import UpdateScheduler


def show_error_dialog(title: str, message: str) -> None:
    """Show an error dialog using tkinter."""
    import tkinter as tk
    from tkinter import messagebox      
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    messagebox.showerror(title, message)
    root.destroy()


def main() -> None:
    """Initialize and run the AWS Cost Widget application."""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if not os.path.exists(config_path):
        config_path = 'config.json'
    
    config = load_config(config_path)
    
    # Select data fetcher based on configuration
    if config.use_simulated_data:
        fetcher = fetch_simulated_costs
        print("Using simulated cost data")
        print("To use real AWS data:")
        print("  1. Enable CloudWatch billing alerts (see CLOUDWATCH_SETUP.md)")
        print("  2. Wait 24 hours for data to populate")
        print("  3. Set 'use_simulated_data': false in config.json")
    else:
        # Check if user wants to display November data
        if config.display_month == "november":
            print("Displaying November 2025 cost data...")
            try:
                test_data = fetch_november_costs()
                if test_data.month_to_date > 0:
                    fetcher = fetch_november_costs
                    print(f"✅ November 2025 Total: ${test_data.month_to_date:.2f}")
                else:
                    print("⚠️  No charges in November 2025")
                    print("Using simulated data instead...")
                    fetcher = fetch_simulated_costs
            except Exception as e:
                print(f"Error fetching November data: {e}")
                fetcher = fetch_simulated_costs
        else:
            # Test AWS credentials before starting
            try:
                print("Attempting to fetch real AWS cost data...")
                test_data = fetch_aws_costs()
                
                if test_data.month_to_date == 0:
                    print("\n⚠️  Warning: Current month showing $0.00")
                    print("This usually means:")
                    print("  - Cost Explorer has 24-48 hour delay")
                    print("  - No charges yet this month")
                    print("\nTip: Set 'display_month': 'november' in config.json to see last month's data")
                    print("\nUsing simulated data instead...")
                    fetcher = fetch_simulated_costs
                else:
                    fetcher = fetch_aws_costs
                    print(f"✅ Connected to AWS - Current MTD: ${test_data.month_to_date:.2f}")
            except Exception as e:
                error_msg = str(e)
                print(f"AWS Error: {error_msg}")
                
                # Show error and offer to use simulated data
                show_error_dialog(
                    "AWS Credentials Error",
                    f"{error_msg}\n\n"
                    "The widget will use simulated data instead.\n"
                    "To use real AWS data, see CLOUDWATCH_SETUP.md"
                )
                fetcher = fetch_simulated_costs
    
    # Create and configure widget
    try:
        widget = AWSCostWidget(config)
    except Exception as e:
        show_error_dialog("Widget Error", f"Failed to create widget: {e}")
        sys.exit(1)
    
    # Create scheduler and start updates
    scheduler = UpdateScheduler(widget, fetcher, config.refresh_interval)
    scheduler.start()
    
    print(f"AWS Cost Widget started (refresh every {config.refresh_interval}s)")
    print("Drag to move, click X to close")
    
    # Run the widget
    try:
        widget.run()
    except KeyboardInterrupt:
        print("\nShutting down...")



if __name__ == "__main__":
    main()
