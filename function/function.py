import boto3

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')

    response = cloudwatch.put_metric_data(
        Namespace='MyApp',
        MetricData=[
            {
                'MetricName': 'CPUUsage',
                'Dimensions': [
                    {
                        'Name': 'FunctionName',
                        'Value': 'my_lambda_function'
                    },
                ],
                'Value': 70.0,
                'Unit': 'Percent'
            },
        ]
    )

    response = cloudwatch.put_metric_alarm(
        AlarmName='HighCPUUsageAlarm',
        MetricName='CPUUsage',
        Namespace='MyApp',
        Statistic='Average',
        Period=300,
        EvaluationPeriods=1,
        Threshold=75.0,
        ComparisonOperator='GreaterThanThreshold',
        AlarmActions=[
            'arn:aws:autoscaling:us-west-2:123456789012:scalingPolicy:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:autoScalingGroupName/my-asg:policyName/MyScalingPolicy'
        ]
    )

    appscaling = boto3.client('application-autoscaling')

    response = appscaling.register_scalable_target(
        ServiceNamespace='lambda',
        ResourceId='function:my_lambda_function',
        ScalableDimension='lambda:function:ProvisionedConcurrency',
        MinCapacity=1,
        MaxCapacity=10
    )

    response = appscaling.put_scaling_policy(
        PolicyName='MyScalingPolicy',
        ServiceNamespace='lambda',
        ResourceId='function:my_lambda_function',
        ScalableDimension='lambda:function:ProvisionedConcurrency',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 75.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'LambdaProvisionedConcurrencyUtilization'
            },
            'ScaleOutCooldown': 60,
            'ScaleInCooldown': 60
        }
    )
    return {
        'statusCode': 200,
        'body': 'Metrics and alarms configured successfully.'
    }