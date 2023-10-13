# Overview
'''
This document expose a custom macro to establish standardized and consistent descriptions for respective columns from table and their accepted_valued test. 
This approach streamlines the documentation process, ensuring clarity and uniformity in describing data structures and attributes throughout the project.
'''

# Columns description 

##  Column id
{% docs id %}
Warehouse's id.
{% enddocs %}

##  Column placed
{% docs placed %}
The order has been placed but has not yet left the warehouse.
{% enddocs %}

##  Column shipped
{% docs shipped %}
The order has ben shipped to the customer and is currently in transit.
{% enddocs %}

##  Column completed
{% docs completed %}
The order has been received by the customer.
{% enddocs %}

##  Column returned
{% docs returned %}
The order has been returned by the customer and received at the warehouse.
{% enddocs %}