#!/bin/bash
#文件名
FILE_NAME='/home/wwwroot/www/log.txt'
#获取文件做后修改时间戳
a=`stat -c %Y  $FILE_NAME`
#格式化时间戳
formart_date=`date '+%Y-%m-%d %H:%M:%S' -d @$a`

b=`date +%s`

pid=`ps aux|grep demo_requests_login|grep -v grep|awk '{print $2}'`	
echo pid
if [ -z $pid ];then
	echo "进程不存在"
	#python3.8 /home/wwwroot/www/demo_requests_login.py	
else	
	if [ $[$b - $a] -gt 60 ];then		
		echo "间隔时间大于60秒"
		kill -9 $pid
		python3.8 /home/wwwroot/www/demo_requests_login.py
	else
		echo "间隔时间"
	    echo  $[$b - $a]
	fi
fi




