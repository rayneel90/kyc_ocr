# How to connect to the s3 instance

### Basic Configuration
run following command
```
aws configure
```
enter details as asked:
 * AWS Access Key ID - __AKIAVVSA4252J4EBMO7G__
 * AWS Secret Access Key - __i+fKFVR/dmwQDQjqJp/z9c4L9FYhw5bRHkpTRPjL__
 * Default region name - __ap-southeast-1__
 * Default output format - __json__
 
 *These details are created from my security credentials segment/create access key. They are also stored in aws access key.csv*
 

### MFA configuration
In order to configure the CLI with multi-factor-authentication, we need to run following command:
```
aws sts get-session-token --serial-number arn:aws:iam::389904390004:mfa/nilabja.ray@dcbbank.com --duration-seconds 129600 --token-code <token_from mfa_device>
```
