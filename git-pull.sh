#!/bin/bash

# Define the path to the config file
CONFIG_FILE="resources/config.json"
TEMP_FILE="config_backup.json"

# Copy the content of the config file to a temporary file
cp $CONFIG_FILE $TEMP_FILE

# Reset local changes
git reset --hard

# Pull the latest changes from the main branch
git pull origin main

# Restore the config file from the temporary file
cp $TEMP_FILE $CONFIG_FILE

# Remove the temporary file
rm $TEMP_FILE

echo "Config file has been backed up, git pull executed, and config file restored."