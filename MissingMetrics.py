import json
import boto3

def lambda_handler(event, context):
    # TODO implement

    # Initialize AWS clients
    CloudwatchClient = boto3.client('cloudwatch')
    ec2 = boto3.client('ec2')
    
    # Initialize set of expected metrics from AWS
    AWS_metrics = {
        "CPUUtilization", 'Memory % Committed Bytes In Use', 'LogicalDisk Free Megabytes'
    }
    
    # Initialize set of disk metrics being sent
    disks = {"C:", "D:"}
    
    # Describe instances to get the most recent version
    def getInstanceType(instanceId):
        response = ec2.describe_instances(
            InstanceIds=[instanceId]
        )
        return response["Reservations"][0]["Instances"][0]["InstanceType"]
            
    # Get instance details
    instanceId = event['instanceId']
    instanceName = event['instanceName']
    instanceType = getInstanceType(instanceId)

    # Find metrics for the given instance
    dimensions = [{'Name': 'InstanceId', 'Value': instanceId}]
    currmetrics = set()  # Stores the metrics it could find
    driveletters = set()
    response = CloudwatchClient.list_metrics(Dimensions=dimensions)['Metrics']
    
    for metric in response:
        if metric["Namespace"] == "CWAgent":  # If it's a CWAgent metric
            for dimension in metric["Dimensions"]:  # Look through the dimensions to find the Instance Type
                if dimension['Name'] == "InstanceType" and dimension["Value"] == instanceType:
                    # Only add to currmetrics if it has the same instanceType as the instance
                    currmetrics.add(metric["MetricName"])
                    if metric["Dimensions"][0]["Value"] in disks and metric["MetricName"] == 'LogicalDisk Free Megabytes':
                        driveletters.add(metric["Dimensions"][0]["Value"])
                    break
                else:
                    continue
        else:  # If it's just a standard metric, add it to currmetrics
            currmetrics.add(metric["MetricName"])
    
    # Print the metrics and disk letters
    #print(currmetrics)
    #print(driveletters)
    
    
    #name of the instance followed by what it prints
    val = []
    #print(instanceName, ": ")
    missing = False
    # Check for missing metrics and disks
    for metric in AWS_metrics:
        if metric not in currmetrics:
            #print(metric, "not found")
            val.append(str(metric) + " not found")
            missing = True
    for letter in disks:
        if letter not in driveletters:
            #print(letter, "drive missing")
            val.append(str(letter) + " drive missing")
            missing = True
    if(not missing):
        val = ["Nothing is missing"]
    
    #return missing
    return {
        'statusCode': 200,
        'body': val
        
    }
