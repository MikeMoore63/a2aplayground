#!/usr/bin/env bash
# This script installs the necessary dependencies for the hacky agent environment.
set -x
echo "Agent Engine build over here"
env
cat /etc/os-release
python --version
wget -vO - https://google.com
echo "Agent Engine build install script done"