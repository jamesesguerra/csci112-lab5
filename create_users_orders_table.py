#!/usr/bin/env python3
import boto3


def create_invertible_table(
        ddb_table_name,
        partition_key,
        sort_key
        ):

    dynamodb = boto3.resource('dynamodb')

    table_name = ddb_table_name
    
    attribute_definitions = [
        {'AttributeName': partition_key, 'AttributeType': 'S'},
        {'AttributeName': sort_key, 'AttributeType': 'S'},
        {'AttributeName': 'status_and_date', 'AttributeType': 'S'},
        {'AttributeName': 'status', 'AttributeType': 'S'}
    ]
    
    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}, 
                  {'AttributeName': sort_key, 'KeyType': 'RANGE'}]
                  
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    
    global_secondary_indexes = [
    {
        'IndexName': 'inverted-index',
        'KeySchema': [
            {'AttributeName': sort_key, 'KeyType': 'HASH'},
            {'AttributeName': partition_key, 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['quantity', 'price', 'status', 'product_name']
        },
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    },
    {
        'IndexName': 'pending-orders-index',
        'KeySchema': [ { 'AttributeName': "status", 'KeyType': 'HASH' } ],
        'Projection': { 'ProjectionType': 'ALL' },
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }]

    local_secondary_indexes = [{
        'IndexName': 'status-date-index',
        'KeySchema': [
            {'AttributeName': partition_key, 'KeyType': 'HASH'},
            {'AttributeName': 'status_and_date', 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'ALL'},
    }]
    
    try:
        # Create a DynamoDB table with the parameters provided
        table = dynamodb.create_table(TableName=table_name,
                                      KeySchema=key_schema,
                                      AttributeDefinitions=attribute_definitions,
                                      ProvisionedThroughput=provisioned_throughput,
                                      GlobalSecondaryIndexes=global_secondary_indexes,
                                      LocalSecondaryIndexes=local_secondary_indexes
                                      )
        table.wait_until_exists()
        return table
    except Exception as err:
        print("{0} Table could not be created".format(table_name))
        print("Error message {0}".format(err))
        
def delete_table(name):
    dynamodb = boto3.resource('dynamodb')  
    table = dynamodb.Table(name)
    table.delete()

if __name__ == '__main__':
    table = create_invertible_table("users-orders-items", "pk", "sk")
    
    # delete_table("users-orders-items")
