# AWS Organizations Master Account
This folder contains a set of AWS Organizations Service Control Policies (SCP) to be imported into the AWS Organization and can be attached to member accounts or Organization Units (OU) in the Organization.

## Service Control Policies (SCP)
SCP's allow you to lock down the services that are allowed to be used within an account. SCP’s can be associated with an Organizational Unit (OU) and accounts can be grouped in OU’s. The following example SCP’s are provided by AWS Professional Services:

*organizations-policy-scp-root.json*
This SCP is to be attached to the root of the Organization making it applicable to all accounts in the organization. Only add denies here that need to applied across all accounts including the master account.

*organizations-policy-scp-security.json*
A SCP specifically designed for the security account with a couple of deny statements to make sure no one is able to delete the S3 buckets or any content in it.

*organizations-policy-scp-vanilla.json*
A ‘vanilla’ template allowing the most commonly used AWS services.

## CLI Commands
Using the SCP's consists of three steps, first you need to create the SCP's in your AWS Organization based of the templates provided. The next step is to attach the policies to the right accounts or OU's. The last step consists of removing the default policy from your account if applicable.

### Creating the SCP's
Run the commands below to have the SCP's created in your organization. We specified the profile master to do this with credentials from the master account which should be configured in your ~/.aws/config

*aws organizations create-policy --profile master --type SERVICE_CONTROL_POLICY --description "SCP for the root of the Organization denying services that can not be used anywhere with the AWS Organization" --name Policy-SCP-Root --content file://organizations-policy-scp-root.json*
*aws organizations create-policy --profile master --type SERVICE_CONTROL_POLICY --description "SCP for the Security account limiting the services that can be used and denying certain actions to protect logging data" --name Policy-SCP-Security --content file://organizations-policy-scp-security.json*
*aws organizations create-policy --profile master --type SERVICE_CONTROL_POLICY --description "SCP for other accounts allowing the most commonly used AWS services" --name Policy-SCP-Vanilla --content file://organizations-policy-scp-vanilla.json*

### Attaching SCP's
The next step is to attach the newly created SCP's to the accounts in the organization. Use the output of the previous commands to grab the policy id and use the *aws organizations list-roots --profile master*, *aws organizations list-organizational-units-for-parent --profile master* and *aws organizations list-accounts --profile master* command to get the target-id of the target accounts, root and OU's.

Use the following command to attach the policies:

*aws organizations attach-policy --profile master --policy-id <value> --target-id <value>*

### Detaching default SCP
By default the *p-FullAWSAccess* AWS managed SCP is attached to all accounts, repeat the following command for all target id's you want the default (allow all) policy to be detached:

*aws organizations detach-policy --profile master --policy-id p-FullAWSAccess --target-id <value>*

## Documentation
[AWS Organizations Documentation](http://docs.aws.amazon.com/cli/latest/reference/organizations/index.html)
[AWS Organizations Create Policy Documentation](http://docs.aws.amazon.com/cli/latest/reference/organizations/create-policy.html)
[AWS Organizations Attach Policy Documentation](http://docs.aws.amazon.com/cli/latest/reference/organizations/attach-policy.html)
