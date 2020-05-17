#!/bin/bash

usage ()
{
    echo 'Usage: ./host_server.sh'

    exit
}

echo ""
echo "New script, use with caution"
echo ""

branch="master"

git fetch
git checkout $branch
git pull

echo ""
echo "Done - Checked out latest $branch branch"
echo ""
echo "Hosting telegram server"
echo ""


python server.py
