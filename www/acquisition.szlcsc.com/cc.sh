#!/bin/bash
#文件名
FILE_NAME='log.txt'
#获取文件做后修改时间戳
a=`stat -c %Y  $FILE_NAME`
#格式化时间戳
formart_date=`date '+%Y-%m-%d %H:%M:%S' -d @$a`

old_pid=$(ps ax|grep demo_requests_login|grep -v grep|awk '{print $1}')
echo "old_pid=${old_pid}"
if [ -z $old_pid ];then
	echo 1
else

	echo 2
fi