## EC2 manager script
A simple python script to demonstrate the basic work with AWS EC2 using the "boto3" SDK.


--- 


## Features
-Loads AWS region from '.env'
-Lists EC2 instances in the selected region
-Simulates launching a new instance(using Dryrun = True)
-provide start,stop, terminate operations for existing EC2 instances

---

## Requirements
-Python 3.9+
- AWS credentials configured locally (via AWS CLI or environment)
- `.env` file containing:
```bash
AWS_REGION=eu-central-1
```
    
## Usage
```bash
pip install -r requirements.txt
python ec2_manager.py