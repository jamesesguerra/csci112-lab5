# GROUP 8 - LAB 5

### Justification of data model:

To easily retrieve a user's order by status and by date, a new attribute `status_and_date` was added to the order entities. This will act as a composite sort key for the LSI as it combines the status of the order and the date into one string. An LSI was also created with `pk` as the partition key and the `status_and_date` field as the sort key. This makes it so that direct lookups can be made on the partition key with a username to retrieve a specific user's orders, and these orders can then be filtered by status and by date. These queries are efficient since performing a scan is unnecessary. The value given to the `status_and_date` fields are in the format `#STATUS#{status}#DATE#{YYYY}-{MM}-{DD}`. With the hierarchical format of the date, orders can also be retrieved with a specific date granularity. To retrieve orders placed during a specific year, a value for year just needs to be specified without indicating the month and date. To retrieve orders for a certain year *and* month, a value for the day just needs to be left out. And finally, to retrieve orders placed on a certain date, all values need to be specified. All of this functionality is carried out by the `query_orders_status_date()` function in the `order_ops.py` file.

To easily retrieve all the pending orders, a new GSI called `pending-orders-index` was created with the `status` attribute of the order entities used as the partition key. A sort key was not specified since conditional statements or filtering will not be performed on the queries made on the partition key since *all* the pending orders must be returned. By using the `status` attribute as the partition key, direct lookups can be made for rows that have a certain status without needing to perform a full scan. In this case, lookups for rows with a status of `Pending` are required, and the `query_pending_orders()` function in the `order_ops.py` file carries out this functionality.




