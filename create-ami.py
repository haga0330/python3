# coding: utf-8
"""AMI image creation."""

import boto3
import datetime
import os

client_ec2 = boto3.client('ec2')
resource_ec2 = boto3.resource('ec2')
dt_utc = datetime.datetime.now(tz=datetime.timezone.utc)
dt_jst = dt_utc + datetime.timedelta(hours=9)
dt_fm = "{0:%Y%m%d-%H%M%S}".format(dt_jst)

# Executing in the local environment
# TARGET_NAME_TAG = '***'
# Executing in the AWS Lambda environment
NAME_TAG_LIST = [x.strip() for x in os.environ["target_list"].split(',')]


def create_image(instance_name):
    """Extract instance ID from Name tag and create AMI."""
    instance_id = ""
    for reservation in client_ec2.describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if(tag["Key"] == "Name" and tag["Value"] == instance_name):
                    instance_id = instance["InstanceId"]
    if instance_id != "":
        print("Info: Found Instance_id " + instance_id + ".")
        instance = resource_ec2.Instance(instance_id)
        image_name = instance_name + "-createimage" + "_" + dt_fm
        instance.create_image(
                              Name=image_name,
                              Description=dt_fm + ' AMI created in Lambda.',
                              NoReboot=True
                              )
        print("Info: Created AMI " + image_name + " for " + instance_id + ".")
    else:
        print("Error: Name tag of " + instance_name + " could not be found.")


def lambda_handler(event, context):
    for target_tag in NAME_TAG_LIST:
        create_image(target_tag)
