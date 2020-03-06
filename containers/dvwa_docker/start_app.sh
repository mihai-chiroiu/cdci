#!/bin/bash
service mysql start; 
mysql=( mysql -uroot -pvulnerables )
for i in {30..0}; do
  if echo 'SELECT 1' | "${mysql[@]}" &> /dev/null; then
	  break
  fi
  echo 'MySQL init process in progress...'
  sleep 1 
done
if [ "$i" = 0 ]; then
  echo >&2 'MySQL init process failed.'
  exit 1 
fi
mysql -uroot -pvulnerables < init_mysql.sql ; 
service apache2 start
echo 'Sleeping now ...'
while true
do
  tail -f /var/log/apache2/*.log
  exit 0
done
