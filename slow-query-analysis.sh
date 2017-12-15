# Requirements: percona-toolkit, jq, Python, PrettyTable (via pip).

env=`cat environments.txt`
date=`date +%Y%m%d`
rm $homedir/tmp/slow-query*
hook=`cat hook.txt`
token=`cat token.txt`
region='us-west-2'
homedir='/opt/slow-query-analysis'
for environment in $env
do
  for host in `cat $env-hosts.txt`
  do
    loglist=`aws --region=$region --profile=$environment --output text rds describe-db-log-files --db-instance-identifier $host | grep slow | sort -k2 | awk {'print $3'} | tail -4`
    echo "loglist: $loglist"
    for each in $loglist
    do
      aws --region=$region --profile=prd --output text rds download-db-log-file-portion --db-instance-identifier $host --log-file-name $each >> $homedir/tmp/slow-query-tmp-$host.log
    done

    pt-query-digest $homedir/tmp/slow-query-tmp-$host.log --output json | jq "limit(10; .classes) | [.[] | {fingerprint: .fingerprint, checksum: .checksum, metrics: .metrics.Query_time}]" > $homedir/thisweek-slowquery-$host.json

    cp $homedir/thisweek-slowquery-$host.json $homedir/archive/slowquery-$host-$date.json

    python compare-slow.py $homedir/thisweek-slowquery-$host.json $homedir/lastweek-slowquery-$host.json

    rm $homedir/lastweek-slowquery-$host.json
    mv $homedir/thisweek-slowquery-$host.json $homedir/lastweek-slowquery-$host.json

    curl -X POST --data-urlencode "payload={\"channel\": \"#db-advice-team\", \"username\": \"slow-query-bot\", \"text\": \"New slow queries detected on $host this week:\n\", \"icon_emoji\": \":thisisfine:\"}" $hook
    curl -F file=@Output.txt -F token=$token  -F channels=\#db-advice-team https://slack.com/api/files.upload

    mv Output.txt ./archive/Output-$host-$date.txt
  done
done
