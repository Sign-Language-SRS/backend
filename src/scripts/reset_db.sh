#!/bin/sh
python script_exec.py --reset_db && flask db upgrade
