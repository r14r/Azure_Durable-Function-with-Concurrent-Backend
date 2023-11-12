#!/usr/local/bin/bash

export ENV_NAME=Azure
export HOME=/Users/Shared/CLOUD/Programmier-Workshops/Kurse/$ENV_NAME
export HERE=$PWD

. venv vscode     init
. venv python     init 3.11

export AZURE_CONFIG_DIR=$HERE/.azure
echo "environment for azure     : AZURE_CONFIG_DIR ${AZURE_CONFIG_DIR/$HOME/<HOME>}"

