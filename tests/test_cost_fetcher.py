"""Tests for cost data fetching."""

import pytest
from hypothesis import given, strategies as st, settings
from cost_fetcher import (
    CostData, format_currency, get_top_services, fetch_simulated_costs
)
from datetime import datetime


class TestFormatCurrency:
    """Tests for format_currency function."""
    
    def test_basic_formatting(self):
        """Basic amounts should format correctly."""
        assert format_currency(100.0) == "$100.00"
        assert format_currency(0.0) == "$0.00"
        assert format_currency(1234.56) == "$1234.56"
    
    def test_rounding(self):
        """Amounts should round to 2 decimal places."""
        assert format_currency(10.999) == "$11.00"
        assert format_currency(10.001) == "$10.00"
        assert format_currency(10.556) == "$10.56"
    
    def test_small_amounts(self):
        """Small amounts should display correctly."""
        assert format_currency(0.01) == "$0.01"
        assert format_currency(0.99) == "$0.99"


class TestGetTopServices:
    """Tests for get_top_services function."""
    
    def test_returns_top_10_by_default(self):
        """Should return top 10 services by cost."""
        services = [
            ("Service A", 10.0),
            ("Service B", 50.0),
            ("Service C", 30.0),
            ("Service D", 20.0),
            ("Service E", 40.0),
            ("Service F", 5.0),
            ("Service G", 15.0),
            ("Service H", 25.0),
            ("Service I", 35.0),
            ("Service J", 45.0),
            ("Service K", 3.0),
        ]
        result = get_top_services(services)
        assert len(result) == 10
        assert result[0] == ("Service B", 50.0)
        assert result[1] == ("Service J", 45.0)
    
    def test_fewer_than_limit(self):
        """Should return all services if fewer than limit."""
        services = [("Service A", 10.0), ("Service B", 20.0)]
        result = get_top_services(services)
        assert len(result) == 2
    
    def test_empty_list(self):
        """Should handle empty list."""
        result = get_top_services([])
        assert result == []
    
    def test_custom_limit(self):
        """Should respect custom limit."""
        services = [
            ("A", 10.0), ("B", 20.0), ("C", 30.0), ("D", 40.0)
        ]
        result = get_top_services(services, limit=2)
        assert len(result) == 2
        assert result[0] == ("D", 40.0)


class TestFetchSimulatedCosts:
    """Tests for fetch_simulated_costs function."""
    
    def test_returns_cost_data(self):
        """Should return valid CostData object."""
        data = fetch_simulated_costs()
        assert isinstance(data, CostData)
        assert isinstance(data.month_to_date, float)
        assert isinstance(data.top_services, list)
        assert isinstance(data.last_updated, datetime)
    
    def test_mtd_in_range(self):
        """MTD cost should be in reasonable range."""
        data = fetch_simulated_costs()
        assert 10.0 <= data.month_to_date <= 500.0
    
    def test_top_services_limit(self):
        """Should return at most 10 top services."""
        data = fetch_simulated_costs()
        assert len(data.top_services) <= 10
    
    def test_services_have_names_costs_and_activity(self):
        """Each service should have name, cost, and activity count."""
        data = fetch_simulated_costs()
        for service_data in data.top_services:
            assert len(service_data) == 3, "Expected (name, cost, activity) tuple"
            service_name, cost, activity = service_data
            assert isinstance(service_name, str)
            assert len(service_name) > 0
            assert isinstance(cost, float)
            assert isinstance(activity, int)
            assert activity >= 0


# Property-Based Tests

class TestCurrencyFormattingProperty:
    """
    **Feature: aws-cost-widget, Property 1: Currency formatting consistency**
    **Validates: Requirements 1.2**
    
    For any non-negative float value, the format_currency function SHALL produce
    a string that starts with "$" and contains exactly two decimal places.
    """
    
    @settings(max_examples=100)
    @given(st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False))
    def test_currency_format_starts_with_dollar(self, amount):
        """Currency format should always start with $ symbol."""
        result = format_currency(amount)
        assert result.startswith("$"), f"Expected '$' prefix, got: {result}"
    
    @settings(max_examples=100)
    @given(st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False))
    def test_currency_format_has_two_decimals(self, amount):
        """Currency format should always have exactly two decimal places."""
        result = format_currency(amount)
        # Remove $ and check decimal places
        numeric_part = result[1:]
        assert "." in numeric_part, f"Expected decimal point, got: {result}"
        decimal_places = len(numeric_part.split(".")[1])
        assert decimal_places == 2, f"Expected 2 decimal places, got {decimal_places} in: {result}"


class TestTopServicesProperty:
    """
    **Feature: aws-cost-widget, Property 3: Top services list constraint**
    **Validates: Requirements 3.1, 3.2**
    
    For any list of services with costs, the get_top_services function SHALL return
    at most 10 services, sorted by cost in descending order, where each entry
    contains both service name and cost.
    """
    
    @settings(max_examples=100)
    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50),
            st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False)
        ),
        min_size=0,
        max_size=20
    ))
    def test_top_services_returns_at_most_10(self, services):
        """Should return at most 10 services."""
        result = get_top_services(services)
        assert len(result) <= 10, f"Expected at most 10 services, got {len(result)}"
    
    @settings(max_examples=100)
    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50),
            st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False)
        ),
        min_size=0,
        max_size=20
    ))
    def test_top_services_sorted_descending(self, services):
        """Services should be sorted by cost in descending order."""
        result = get_top_services(services)
        if len(result) > 1:
            costs = [cost for _, cost in result]
            for i in range(len(costs) - 1):
                assert costs[i] >= costs[i + 1], f"Services not sorted descending: {costs}"
    
    @settings(max_examples=100)
    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=50),
            st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False)
        ),
        min_size=0,
        max_size=20
    ))
    def test_top_services_contain_name_and_cost(self, services):
        """Each entry should contain service name (str) and cost (float)."""
        result = get_top_services(services)
        for entry in result:
            assert isinstance(entry, tuple), f"Expected tuple, got {type(entry)}"
            assert len(entry) == 2, f"Expected 2 elements, got {len(entry)}"
            name, cost = entry
            assert isinstance(name, str), f"Expected str name, got {type(name)}"
            assert isinstance(cost, float), f"Expected float cost, got {type(cost)}"
