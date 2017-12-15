A quick and dirty tool to do slow query analysis week over week on RDS
slowlogs.

Sample Output:

~~~~
+------------------------------------------------------------------------+------------------------+----------------------+
|                               Query Text                               | Average Execution Time | Total Execution Time |
+------------------------------------------------------------------------+------------------------+----------------------+
|  select foo, count(*) as foo from foobar fooba where                    |        5.231729        |     3149.500969      |
|             created_time>? and flange > ? group by bar                 |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
| select foo, max(created) as created from bar b  where id is            |        3.869685        |     2329.550495      |
|               not ? and foobar   in(?+) group by id                    |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
~~~~
