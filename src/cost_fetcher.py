"""Cost data fetching for AWS Cost Widget."""

import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional

# AWS service names for simulation
AWS_SERVICES = [
    "Amazon EC2", "Amazon S3", "Amazon RDS", "AWS Lambda",
    "Amazon CloudFront", "Amazon DynamoDB", "Amazon ECS",
    "Amazon SQS", "Amazon SNS", "AWS Fargate", "Amazon EKS",
    "Amazon ElastiCache", "Amazon Redshift", "AWS Glue"
]


@dataclass
class CostData:
    """Container for AWS cost information."""
    month_to_date: float
    top_services: List[Tuple[str, float, int]]  # (service_name, cost, activity_count)
    last_updated: datetime


def format_currency(amount: float) -> str:
    """
    Format amount as currency string with $ symbol and 2 decimal places.
    
    Args:
        amount: The amount to format
        
    Returns:
        Formatted string like "$123.45"
    """
    return f"${amount:.2f}"


def get_top_services(services: List[Tuple[str, float]], limit: int = 10) -> List[Tuple[str, float]]:
    """
    Get top N services sorted by cost in descending order.
    
    Args:
        services: List of (service_name, cost) tuples
        limit: Maximum number of services to return
        
    Returns:
        Up to `limit` services sorted by cost descending
    """
    sorted_services = sorted(services, key=lambda x: x[1], reverse=True)
    return sorted_services[:limit]


# Mapping from Cost Explorer service names to CloudTrail event sources
SERVICE_TO_EVENT_SOURCE = {
    "Amazon EC2": "ec2.amazonaws.com",
    "Amazon S3": "s3.amazonaws.com",
    "Amazon RDS": "rds.amazonaws.com",
    "AWS Lambda": "lambda.amazonaws.com",
    "Amazon CloudFront": "cloudfront.amazonaws.com",
    "Amazon DynamoDB": "dynamodb.amazonaws.com",
    "Amazon ECS": "ecs.amazonaws.com",
    "Amazon SQS": "sqs.amazonaws.com",
    "Amazon SNS": "sns.amazonaws.com",
    "AWS Fargate": "ecs.amazonaws.com",
    "Amazon EKS": "eks.amazonaws.com",
    "Amazon ElastiCache": "elasticache.amazonaws.com",
    "Amazon Redshift": "redshift.amazonaws.com",
    "AWS Glue": "glue.amazonaws.com",
    "Amazon CloudWatch": "monitoring.amazonaws.com",
    "AWS Key Management Service": "kms.amazonaws.com",
    "Amazon Route 53": "route53.amazonaws.com",
    "Amazon API Gateway": "apigateway.amazonaws.com",
    "AWS Secrets Manager": "secretsmanager.amazonaws.com",
    "Amazon Elastic Load Balancing": "elasticloadbalancing.amazonaws.com",
}


def fetch_service_activity(service_names: List[str]) -> dict:
    """
    Fetch recent activity counts per service from CloudTrail.
    
    Args:
        service_names: List of AWS service names to look up
        
    Returns:
        Dictionary mapping service names to event counts (last 24 hours)
    """
    try:
        import boto3
        from datetime import datetime, timedelta
        
        client = boto3.client('cloudtrail')
        activity = {}
        
        # Look up events for the last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        for service_name in service_names:
            event_source = SERVICE_TO_EVENT_SOURCE.get(service_name)
            if not event_source:
                # Try to derive event source from service name
                simplified = service_name.lower().replace("amazon ", "").replace("aws ", "").replace(" ", "")
                event_source = f"{simplified}.amazonaws.com"
            
            try:
                # Use lookup_events to count events for this service
                response = client.lookup_events(
                    LookupAttributes=[
                        {
                            'AttributeKey': 'EventSource',
                            'AttributeValue': event_source
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    MaxResults=50  # Limit to avoid rate limiting
                )
                activity[service_name] = len(response.get('Events', []))
            except Exception:
                activity[service_name] = 0
        
        return activity
        
    except ImportError:
        return {name: 0 for name in service_names}
    except Exception:
        return {name: 0 for name in service_names}


def fetch_simulated_costs() -> CostData:
    """
    Generate simulated cost data for testing/demo purposes.
    Uses realistic AWS service costs based on typical usage patterns.
    
    Returns:
        CostData with realistic values
    """
    # Realistic cost distribution based on common AWS usage
    # Total MTD: $2.13 (matching typical small account usage)
    service_costs = [
        ("AWS WAF", 1.48),
        ("AWS Amplify", 0.34),
        ("AWS Cost Explorer", 0.24),
        ("Amazon EC2 Container Registry (ECR)", 0.04),
        ("Amazon Bedrock AgentCore", 0.01),
        ("Amazon S3", 0.01),
        ("Amazon CloudWatch", 0.01),
    ]
    
    # Add some randomness to make it feel live (±10%)
    randomized_costs = []
    for service, base_cost in service_costs:
        variation = random.uniform(0.9, 1.1)
        cost = round(base_cost * variation, 2)
        randomized_costs.append((service, cost))
    
    mtd = sum(cost for _, cost in randomized_costs)
    top_services = get_top_services(randomized_costs)
    
    # Add simulated activity counts (realistic for these services)
    activity_ranges = {
        "AWS WAF": (50, 200),
        "AWS Amplify": (10, 50),
        "AWS Cost Explorer": (5, 20),
        "Amazon EC2 Container Registry (ECR)": (20, 80),
        "Amazon Bedrock AgentCore": (5, 30),
        "Amazon S3": (100, 500),
        "Amazon CloudWatch": (200, 800),
    }
    
    top_services_with_activity = [
        (name, cost, random.randint(*activity_ranges.get(name, (0, 50))))
        for name, cost in top_services
    ]
    
    return CostData(
        month_to_date=round(mtd, 2),
        top_services=top_services_with_activity,
        last_updated=datetime.now()
    )


def fetch_cloudwatch_billing_metrics() -> CostData:
    """
    Fetch real-time cost data from AWS CloudWatch Billing Metrics.
    This is more up-to-date than Cost Explorer (updates every 4 hours vs 24-48 hours).
    
    Note: Billing metrics are only available in us-east-1 region.
    
    Returns:
        CostData with actual AWS spending information
        
    Raises:
        Exception: If AWS credentials are missing or invalid
    """
    try:
        import boto3
        from datetime import datetime, timedelta
        
        # CloudWatch billing metrics are ONLY available in us-east-1
        cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        
        # Get the last 24 hours of data
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        print("Fetching billing data from CloudWatch (us-east-1)...")
        
        # Get total estimated charges
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {'Name': 'Currency', 'Value': 'USD'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour intervals
            Statistics=['Maximum']
        )
        
        # Get the most recent total cost
        total_cost = 0.0
        if response['Datapoints']:
            # Sort by timestamp and get the latest
            sorted_points = sorted(response['Datapoints'], key=lambda x: x['Timestamp'], reverse=True)
            total_cost = sorted_points[0]['Maximum']
            print(f"Total estimated charges: ${total_cost:.2f}")
        
        # Get per-service costs
        # First, list all available services
        service_costs = []
        
        # Common AWS services to check
        services_to_check = [
            'AmazonEC2', 'AmazonS3', 'AmazonRDS', 'AWSLambda',
            'AmazonCloudFront', 'AmazonDynamoDB', 'AmazonECS',
            'AmazonSQS', 'AmazonSNS', 'AWSDataTransfer',
            'AmazonCloudWatch', 'AWSWAF', 'AWSAmplify',
            'AWSCostExplorer', 'AmazonECR', 'AmazonBedrock',
            'AWSSecretsManager', 'AWSKeyManagementService',
            'AmazonAPIGateway', 'AmazonCognito', 'AmazonTextract',
            'AmazonRekognition', 'AmazonComprehend', 'AWSGlue'
        ]
        
        print(f"Checking {len(services_to_check)} services...")
        
        for service in services_to_check:
            try:
                response = cloudwatch.get_metric_statistics(
                    Namespace='AWS/Billing',
                    MetricName='EstimatedCharges',
                    Dimensions=[
                        {'Name': 'Currency', 'Value': 'USD'},
                        {'Name': 'ServiceName', 'Value': service}
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Maximum']
                )
                
                if response['Datapoints']:
                    sorted_points = sorted(response['Datapoints'], key=lambda x: x['Timestamp'], reverse=True)
                    cost = sorted_points[0]['Maximum']
                    if cost > 0.001:
                        # Convert service name to readable format
                        readable_name = service.replace('Amazon', 'Amazon ').replace('AWS', 'AWS ')
                        service_costs.append((readable_name, round(cost, 2)))
                        print(f"  {readable_name}: ${cost:.2f}")
            except Exception as e:
                # Service might not have data, skip it
                pass
        
        # If we didn't get service breakdown but have total, use Cost Explorer as fallback for services
        if not service_costs and total_cost > 0:
            print("No service breakdown from CloudWatch, falling back to Cost Explorer for services...")
            service_costs = fetch_cost_explorer_services()
        
        top_services = get_top_services(service_costs)
        
        # Fetch activity data from CloudTrail
        service_names = [name for name, _ in top_services]
        activity_data = fetch_service_activity(service_names)
        
        # Combine cost and activity data
        top_services_with_activity = [
            (name, cost, activity_data.get(name, 0))
            for name, cost in top_services
        ]
        
        return CostData(
            month_to_date=round(total_cost, 2),
            top_services=top_services_with_activity,
            last_updated=datetime.now()
        )
        
    except ImportError:
        raise Exception("boto3 is required for AWS integration. Install with: pip install boto3")
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower() or "NoCredentialsError" in error_msg:
            raise Exception(
                "AWS credentials not found. Please configure credentials:\n"
                "1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, or\n"
                "2. Configure ~/.aws/credentials file, or\n"
                "3. Use AWS IAM role if running on EC2"
            )
        raise


def fetch_cost_explorer_services(start_date: str = None, end_date: str = None) -> List[Tuple[str, float]]:
    """
    Fallback function to get service breakdown from Cost Explorer.
    Used when CloudWatch doesn't provide service-level details.
    
    Args:
        start_date: Start date in YYYY-MM-DD format (defaults to current month)
        end_date: End date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        List of (service_name, cost) tuples
    """
    try:
        import boto3
        from datetime import date, timedelta
        
        client = boto3.client('ce')
        
        if not start_date or not end_date:
            today = date.today()
            start_date = today.replace(day=1).isoformat()
            end_date = today.isoformat()
        
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        service_cost_map = {}
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                service_name = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                if service_name not in service_cost_map:
                    service_cost_map[service_name] = 0.0
                service_cost_map[service_name] += cost
        
        service_costs = []
        for service_name, cost in service_cost_map.items():
            if cost > 0.001:
                service_costs.append((service_name, round(cost, 2)))
        
        return service_costs
    except Exception:
        return []


def fetch_november_costs() -> CostData:
    """
    Fetch November 2025 cost data from AWS Cost Explorer.
    This is useful when current month has no data yet.
    
    Returns:
        CostData with November 2025 spending information
        
    Raises:
        Exception: If AWS credentials are missing or invalid
    """
    try:
        import boto3
        from datetime import date
        
        client = boto3.client('ce')
        
        # November 2025 date range
        start_date = '2025-11-01'
        end_date = '2025-12-01'
        
        print(f"Fetching November 2025 costs...")
        
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        # Parse response - aggregate costs across all days
        service_cost_map = {}
        total_cost = 0.0
        
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                service_name = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                
                if service_name not in service_cost_map:
                    service_cost_map[service_name] = 0.0
                service_cost_map[service_name] += cost
        
        # Convert to list and filter out zero costs
        service_costs = []
        for service_name, cost in service_cost_map.items():
            if cost > 0.001:
                service_costs.append((service_name, round(cost, 2)))
                total_cost += cost
        
        print(f"November 2025 total: ${total_cost:.2f}")
        print(f"Services with charges: {len(service_costs)}")
        
        top_services = get_top_services(service_costs)
        
        # Fetch activity data from CloudTrail (will be 0 for historical data)
        service_names = [name for name, _ in top_services]
        activity_data = {name: 0 for name in service_names}  # Historical data has no activity
        
        # Combine cost and activity data
        top_services_with_activity = [
            (name, cost, activity_data.get(name, 0))
            for name, cost in top_services
        ]
        
        return CostData(
            month_to_date=round(total_cost, 2),
            top_services=top_services_with_activity,
            last_updated=datetime.now()
        )
        
    except ImportError:
        raise Exception("boto3 is required for AWS integration. Install with: pip install boto3")
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower() or "NoCredentialsError" in error_msg:
            raise Exception(
                "AWS credentials not found. Please configure credentials:\n"
                "1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, or\n"
                "2. Configure ~/.aws/credentials file, or\n"
                "3. Use AWS IAM role if running on EC2"
            )
        raise


def fetch_aws_costs_before_credits() -> CostData:
    """
    Fetch AWS usage costs BEFORE credits are applied.
    This shows actual usage even if you have AWS credits.
    
    Returns:
        CostData with actual AWS usage costs (before credits)
        
    Raises:
        Exception: If AWS credentials are missing or invalid
    """
    try:
        import boto3
        from datetime import date
        
        client = boto3.client('ce')
        today = date.today()
        start_date = today.replace(day=1).isoformat()
        end_date = today.isoformat()
        
        print("Fetching AWS costs (before credits)...")
        
        # Get costs by RECORD_TYPE to separate usage from credits
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'RECORD_TYPE'}]
        )
        
        # Extract usage costs (before credits)
        usage_cost = 0.0
        credit_amount = 0.0
        
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                record_type = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                
                if record_type == 'Usage':
                    usage_cost += cost
                elif record_type == 'Credit':
                    credit_amount += cost
        
        print(f"Usage cost: ${usage_cost:.2f}")
        print(f"Credits applied: ${credit_amount:.2f}")
        print(f"Net cost: ${usage_cost + credit_amount:.2f}")
        
        # Now get service breakdown for the usage
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'RECORD_TYPE'}
            ]
        )
        
        service_cost_map = {}
        
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                keys = group['Keys']
                if len(keys) >= 2:
                    service_name = keys[0]
                    record_type = keys[1]
                    cost = float(group['Metrics']['UnblendedCost']['Amount'])
                    
                    # Only count usage, not credits
                    if record_type == 'Usage' and cost > 0:
                        if service_name not in service_cost_map:
                            service_cost_map[service_name] = 0.0
                        service_cost_map[service_name] += cost
        
        service_costs = []
        for service_name, cost in service_cost_map.items():
            if cost > 0.001:
                service_costs.append((service_name, round(cost, 2)))
        
        print(f"Found {len(service_costs)} services with usage")
        
        top_services = get_top_services(service_costs)
        
        # Fetch activity data
        service_names = [name for name, _ in top_services]
        activity_data = fetch_service_activity(service_names)
        
        top_services_with_activity = [
            (name, cost, activity_data.get(name, 0))
            for name, cost in top_services
        ]
        
        return CostData(
            month_to_date=round(usage_cost, 2),
            top_services=top_services_with_activity,
            last_updated=datetime.now()
        )
        
    except ImportError:
        raise Exception("boto3 is required for AWS integration. Install with: pip install boto3")
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower() or "NoCredentialsError" in error_msg:
            raise Exception(
                "AWS credentials not found. Please configure credentials:\n"
                "1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, or\n"
                "2. Configure ~/.aws/credentials file, or\n"
                "3. Use AWS IAM role if running on EC2"
            )
        raise


def fetch_aws_costs() -> CostData:
    """
    Fetch real cost data from AWS.
    Automatically detects if credits are applied and shows usage before credits.
    
    Returns:
        CostData with actual AWS spending information
        
    Raises:
        Exception: If AWS credentials are missing or invalid
    """
    try:
        # Fetch costs before credits (shows actual usage)
        return fetch_aws_costs_before_credits()
    except Exception as e:
        print(f"Error fetching AWS costs: {e}")
        raise
