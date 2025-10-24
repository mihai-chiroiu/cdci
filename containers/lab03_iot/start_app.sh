#!/bin/bash
service mysql start; 
mysql=( mysql -uroot )
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
mysql < init_mysql.sql ; 
python3 app.py
