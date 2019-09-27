#!/bin/sh
#################################################################
# SCRIPT RUN LOCAL postgresql
#################################################################
echo '>>>> stop postgresql'
brew services stop postgresql
echo '>>>> start postgresql'
brew services start postgresql