import boto3
import time
from datetime import datetime

ss = boto3.client('s3', region_name='us-west-2')
s3 = boto3.client('s3', region_name = 'us-west-1')
def lambda_handler(event, context):
    try:
        src_bucket = s3.create_bucket(ACL='private',Bucket='src-bucket-replica-6258',CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
        src_versioning = s3.put_bucket_versioning(Bucket='src-bucket-replica-6258',VersioningConfiguration={'Status': 'Enabled'})
        src_encryption = s3.put_bucket_encryption(
            Bucket='src-bucket-replica-6258',
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                            
                        }
                        
                    },
                    ]
                
            }
            )
        print("Souce Bucket created:", src_bucket)
    except:
        print("Souce Bucket already created")
    
    try:
        dst_bucket = ss.create_bucket(ACL='private',Bucket='dst-bucket-replica-us-west-2',CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        dst_versioning = ss.put_bucket_versioning(Bucket='dst-bucket-replica-us-west-2',VersioningConfiguration={'Status': 'Enabled'})
        dst_encryption = ss.put_bucket_encryption(
            Bucket='dst-bucket-replica-us-west-2',
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                            
                        }
                        
                    },
                    ]
                
            }
            )
        print("Destination Bucket created:", dst_bucket)
    except:
        print("Destination Bucket already created")
    
    time.sleep(20)    
    
    
    respon = s3.put_bucket_replication(
    Bucket='src-bucket-replica-6258',
    ReplicationConfiguration={
        "Role": "arn:aws:iam::role",
        "Rules": [
            {
                'ID': 'ObjReplication',
                "Prefix": "",
                "Status": "Enabled",
                "Destination": {
                "Bucket": "arn:aws:s3:::dest-bucket",
                "StorageClass": "STANDARD"
           }
        }
     ]
    }
) 
    
