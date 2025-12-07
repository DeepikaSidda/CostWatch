# Implementation Plan

- [x] 1. Set up project structure and dependencies

  - Create directory structure: `src/`, `tests/`
  - Create `requirements.txt` with dependencies (boto3, hypothesis, pytest)
  - Create `config.json` template file
  - _Requirements: 6.2, 7.2_

- [x] 2. Implement configuration management

  - [x] 2.1 Create WidgetConfig dataclass and load_config function
    - Implement `src/config.py` with WidgetConfig dataclass
    - Implement load_config() to read from JSON file with defaults
    - Implement validate_refresh_interval() to clamp values to [10, 300]
    - _Requirements: 5.3, 7.2, 7.4_
  - [x] 2.2 Write property test for refresh interval validation
    - **Property 5: Refresh interval validation**
    - **Validates: Requirements 5.3**
  - [x] 2.3 Write property test for configuration round-trip
    - **Property 6: Configuration loading round-trip**
    - **Validates: Requirements 7.2**

- [x] 3. Implement cost data fetching

  - [x] 3.1 Create CostData dataclass and format_currency function
    - Implement `src/cost_fetcher.py` with CostData dataclass
    - Implement format_currency() for $ symbol and 2 decimal places
    - _Requirements: 1.2_
  - [x] 3.2 Write property test for currency formatting
    - **Property 1: Currency formatting consistency**
    - **Validates: Requirements 1.2**
  - [x] 3.3 Implement fetch_simulated_costs function
    - Generate realistic mock cost data for testing
    - Include random top services with varying costs
    - _Requirements: 1.1, 3.1_
  - [x] 3.4 Implement fetch_aws_costs function
    - Use boto3 Cost Explorer API to get month-to-date costs
    - Parse response to extract top 5 services by cost
    - Handle API errors gracefully
    - _Requirements: 1.1, 3.1, 7.1_
  - [x] 3.5 Write property test for top services list constraint
    - **Property 3: Top services list constraint**
    - **Validates: Requirements 3.1, 3.2**

- [x] 4. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement widget UI core

  - [x] 5.1 Create AWSCostWidget class with tkinter window setup
    - Implement `src/widget.py` with basic window configuration
    - Set window to always-on-top, frameless, compact size
    - Add close button in corner
    - _Requirements: 8.1, 8.2_
  - [x] 5.2 Implement get_budget_color function
    - Return green for <75%, yellow for 75-90%, red for >90%
    - _Requirements: 2.2, 2.3, 2.4_
  - [x] 5.3 Write property test for budget color thresholds
    - **Property 2: Budget color threshold correctness**
    - **Validates: Requirements 2.2, 2.3, 2.4**
  - [x] 5.4 Implement cost display components
    - Add month-to-date cost label with currency formatting
    - Add budget progress bar with color coding
    - Add top services list display
    - _Requirements: 1.1, 2.1, 2.5, 3.1, 3.2_
  - [x] 5.5 Implement update_display method
    - Update all UI elements with new CostData
    - Recalculate budget percentage and update progress bar
    - _Requirements: 1.3, 3.3_

- [x] 6. Implement drag functionality

  - [x] 6.1 Implement start_drag and do_drag methods
    - Track initial click position for drag offset
    - Move window to follow cursor during drag
    - _Requirements: 4.1, 4.2_
  - [x] 6.2 Implement position boundary clamping
    - Clamp widget position to stay within screen bounds
    - _Requirements: 4.3_
  - [x] 6.3 Write property test for position boundary clamping
    - **Property 4: Widget position boundary clamping**
    - **Validates: Requirements 4.3**

- [x] 7. Implement update scheduler

  - [x] 7.1 Create UpdateScheduler class
    - Implement `src/scheduler.py` with scheduling logic
    - Use tkinter's after() method for periodic updates
    - _Requirements: 5.1, 5.2_

- [x] 8. Implement main entry point

  - [x] 8.1 Create main.py with application bootstrap
    - Load configuration
    - Initialize cost fetcher (simulated or real based on config)
    - Create widget and scheduler
    - Handle credential errors with user guidance
    - Start main loop
    - _Requirements: 6.1, 7.1, 7.3_

- [x] 9. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
