"""Configuration management for AWS Cost Widget."""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional


# Default values
DEFAULT_BUDGET = 100.0
DEFAULT_REFRESH_INTERVAL = 30
MIN_REFRESH_INTERVAL = 10
MAX_REFRESH_INTERVAL = 300


@dataclass
class WidgetConfig:
    """Configuration for the AWS Cost Widget."""
    budget: float = DEFAULT_BUDGET
    refresh_interval: int = DEFAULT_REFRESH_INTERVAL
    use_simulated_data: bool = False
    display_month: str = "current"  # "current" or "november"

    def to_dict(self) -> dict:
        """Convert config to dictionary for JSON serialization."""
        return asdict(self)


def validate_refresh_interval(interval: int) -> int:
    """
    Ensure interval is within valid range [10, 300] seconds.
    
    Args:
        interval: The refresh interval in seconds
        
    Returns:
        Clamped interval value within valid range
    """
    return max(MIN_REFRESH_INTERVAL, min(MAX_REFRESH_INTERVAL, interval))


def load_config(config_path: str = "config.json") -> WidgetConfig:
    """
    Load configuration from JSON file, falling back to defaults.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        WidgetConfig with loaded or default values
    """
    config = WidgetConfig()
    
    if not os.path.exists(config_path):
        return config
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        # Load budget with validation
        if 'budget' in data:
            try:
                budget = float(data['budget'])
                if budget > 0:
                    config.budget = budget
            except (ValueError, TypeError):
                pass  # Use default
        
        # Load refresh interval with validation
        if 'refresh_interval' in data:
            try:
                interval = int(data['refresh_interval'])
                config.refresh_interval = validate_refresh_interval(interval)
            except (ValueError, TypeError):
                pass  # Use default
        
        # Load simulated data flag
        if 'use_simulated_data' in data:
            config.use_simulated_data = bool(data['use_simulated_data'])
        
        # Load display month option
        if 'display_month' in data:
            month = str(data['display_month']).lower()
            if month in ['current', 'november']:
                config.display_month = month
            
    except (json.JSONDecodeError, IOError):
        # Return defaults on any file/parse error
        pass
    
    return config


def save_config(config: WidgetConfig, config_path: str = "config.json") -> None:
    """
    Save configuration to JSON file.
    
    Args:
        config: The configuration to save
        config_path: Path to the configuration file
    """
    with open(config_path, 'w') as f:
        json.dump(config.to_dict(), f, indent=4)
