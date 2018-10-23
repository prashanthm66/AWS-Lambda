# AWS-Lambda
1.	Purpose:  
This document is the runbook for Lambda Functions to copy RDS snapshots from us-west-2 region to us-east-1 and s3 bucket replication. It is a basic document that describes two lambda functions to RDS snapshots from us-west-2 region to us-east-1. 
 
The document has two sections — Copying of RDS snapshots and S3 bucket replication. 
Lambda function to copy RDS snapshots from one region to another: 
Dependencies: 
- IAM roles; lambda to access RDS 
- IAM Policies; RDS: List access –Describe DBSnapshots, Write access –Copy DBSnapshot 
- Runtime; Python3.6 
  
2.	Procedure:  

- Go to lambda Console. 
- Click on Create function. 
     - Specify Name of the lambda Function  
     - Runtime as Python 3.6 
     - Choose IAM role 
- Under function code section; specify 'code entry type' as 'Edit code inline' and paste the code and save it. 
  
3.	Source Code dependencies:
  
- Python 3.6 
- Boto3 
- json 
- Modules 
     - import boto3 
     - from datetime import datetime, timedelta 
     - from dateutil.tz import * 
      
4.	Code Description:
Code Description: 
- Get RDS resource into lambda  
      rds_client = boto3.client('rds') 
- Get RDS resource from another region into lambda 
      con = boto3.client('rds', region_name='us-west-2') 
- Todays date    
      today = datetime.today() 
- Delete days = 7   
      delete_time = today - timedelta(days=7) 
- List of existing manual snapshots    
      snapshots = rds_client.describe_db_snapshots(SnapshotType='manual') 
- Replacing tzlocal to local  
      local = tzlocal() 
      delete_time = delete_time.replace(tzinfo = local) 
      today = today.replace(tzinfo=local) 
- Iterating snapshots Dictionary   
      for i in snapshots['DBSnapshots']: 
- In the iteration if the snapshotcreation time is 'today', then copy those snapshots to other region using the 'con.copy_db_snapshot()' boto3 method.       
    if i['SnapshotCreateTime'] == today: 
     respon = con.copy_db_snapshot(SourceDBSnapshotIdentifier= i['DBSnapshotArn'],TargetDBSnapshotIdentifier= i['DBSnapshotIdentifier'],SourceRegion='us-east-1') 
- Iterating snapshots Dictionary again  
   for i in snapshots['DBSnapshots']: 
- In the iteration if the snapshotcreation time is 'delete_time' that is 7 days, then delete those snapshots in the current region using the 'rds_client.delete_db_snapshot' boto3 method.   
     if i['SnapshotCreateTime'] >= delete_time: 
      response = rds_client.delete_db_snapshot(DBSnapshotIdentifier=i['DBSnapshotIdentifier']) 
      print ("deleted:", response) 
5.	Note:    
- Region specified in the code is us-east-1 and us-west-2(If needed can change the regions) 
- Original snapshots from us-east-1 getting copied to us-west-2. 
