#!/usr/bin/env python
########
# This script takes tree arguments and supports two modes of operation:
# ./runbook.py <mode> <profile> <stack> <parameters>
#
# Where <mode> is
# - 'create' - will create stacks in this folder
# - 'update' - will update stacks in this folder
# - 'delete' - will delete all stack in this folder
#
# <profile> points back to the profiles configured in your ~/.aws/config
#
# <stack> is
# - linux
# - windows
#
# Parameters are settings file available on the local filesysten. 
#(ec2-settings.json and ../AccountSettings.json)
#
# This script allows orchestration of CloudFormation stacks and or 
# update and deletion of EC2 instances. Any code, applications, scripts, 
# templates, proofs of concept, documentation and other items provided by 
# Cube Networks under this SOW are \"Cube Networks content.\" All such 
# content is provided by Cube Networks, and is subject to the terms of 
# the Agreement. The Customer is solely responsible for using, deploying, 
# testing, and supporting any code and applications provided by Cube Networks 
# under this SOW.
#
# Developed by Trevor Furnell <trevor.furnell@cubenetworks.com.au>
#     - based on scripts developed by Amazon Web Service
# Mar 2018
########

import sys
import boto3
import logging
import json
import time
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

Mode = sys.argv[1]
Profile = sys.argv[2]
Stack = sys.argv[3]

# Retrieve custom account settings file, or default
try:
    StackName = sys.argv[4]
except:
    print "You must specify a stack name"
# Retrieve EC2 details from a template file, or default
if Mode == 'create' or Mode == 'update':
    try:
        EC2Settings = sys.argv[5]
    except:
        print "You must specify an *-ec2-settings json file"
# Retrieve custom account settings file, or default
    try:
        AccountSettings = sys.argv[6]
    except:
        AccountSettings = "../accountSettings.json"

########
# Read in EC2 settings
########
if Mode == 'create' or Mode == 'update':
    with open(EC2Settings) as AEC2SettingsFh:
        EC2SettingsJson = json.load(AEC2SettingsFh)

########
# Read in account settings
########
if Mode == 'create' or Mode == 'update':
    with open(AccountSettings) as AccountSettingsFh:
        AccountSettingsJson = json.load(AccountSettingsFh)

        # The following parameter are using for Tagging purposes
        # Tag "Environment" can be Development, Integration or Production
        ENVIRONMENT=AccountSettingsJson["Tags"]["Environment"]
        # Tag "CostCenter" for accounting and showback by Cost Center
        COSTCENTER=AccountSettingsJson["Tags"]["CostCenter"]
        # Tag "Cluster" for the Application Cluster name, if applicable
        CLUSTER=AccountSettingsJson["Tags"]["Cluster"]
        # Tab "InfoSec" reserved for security, e.g. all resources that must comply with regulations
        INFOSEC=AccountSettingsJson["Tags"]["InfoSec"]

#########################################################
# Python logic below, should not be necessary to change
#########################################################
Session = boto3.Session(profile_name=Profile)
Cfn_Client = Session.client('cloudformation')
def orchestrate_stacks():
    if Mode == 'create' or Mode == 'update':

        #ec2-linux.template
        if Stack == 'linux':
            create_update(
                stack='ec2-linux',
                parameters= {
                    # Size in GB of the second drive
                    'EBSSecondDriveSize' : EC2SettingsJson["Config"]["EBSSecondDriveSize"],
                    # Size in GB of the primary drive
                    'EBSSize': EC2SettingsJson["Config"]["EBSSize"],
                    # Instance Type - for more information see https://aws.amazon.com/ec2/instance-types/
                    'InstanceType' : EC2SettingsJson["Config"]["InstanceType"],
                    # The Operating System Type for the EC2 Instances. Can be AmazonLinux64, RHEL73, WIN2K12R2, WIN2016
                    'OsType' : EC2SettingsJson["Config"]["OsType"],
                    # The Security Group for the EC2 instance
                    'SecurityGroup' : EC2SettingsJson["Config"]["SecurityGroup"],
                    # The name of the Key used to SSH into Linux instances or to decrypt Windows passwords
                    'KeyName' : EC2SettingsJson["Network"]["KeyName"],
                    # The ID of the subnet the EC2 instance will be deployed into
                    'SubnetId' : EC2SettingsJson["Network"]["SubnetId"],
                    # The ID of the VPC the EC2 instance will be deployed into
                    'VpcId' : EC2SettingsJson["Network"]["VpcId"],
                    # A Tag to describe the application role
                    'ApplicationRole' : EC2SettingsJson["Tags"]["ApplicationRole"],
                    # A Tag to describe the Cluster the application belongs to
                    'Cluster' : CLUSTER,
                    # A Tag to describe the Cost Center for the EC2
                    'CostCenter' : COSTCENTER,
                    # A Tag to describe the environment the EC2 will be deployed into (Development, Integration, Production are the allowed value. Change ec2-linux and ec2-windows templates to change values)
                    'Environment' : ENVIRONMENT,
                    # A Tag to describe the Hostname
                    'Hostname' : EC2SettingsJson["Tags"]["Hostname"],
                    # A Tag to describe security standard to comply with
                    'InfoSec' : INFOSEC,
                    # A Tag to describe the Instance Name as it will display in the console
                    'InstanceName' : EC2SettingsJson["Tags"]["InstanceName"],
                    # A Tag for the email of requestor. The email address will be used in the SNS topic
                    'RequestorEmail' : EC2SettingsJson["Tags"]["RequestorEmail"],
                    # A Tag for the Name of requestor.
                    'RequestorName' : EC2SettingsJson["Tags"]["RequestorName"],
                    # A Tag to specify a generic amount of time to schedule an operation (e.g. perform full backups every "Retention" days)
                    'Retention' : EC2SettingsJson["Tags"]["Retention"],
                    # A Tag for the System Administrator name.
                    'SystemAdministrator' : EC2SettingsJson["Tags"]["SystemAdministrator"],
                    # A Tag for the System Manager name.
                    'SystemManager' : EC2SettingsJson["Tags"]["SystemManager"],
                    # Another Tag to describe the name of the instance
                    'SystemName' : EC2SettingsJson["Tags"]["SystemName"],
                    # Another Tag to describe the ownersthip of the instance
                    'SystemOwner' : EC2SettingsJson["Tags"]["SystemOwner"],
                    # Whether or not the detailed monitoring is enabled (true/false)
                    'DetailedMonitoring' : EC2SettingsJson["Config"]["DetailedMonitoring"]
                }
            )
        #ec2-windows.template
        if Stack == 'windows':
            create_update(
                stack='ec2-windows',
                parameters= {
                    # Size in GB of the second drive
                    'EBSSecondDriveSize' : EC2SettingsJson["Config"]["EBSSecondDriveSize"],
                    # Size in GB of the primary drive
                    'EBSSize': EC2SettingsJson["Config"]["EBSSize"],
                    # Instance Type - for more information see https://aws.amazon.com/ec2/instance-types/
                    'InstanceType' : EC2SettingsJson["Config"]["InstanceType"],
                    # The Operating System Type for the EC2 Instances. Can be AmazonLinux64, RHEL73, WIN2K12R2, WIN2016
                    'OsType' : EC2SettingsJson["Config"]["OsType"],
                    # The Security Group for the EC2 instance
                    'SecurityGroup' : EC2SettingsJson["Config"]["SecurityGroup"],
                    # The name of the Key used to SSH into Linux instances or to decrypt Windows passwords
                    'KeyName' : EC2SettingsJson["Network"]["KeyName"],
                    # The ID of the subnet the EC2 instance will be deployed into
                    'SubnetId' : EC2SettingsJson["Network"]["SubnetId"],
                    # The ID of the VPC the EC2 instance will be deployed into
                    'VpcId' : EC2SettingsJson["Network"]["VpcId"],
                    # A Tag to describe the application role
                    'ApplicationRole' : EC2SettingsJson["Tags"]["ApplicationRole"],
                    # A Tag to describe the Cluster the application belongs to
                    'Cluster' : CLUSTER,
                    # A Tag to describe the Cost Center for the EC2
                    'CostCenter' : COSTCENTER,
                    # A Tag to describe the environment the EC2 will be deployed into (Development, Integration, Production are the allowed value. Change ec2-linux and ec2-windows templates to change values)
                    'Environment' : ENVIRONMENT,
                    # A Tag to describe the Hostname
                    'Hostname' : EC2SettingsJson["Tags"]["Hostname"],
                    # A Tag to describe security standard to comply with
                    'InfoSec' : INFOSEC,
                    # A Tag to describe the Instance Name as it will display in the console
                    'InstanceName' : EC2SettingsJson["Tags"]["InstanceName"],
                    # A Tag for the email of requestor. The email address will be used in the SNS topic
                    'RequestorEmail' : EC2SettingsJson["Tags"]["RequestorEmail"],
                    # A Tag for the Name of requestor.
                    'RequestorName' : EC2SettingsJson["Tags"]["RequestorName"],
                    # A Tag to specify a generic amount of time to schedule an operation (e.g. perform full backups every "Retention" days)
                    'Retention' : EC2SettingsJson["Tags"]["Retention"],
                    # A Tag for the System Administrator name.
                    'SystemAdministrator' : EC2SettingsJson["Tags"]["SystemAdministrator"],
                    # A Tag for the System Manager name.
                    'SystemManager' : EC2SettingsJson["Tags"]["SystemManager"],
                    # Another Tag to describe the name of the instance
                    'SystemName' : EC2SettingsJson["Tags"]["SystemName"],
                    # Another Tag to describe the ownersthip of the instance
                    'SystemOwner' : EC2SettingsJson["Tags"]["SystemOwner"],
                    # Whether or not the detailed monitoring is enabled (true/false)
                    'DetailedMonitoring' : EC2SettingsJson["Config"]["DetailedMonitoring"]
                }
            )

    elif Mode == 'delete':
        if Stack == 'linux':
            delete('ec2-linux')
        if Stack == 'windows':
            delete('ec2-windows')

##### Helper functions from here, we may consider moving these into separate module
def wait(stack):
    if Mode == 'crate' or Mode == 'updade':
        logging.info('wait-'+Mode+'-stack '+Profile+'-'+stack)
    if Mode == 'delete':
        logging.info('wait-delete-stack '+StackName)
    Cfn_Client.get_waiter('stack_'+Mode+'_complete').wait(
        StackName=Profile+'-'+stack
    )

def create_update(stack, parameters):
        logging.info(Mode+'-stack '+Profile+'-'+stack)
        with open(stack+'.template', 'r') as f:
            # generate verbose/required parameter structure
            params = []
            for key, value in parameters.items():
                param = {}
                param["ParameterKey"] = key
                param["ParameterValue"] = value
                param["UsePreviousValue"] = False
                params.append(param)

            if Mode == 'create':
                Cfn_Client.create_stack(
                    StackName=StackName,
                    TemplateBody=f.read(),
                    Parameters=params,
                    #DisableRollback=True
                )
            elif Mode == 'update':
                Cfn_Client.update_stack(
                    StackName=StackName,
                    TemplateBody=f.read(),
                    Parameters=params,
                    #DisableRollback=True
                    )
        wait(stack)

def delete(stack):
    logging.info('delete-stack '+stack)
    Cfn_Client.delete_stack(
        StackName=StackName
    )
    if Mode == 'crate' or Mode == 'updade':
        wait(stack)
    if Mode == 'delete':
            wait(StackName)

def get_output_from_stack(stack, output):
    stack_description_json = Cfn_Client.describe_stacks(StackName=Profile+'-'+stack)['Stacks'][0]
    outputs = stack_description_json['Outputs']
    for o in outputs:
        if o["OutputKey"] == output:
            return o["OutputValue"]

if __name__ == '__main__':
    orchestrate_stacks()

#EOF
