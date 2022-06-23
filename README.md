# AWS Lambda RDS Auto Start / Stop

AWS RDS 自動起動・停止スクリプト

- Python 3.9

## Json

- All Database

  ```json
  {
    "Region": "xxxxxx",
    "Action": "start"   // start or stop
  }
  ```

- Tag filter

  ```json
  {
    "Region": "xxxxxx",
    "TagKey": "xxxxxx",
    "TagValue": "xxxxxx",
    "Action": "start"   // start or stop
  }
  ```

  

## IAM Role Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "rds:DescribeDBClusterEndpoints",
                "rds:DescribeDBClusterParameterGroups",
                "rds:DescribeDBClusterParameters",
                "rds:DescribeDBClusters",
                "rds:DescribeDBEngineVersions",
                "rds:DescribeDBInstances",
                "rds:DescribeDBLogFiles",
                "rds:DescribeGlobalClusters",
                "rds:DescribeOptionGroups",
                "rds:DescribePendingMaintenanceActions",
                "rds:DescribeReservedDBInstances",
                "rds:DescribeReservedDBInstancesOfferings",
                "rds:DescribeSourceRegions",
                "rds:DescribeValidDBInstanceModifications",
                "rds:ListTagsForResource",
                "rds:StartDBCluster",
                "rds:StartDBInstance",
                "rds:StopDBCluster",
                "rds:StopDBInstance"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

