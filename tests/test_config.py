"""Tests for configuration management."""

import json
import os
import tempfile
import pytest
from hypothesis import given, strategies as st, settings
from config import (
    WidgetConfig, load_config, save_config, 
    validate_refresh_interval, DEFAULT_BUDGET, DEFAULT_REFRESH_INTERVAL,
    MIN_REFRESH_INTERVAL, MAX_REFRESH_INTERVAL
)


class TestValidateRefreshInterval:
    """Tests for validate_refresh_interval function."""
    
    def test_valid_interval_unchanged(self):
        """Valid intervals within range should be unchanged."""
        assert validate_refresh_interval(30) == 30
        assert validate_refresh_interval(10) == 10
        assert validate_refresh_interval(300) == 300
        assert validate_refresh_interval(150) == 150
    
    def test_below_minimum_clamped(self):
        """Intervals below 10 should be clamped to 10."""
        assert validate_refresh_interval(5) == 10
        assert validate_refresh_interval(0) == 10
        assert validate_refresh_interval(-100) == 10
    
    def test_above_maximum_clamped(self):
        """Intervals above 300 should be clamped to 300."""
        assert validate_refresh_interval(500) == 300
        assert validate_refresh_interval(1000) == 300


class TestRefreshIntervalProperty:
    """Property-based tests for refresh interval validation.
    
    **Feature: aws-cost-widget, Property 5: Refresh interval validation**
    """
    
    @given(st.integers())
    @settings(max_examples=100)
    def test_refresh_interval_always_within_bounds(self, interval: int):
        """
        **Feature: aws-cost-widget, Property 5: Refresh interval validation**
        **Validates: Requirements 5.3**
        
        For any input interval value, the validate_refresh_interval function
        SHALL return a value within the range [10, 300] seconds.
        """
        result = validate_refresh_interval(interval)
        assert MIN_REFRESH_INTERVAL <= result <= MAX_REFRESH_INTERVAL, (
            f"Result {result} is outside valid range [{MIN_REFRESH_INTERVAL}, {MAX_REFRESH_INTERVAL}]"
        )


class TestWidgetConfig:
    """Tests for WidgetConfig dataclass."""
    
    def test_default_values(self):
        """Config should have correct defaults."""
        config = WidgetConfig()
        assert config.budget == DEFAULT_BUDGET
        assert config.refresh_interval == DEFAULT_REFRESH_INTERVAL
        assert config.use_simulated_data is False
    
    def test_to_dict(self):
        """Config should serialize to dict correctly."""
        config = WidgetConfig(budget=200.0, refresh_interval=60, use_simulated_data=True)
        d = config.to_dict()
        assert d['budget'] == 200.0
        assert d['refresh_interval'] == 60
        assert d['use_simulated_data'] is True


class TestConfigRoundTripProperty:
    """Property-based tests for configuration round-trip.
    
    **Feature: aws-cost-widget, Property 6: Configuration loading round-trip**
    """
    
    @given(
        budget=st.floats(min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False),
        refresh_interval=st.integers(min_value=MIN_REFRESH_INTERVAL, max_value=MAX_REFRESH_INTERVAL),
        use_simulated_data=st.booleans()
    )
    @settings(max_examples=100)
    def test_config_round_trip(self, budget: float, refresh_interval: int, use_simulated_data: bool):
        """
        **Feature: aws-cost-widget, Property 6: Configuration loading round-trip**
        **Validates: Requirements 7.2**
        
        For any valid WidgetConfig object, serializing to JSON and then loading
        SHALL produce an equivalent WidgetConfig object.
        """
        # Create original config
        original = WidgetConfig(
            budget=budget,
            refresh_interval=refresh_interval,
            use_simulated_data=use_simulated_data
        )
        
        # Round-trip through JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            save_config(original, temp_path)
            loaded = load_config(temp_path)
            
            # Verify equivalence (using approximate comparison for floats)
            assert abs(loaded.budget - original.budget) < 0.01, (
                f"Budget mismatch: {loaded.budget} != {original.budget}"
            )
            assert loaded.refresh_interval == original.refresh_interval, (
                f"Refresh interval mismatch: {loaded.refresh_interval} != {original.refresh_interval}"
            )
            assert loaded.use_simulated_data == original.use_simulated_data, (
                f"use_simulated_data mismatch: {loaded.use_simulated_data} != {original.use_simulated_data}"
            )
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestLoadConfig:
    """Tests for load_config function."""
    
    def test_missing_file_returns_defaults(self):
        """Missing config file should return defaults."""
        config = load_config("/nonexistent/path/config.json")
        assert config.budget == DEFAULT_BUDGET
        assert config.refresh_interval == DEFAULT_REFRESH_INTERVAL
    
    def test_valid_config_loaded(self):
        """Valid config file should be loaded correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                'budget': 250.0,
                'refresh_interval': 45,
                'use_simulated_data': True
            }, f)
            f.flush()
            
            config = load_config(f.name)
            assert config.budget == 250.0
            assert config.refresh_interval == 45
            assert config.use_simulated_data is True
            
            os.unlink(f.name)
    
    def test_invalid_interval_clamped(self):
        """Invalid refresh interval should be clamped."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({'refresh_interval': 5}, f)
            f.flush()
            
            config = load_config(f.name)
            assert config.refresh_interval == 10
            
            os.unlink(f.name)
    
    def test_invalid_json_returns_defaults(self):
        """Invalid JSON should return defaults."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("not valid json {{{")
            f.flush()
            
            config = load_config(f.name)
            assert config.budget == DEFAULT_BUDGET
            
            os.unlink(f.name)
