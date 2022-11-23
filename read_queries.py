from pprint import pprint
import user_ops as user
import order_ops as order_ops   


if __name__ == '__main__':
        
    # query orders of tgrimes1 that have a status of "Placed" and a date of 2022-11-22
    orders = order_ops.query_orders_status_date("tgrimes1", "Placed", year="2022", month="11", day="22")
    
    for order in orders:
        pprint(order)
    
    # query all pending orders
    pending_orders = order_ops.query_pending_orders()
    
    for order in pending_orders:
        pprint(order)
    
    