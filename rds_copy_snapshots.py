import boto3
from datetime import datetime, timedelta
from dateutil.tz import *
from boto3 import Session

con = boto3.client('rds', region_name='us-east-1')

def lambda_handler(event, context):
  rds_client = boto3.client('rds')
  today = datetime.today()
  delete_time = today - timedelta(days=3)
  snapshots = rds_client.describe_db_snapshots(SnapshotType='manual')
 # print(snapshots)
  local = tzlocal()
  delete_time = delete_time.replace(tzinfo = local)
  today = today.replace(tzinfo=local)

  for i in snapshots['DBSnapshots']:
      if i['SnapshotCreateTime'] == today:
          respon = con.copy_db_snapshot(
              SourceDBSnapshotIdentifier= i['DBSnapshotArn'],
              TargetDBSnapshotIdentifier= i['DBSnapshotIdentifier'],
              SourceRegion='us-west-2'
              )

  for i in snapshots['DBSnapshots']:
      if 'SnapshotCreateTime' in i:
          if i['SnapshotCreateTime'] >= delete_time:
              response = rds_client.delete_db_snapshot(
                  DBSnapshotIdentifier=i['DBSnapshotIdentifier'])