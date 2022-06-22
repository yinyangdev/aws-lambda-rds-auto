import json
import os
import sys
import boto3
import traceback

def check_status(action, status):
    if action == 'start' and status == 'stopped':
        return True
    elif action == 'stop' and status == 'available':
        return True
    else:
        return False

def cluster_action(client, action, dbclusteridentifier):
    try:
        if action == 'start':
            client.start_db_cluster(DBClusterIdentifier=dbclusteridentifier)
            print('started cluster {}.'.format(dbclusteridentifier))
        elif action == 'stop':
            client.stop_db_cluster(DBClusterIdentifier=dbclusteridentifier)
            print('stopped cluster {}.'.format(dbclusteridentifier))
        else:
            print('Invalid action.')
    except:
        print(traceback.format_exc())

def instance_action(client, action, dbinstanceidentifier):
    try:
        if action == 'start':
            client.start_db_instance(DBInstanceIdentifier=dbinstanceidentifier)
            print('started instance {}.'.format(dbinstanceidentifier))
        elif action == 'stop':
            client.stop_db_instance(DBInstanceIdentifier=dbinstanceidentifier)
            print('stopped instance {}.'.format(dbinstanceidentifier))
        else:
            print('Invalid action.')
    except:
        print(traceback.format_exc())

def lambda_handler(event, context):
    try:
        region = event['Region']
        tagkey = event.get('TagKey', None)
        tagvalue = event['TagValue']
        action = event['Action']
        client = boto3.client('rds', region_name = region)

        db_clusters = client.describe_db_clusters()
        for cluster in db_clusters['DBClusters']:
            if check_status(action, cluster['Status']):
                if tagkey is not None:
                    for tag in cluster['TagList']:
                        if tag['Key'] == tagkey and tag['Value'] == tagvalue:
                            cluster_action(client, action, cluster['DBClusterIdentifier'])
                else:
                    cluster_action(client, action, cluster['DBClusterIdentifier'])
            else:
                print('No Action: Clusters status {}.'.format(cluster['Status']))

        db_instances = client.describe_db_instances()
        v_readreplica = []
        for i in db_instances['DBInstances']:
            readreplica = i['ReadReplicaDBInstanceIdentifiers']
            v_readreplica.extend(readreplica)

        for instance in db_instances['DBInstances']:
            if instance['Engine'] not in ['aurora-mysql', 'aurora-postgresql']:
                if instance['DBInstanceIdentifier'] not in v_readreplica and len(instance['ReadReplicaDBInstanceIdentifiers']) == 0:
                    if check_status(action, instance['DBInstanceStatus']):
                        if tagkey is not None:
                            for tag in instance['TagList']:
                                if tag['Key'] == tagkey and tag['Value'] == tagvalue:
                                    instance_action(client, action, instance['DBInstanceIdentifier'])
                        else:
                            instance_action(client, action, instance['DBInstanceIdentifier'])
                    else:
                        print('No Action: instance status {}.'.format(cluster['Status']))

        return {
            "statusCode": 200,
            "message": 'Finished automatic start / stop RDS instances process. [Region: {}, Tag: {} : {}, Action: {}]'.format(region,tagkey,tagvalue, action)
        }
    except:
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "message": 'An error occured at automatic start / stop RDS clusters and instances process.'
        }
