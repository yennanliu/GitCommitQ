#!/bin/sh
#################################################################
# SCRIPT RUN LOCAL postgresql
#################################################################
echo '>>>> stop postgresql'
brew services stop postgresql
echo '>>>> start postgresql'
brew services start postgresql
echo '>>>> creat DB'
sudo -u yennanliu createdb gitcommit  
echo '>>>> creat user'
sudo -u yennanliu createuser postgre_user
echo '>>>> creat user password'
# $ sudo -u yennanliu psql
# psql=# alter user postgre_user with encrypted password '0000';
echo '>>>> grant user db access'
# psql=# grant all privileges on database gitcommit  to postgre_user ;