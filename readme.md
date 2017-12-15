A quick and dirty tool to do slow query analysis week over week on RDS
slowlogs.

Sample Output:

~~~~
+------------------------------------------------------------------------+------------------------+----------------------+
|                               Query Text                               | Average Execution Time | Total Execution Time |
+------------------------------------------------------------------------+------------------------+----------------------+
|  select teamid, count(*) as num_pitches from offlinepitches op where   |        5.231729        |     3149.500969      |
|             last_viewed>? and teamid > ? group by teamid               |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
| select userid, max(created) as created from touches t where userid is  |        3.869685        |     2329.550495      |
|               not ? and activity in(?+) group by userid                |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
|              select op.offlineid from offlinepitches op,               |       77.235173        |     1621.938640      |
|   emailmessageembeddedpitches ep, emailmessagerecipients emr where     |                        |                      |
|  op.offlineid=ep.offlineid and ep.emid=emr.emid and emr.email like ?   |                        |                      |
|           and op.teamid=? order by op.created desc limit ?             |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
| select distinct concat(recipient_first_name,?,recipient_last_name) as  |       14.753988        |     1298.350909      |
|  name from offlinepitches op, offlineemails oe where op.teamid=? and   |                        |                      |
|   op.offlineid=oe.offlineid and (oe.recipient_first_name like ? or     |                        |                      |
|                oe.recipient_last_name like ?) limit ?                  |                        |                      |
+------------------------------------------------------------------------+------------------------+----------------------+
~~~~
