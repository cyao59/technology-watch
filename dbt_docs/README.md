# dbt project documentation README

## Sharing Documentation overview

Blocks docs begin and end with jinja docs tag and you place your documentation text between.
This approach can be highly beneficial when you include large description, formatted texts or reusable definition/description blocks.

By invoking the name of the docs block, you can reuse it across multiple tables or models.
This is another example where DBT supports dry coding principles which stands for don't repeat yourself.

However it's worth mentioning that you can include multiple dot blocks within a single dot MD file.

## Examples

Suppose we have a table status and shipped is a common attribute in more one table.

- **Example 1 : Description status table.**

**{% docs table_status %}**

In this table you will find the status of all the process of shipping.
| status         | description                                                               |
|----------------|---------------------------------------------------------------------------|
| placed         | The order has been placed but has not yet left the warehouse              |
| shipped        | The order has ben shipped to the customer and is currently in transit     |
| completed      | The order has been received by the customer                               |
| returned       | The order has been returned by the customer and received at the warehouse |

**{% enddocs %}**

- **Example 2 : Description column shipped.**

**{% docs shipped %}** 
The order has ben shipped to the customer and is currently in transit.
**{% enddocs %}** 

# DBT  Docs Benefits

* Improve communication among stakeholders
* Makes project understandable and maintainable
* Accelerates new team members onboarding
* Self-service portal for common queries
                and much more ....

## References

* [link](https://docs.getdbt.com/docs/collaborate/documentation#using-docs-blocks)