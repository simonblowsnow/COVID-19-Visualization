#!/bin/bash
ps -ef | grep update_data.py |awk '{print $2}' |xargs kill -9
