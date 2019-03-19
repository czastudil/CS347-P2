#!/usr/bin/env bash
env_dir="djangoenv"
dependencies=( "Django" "psycopg2" )

pip3 install --user virtualenv
virtualenv --python=python3 "$env_dir"

pip="${env_dir}/bin/pip"
"$pip" install --upgrade pip setuptools

for dep in "${dependencies[@]}"; do
    "$pip" install "$dep"
done
