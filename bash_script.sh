mysql -uroot -p'$3cureUS' -h db -e
"create user 'www'@'%' identified by '$3cureUS';
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%';"