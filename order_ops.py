#!/usr/bin/env python3

import boto3
import hashlib
import random
from boto3.dynamodb.conditions import Key
from datetime import datetime


def add_item(order_id, product_name, quantity, price): 
    item_id = hashlib.sha256(product_name.encode()).hexdigest()[:8]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    item = {
        'pk'           : '#ITEM#{0}'.format(item_id), 
        'sk'           : '#ORDER#{0}'.format(order_id),
        'product_name' : product_name,
        'quantity'     : quantity,
        'price'        : price,
        'status'       : "Pending"    
    }
    table.put_item(Item=item)
    print("Added {0} to order {1}".format(product_name, order_id))
    
def checkout(username, address, items): 
    order_id = hashlib.sha256(str(random.random()).encode()).hexdigest()[:random.randrange(1, 20)]
    current_date = datetime.now().strftime('%Y-%m-%d')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    item = {
        'pk'              : '#USER#{0}'.format(username), 
        'sk'              : '#ORDER#{0}'.format(order_id),
        'address'         : address,
        'status_and_date' : f'#STATUS#Placed#DATE#{current_date}',
        'status'          : 'Placed'
    }
    table.put_item(Item=item)
    
    for item in items:
        add_item(order_id, 
                 item['product_name'], 
                 item['quantity'], 
                 item['price']
                 )

def query_user_orders(username):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sk').begins_with('#ORDER#')
    )
    return response['Items']

def query_orders_status_date(username, status, year=None, month=None, day=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')

    if year and month and day:
        status_date_query = f"#STATUS#{status}#DATE#{year}-{month}-{day}"
    elif year and month:
        status_date_query = f"#STATUS#{status}#DATE#{year}-{month}"
    elif year:
        status_date_query = f"#STATUS#{status}#DATE#{year}"
    else:
        status_date_query = f"#STATUS#{status}"

    response = table.query(
        IndexName='status-date-index',
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('status_and_date').begins_with(status_date_query)
    )
    return response['Items']

def query_pending_orders():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')

    response = table.query(
        IndexName='pending-orders-index',
        KeyConditionExpression=Key('status').eq('Pending')
    )
    return response['Items']
    
def query_order_items(order_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')

    response = table.query(
        IndexName='inverted-index',
        KeyConditionExpression=Key('pk').eq('#ORDER#{0}'.format(order_id)) & 
                               Key('sk').begins_with('#ITEM#')
    )
    return response['Items']
