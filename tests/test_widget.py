"""Tests for widget UI logic."""

import pytest
from hypothesis import given, strategies as st, settings
from widget import get_budget_color, clamp_position, COLOR_GREEN, COLOR_YELLOW, COLOR_RED


class TestGetBudgetColor:
    """Tests for get_budget_color function."""
    
    def test_green_below_75(self):
        """Should return green for percentages below 75."""
        assert get_budget_color(0) == COLOR_GREEN
        assert get_budget_color(50) == COLOR_GREEN
        assert get_budget_color(74) == COLOR_GREEN
        assert get_budget_color(74.9) == COLOR_GREEN
    
    def test_yellow_between_75_and_90(self):
        """Should return yellow for percentages 75-90."""
        assert get_budget_color(75) == COLOR_YELLOW
        assert get_budget_color(80) == COLOR_YELLOW
        assert get_budget_color(90) == COLOR_YELLOW
    
    def test_red_above_90(self):
        """Should return red for percentages above 90."""
        assert get_budget_color(91) == COLOR_RED
        assert get_budget_color(100) == COLOR_RED
        assert get_budget_color(150) == COLOR_RED


class TestBudgetColorProperty:
    """Property-based tests for budget color thresholds.
    
    **Feature: aws-cost-widget, Property 2: Budget color threshold correctness**
    """
    
    @given(st.floats(min_value=0, max_value=74.999, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100)
    def test_green_for_below_75_percent(self, percentage: float):
        """
        **Feature: aws-cost-widget, Property 2: Budget color threshold correctness**
        **Validates: Requirements 2.2, 2.3, 2.4**
        
        For any percentage value below 75, get_budget_color SHALL return green.
        """
        result = get_budget_color(percentage)
        assert result == COLOR_GREEN, (
            f"Expected green for {percentage}%, got {result}"
        )
    
    @given(st.floats(min_value=75, max_value=90, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100)
    def test_yellow_for_75_to_90_percent(self, percentage: float):
        """
        **Feature: aws-cost-widget, Property 2: Budget color threshold correctness**
        **Validates: Requirements 2.2, 2.3, 2.4**
        
        For any percentage value between 75 and 90 (inclusive), 
        get_budget_color SHALL return yellow.
        """
        result = get_budget_color(percentage)
        assert result == COLOR_YELLOW, (
            f"Expected yellow for {percentage}%, got {result}"
        )
    
    @given(st.floats(min_value=90.001, max_value=500, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100)
    def test_red_for_above_90_percent(self, percentage: float):
        """
        **Feature: aws-cost-widget, Property 2: Budget color threshold correctness**
        **Validates: Requirements 2.2, 2.3, 2.4**
        
        For any percentage value above 90, get_budget_color SHALL return red.
        """
        result = get_budget_color(percentage)
        assert result == COLOR_RED, (
            f"Expected red for {percentage}%, got {result}"
        )


class TestClampPosition:
    """Tests for clamp_position function."""
    
    def test_position_within_bounds(self):
        """Position within bounds should be unchanged."""
        x, y = clamp_position(100, 100, 200, 200, 1920, 1080)
        assert x == 100
        assert y == 100
    
    def test_negative_x_clamped(self):
        """Negative X should be clamped to 0."""
        x, y = clamp_position(-50, 100, 200, 200, 1920, 1080)
        assert x == 0
        assert y == 100
    
    def test_negative_y_clamped(self):
        """Negative Y should be clamped to 0."""
        x, y = clamp_position(100, -50, 200, 200, 1920, 1080)
        assert x == 100
        assert y == 0
    
    def test_x_exceeds_screen_clamped(self):
        """X exceeding screen width should be clamped."""
        x, y = clamp_position(1800, 100, 200, 200, 1920, 1080)
        assert x == 1720  # 1920 - 200
        assert y == 100
    
    def test_y_exceeds_screen_clamped(self):
        """Y exceeding screen height should be clamped."""
        x, y = clamp_position(100, 1000, 200, 200, 1920, 1080)
        assert x == 100
        assert y == 880  # 1080 - 200
    
    def test_corner_case_exact_fit(self):
        """Widget at exact bottom-right corner."""
        x, y = clamp_position(1720, 880, 200, 200, 1920, 1080)
        assert x == 1720
        assert y == 880


class TestPositionBoundaryClampingProperty:
    """Property-based tests for widget position boundary clamping.
    
    **Feature: aws-cost-widget, Property 4: Widget position boundary clamping**
    """
    
    @given(
        x=st.integers(min_value=-10000, max_value=10000),
        y=st.integers(min_value=-10000, max_value=10000),
        widget_width=st.integers(min_value=1, max_value=1000),
        widget_height=st.integers(min_value=1, max_value=1000),
        screen_width=st.integers(min_value=100, max_value=10000),
        screen_height=st.integers(min_value=100, max_value=10000)
    )
    @settings(max_examples=100)
    def test_clamped_position_within_screen_bounds(
        self, x: int, y: int, widget_width: int, widget_height: int,
        screen_width: int, screen_height: int
    ):
        """
        **Feature: aws-cost-widget, Property 4: Widget position boundary clamping**
        **Validates: Requirements 4.3**
        
        For any target position (x, y) and screen dimensions, the clamped position
        SHALL remain within visible screen boundaries:
        - 0 <= clamped_x <= screen_width - widget_width
        - 0 <= clamped_y <= screen_height - widget_height
        """
        # Only test when widget can fit on screen
        if widget_width > screen_width or widget_height > screen_height:
            return
        
        clamped_x, clamped_y = clamp_position(
            x, y, widget_width, widget_height, screen_width, screen_height
        )
        
        # Verify X boundary
        assert clamped_x >= 0, (
            f"Clamped X ({clamped_x}) should be >= 0"
        )
        assert clamped_x <= screen_width - widget_width, (
            f"Clamped X ({clamped_x}) should be <= {screen_width - widget_width}"
        )
        
        # Verify Y boundary
        assert clamped_y >= 0, (
            f"Clamped Y ({clamped_y}) should be >= 0"
        )
        assert clamped_y <= screen_height - widget_height, (
            f"Clamped Y ({clamped_y}) should be <= {screen_height - widget_height}"
        )
