# Requirements Document

## Introduction

This document specifies the requirements for a minimal AWS Cost Widget - a cross-platform Python desktop application that displays AWS spending information in a draggable corner widget. The widget provides month-to-date costs, budget progress visualization, and top services breakdown with simulated real-time updates, eliminating the need to log into the AWS Console for routine cost monitoring.

## Glossary

- **Widget**: A small, always-on-top desktop window that displays AWS cost information
- **Month-to-Date Cost (MTD)**: The accumulated AWS spending from the first day of the current month until the current date
- **Budget**: A user-defined spending limit for AWS services
- **Top Services**: The AWS services with the highest spending in the current billing period
- **Simulated Real-Time Updates**: Periodic refresh of cost data at configurable intervals to mimic real-time monitoring
- **Draggable Widget**: A window that can be repositioned on screen by clicking and dragging

## Requirements

### Requirement 1

**User Story:** As a developer, I want to see my month-to-date AWS spending at a glance, so that I can monitor costs without logging into the AWS Console.

#### Acceptance Criteria

1. WHEN the widget starts THEN the Widget SHALL display the current month-to-date cost in a clearly visible format
2. WHEN the month-to-date cost is displayed THEN the Widget SHALL show the cost value with currency symbol and two decimal places
3. WHEN the cost data is refreshed THEN the Widget SHALL update the displayed month-to-date cost within 2 seconds

### Requirement 2

**User Story:** As a developer, I want to see a visual progress bar showing my budget consumption, so that I can quickly understand how much of my budget I've used.

#### Acceptance Criteria

1. WHEN the widget displays budget information THEN the Widget SHALL show a horizontal progress bar representing budget consumption percentage
2. WHEN the budget consumption is below 75% THEN the Widget SHALL display the progress bar in green color
3. WHEN the budget consumption is between 75% and 90% THEN the Widget SHALL display the progress bar in yellow color
4. WHEN the budget consumption exceeds 90% THEN the Widget SHALL display the progress bar in red color
5. WHEN the budget consumption percentage changes THEN the Widget SHALL update the progress bar fill level proportionally

### Requirement 3

**User Story:** As a developer, I want to see which AWS services are costing me the most, so that I can identify optimization opportunities.

#### Acceptance Criteria

1. WHEN the widget displays top services THEN the Widget SHALL show up to 10 services with the highest spending
2. WHEN displaying each top service THEN the Widget SHALL show the service name and its associated cost
3. WHEN the top services data changes THEN the Widget SHALL update the displayed list to reflect current rankings

### Requirement 9

**User Story:** As a developer, I want accurate billing data from AWS Cost Explorer, so that I can trust the displayed cost information.

#### Acceptance Criteria

1. WHEN fetching cost data on the first day of the month THEN the Widget SHALL handle the edge case by using the previous day as the end date or showing zero costs
2. WHEN the AWS Cost Explorer returns data THEN the Widget SHALL display all services with non-zero costs up to the configured limit
3. WHEN parsing AWS Cost Explorer response THEN the Widget SHALL correctly extract and sum costs from all time periods in the response

### Requirement 10

**User Story:** As a developer, I want to see recent activity for each AWS service alongside its cost, so that I can understand what actions are driving my spending.

#### Acceptance Criteria

1. WHEN displaying a service in the top services list THEN the Widget SHALL show the recent activity count for that service from the last 24 hours
2. WHEN fetching activity data THEN the Widget SHALL use AWS CloudTrail to retrieve API event counts per service
3. WHEN a service has no recent activity THEN the Widget SHALL display "0 events" for that service
4. WHEN CloudTrail access fails THEN the Widget SHALL continue displaying cost data without activity information

### Requirement 4

**User Story:** As a developer, I want to position the widget anywhere on my screen, so that it doesn't obstruct my work.

#### Acceptance Criteria

1. WHEN a user clicks and drags the widget THEN the Widget SHALL move to follow the cursor position
2. WHEN the user releases the mouse button after dragging THEN the Widget SHALL remain at the new position
3. WHEN the widget is repositioned THEN the Widget SHALL stay within the visible screen boundaries

### Requirement 5

**User Story:** As a developer, I want the widget to update automatically, so that I always see current cost information.

#### Acceptance Criteria

1. WHEN the widget is running THEN the Widget SHALL refresh cost data at a configurable interval defaulting to 30 seconds
2. WHEN a data refresh occurs THEN the Widget SHALL update all displayed cost information simultaneously
3. WHEN the refresh interval is configured THEN the Widget SHALL accept values between 10 seconds and 300 seconds

### Requirement 6

**User Story:** As a developer, I want the widget to work on any computer with Python, so that I can use it across different machines.

#### Acceptance Criteria

1. WHEN the widget application is executed THEN the Widget SHALL run on Windows, macOS, and Linux operating systems
2. WHEN the widget is started THEN the Widget SHALL use only Python standard library and commonly available cross-platform GUI libraries
3. WHEN the widget encounters a missing dependency THEN the Widget SHALL display a clear error message indicating the required package

### Requirement 7

**User Story:** As a developer, I want to configure my AWS credentials and budget, so that the widget shows my personalized cost data.

#### Acceptance Criteria

1. WHEN the widget starts THEN the Widget SHALL read AWS credentials from environment variables or AWS credentials file
2. WHEN the widget starts THEN the Widget SHALL read budget configuration from a local configuration file
3. WHEN AWS credentials are invalid or missing THEN the Widget SHALL display an error state with guidance on credential setup
4. WHEN the budget value is not configured THEN the Widget SHALL use a default budget of $100

### Requirement 8

**User Story:** As a developer, I want to easily close or minimize the widget, so that I can remove it from view when needed.

#### Acceptance Criteria

1. WHEN a user clicks the close button THEN the Widget SHALL terminate the application gracefully
2. WHEN the widget is running THEN the Widget SHALL display a visible close button in the widget corner
