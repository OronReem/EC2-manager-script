
"""
Simple EC2 manager script for practice.
-Loads AWS region from .env
-Lists instances in that region
-Simulates launching a new instance(currently on dryrun = True)
-Provides start/stop/terminate functions for a given instance ID

Requires valid AWS credentials in your environment.
"""

#this line brings the tool that knows how to read the env. file
from dotenv import load_dotenv
import os #operating systems
import boto3

load_dotenv() #reads the content from a .env file and puts it in the os
region = os.getenv("AWS_REGION") #gets the AWS region from the enviorment
print(f"AWS region loaded from .env: {region}")
ec2 = boto3.client("ec2", region_name=region)
print(f"EC2 client ready in region: {region}")

def list_instances(ec2):
    #we will extract the instances with describe_instances()
    response = ec2.describe_instances()
    count = 0
    for reservation  in response["Reservations"]:
        for instance in reservation["Instances"]:
            count += 1
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            state_name = instance["State"]["Name"]

            name_tag = "-"
            if "Tags" in instance:
                for tag in instance["Tags"]:
                    if tag["Key"] == "Name":
                        name_tag = tag["Value"]
            
            print(f"Instance ID: {instance_id} | State: {state_name} | Type: {instance_type} | Name: {name_tag}")

    if count == 0:
        print("No instances found in this region.")

def get_latest_ami(region):
    ssm = boto3.client("ssm", region_name = region)
    param_name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"
    result  = ssm.get_parameter(Name = param_name)
    ami_id = result["Parameter"]["Value"]
    print(f"Latest Amazon Linux AMI for {region}: {ami_id}")
    return ami_id

def launch_instance(ec2):
    try:
        ami_id = get_latest_ami(region)

        response = ec2.run_instances(
            #eu-central-1
            ImageId = ami_id,
            #free tier
            InstanceType = "t2.micro",
            MinCount = 1,
            MaxCount = 1,
            #Safety check
            DryRun = True
        )
        print ("Dry run successful", response)
    except Exception as e:
        if "DryRunOperation" in str(e):
            print(" :) Dry run successful, you have permission to launch instance")
        else:
            print(" :( Dry run failed", e)

def start_instance(ec2, instance_id):
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(f"Started instance {instance_id}")
        return response
    except Exception as e:
        print(f"Failed to start instance {instance_id} : {e}")

def stop_instance(ec2, instance_id):
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopped instance {instance_id}")
        return response
    except Exception as e:
        print(f"Failed to stop instance {instance_id} : {e}")

def terminate_instance(ec2, instance_id):
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Terminated instance {instance_id}")
        return response
    except Exception as e:
        print(f"Failed to terminate instance {instance_id} : {e}")

if __name__ == "__main__":
    list_instances(ec2)
    #launch_instance(ec2)
    #start_instance(ec2,"")
    #stop_instance(ec2, "")
    #terminate_instance(ec2,"")


