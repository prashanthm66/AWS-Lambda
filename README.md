# AWS-Lambda
Repository contains 3 lambda function 
  a.bucketrplication.py
    Creates bucket replication from one region to another
  b.cloudtrail_logparsing.py
    unzip the cloudtrail delivered s3 and reads, separates event names and send them into another s3 bucket in html table format
  c.rds_copy_snapshots.py
    Copy rds snapshots from one region to another
