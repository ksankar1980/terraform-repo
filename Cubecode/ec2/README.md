# Pre-requisites
- Python 2.7, boto3

# Create an EC2 instance using parameters
- save a copy of the file `../<<profile>>-ec2-settings.json` in this folder
- make changes you need. The file must be a valid JSON document

Run the runbook using the ec2-linux template for Amazon Linux or RHEL7.3 Linux and the ec2-windows template for Windows 2012R2 or 2016

`./runbook_ec2.py create <<profile >>linux stack_name` or `./runbook_ec2.py create <<profile>> windows stack_name` where `stack_name` is a unique name for the stack in the Region per AWS Account and `profile` is the local AWS CLI profile.

#EOF
