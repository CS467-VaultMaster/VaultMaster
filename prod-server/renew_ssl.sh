#!/bin/bash

# Script to renew SSL certificates for the domain 'vaultmaster.site'. 
# Runs weekly; updates if at least 60 days have passed (renewal needed before 90 days)
# Cronjob looks like so: '0 0 * * 1 /home/ec2-user/VaultMaster/prod-server/renew_ssl.sh'

LAST_RUN_FILE="/home/ec2-user/VaultMaster/prod-server/last_run_date.txt"
CURRENT_DATE=$(date +%s)

# Set last run to 0 (in epoch time) if no file found
if [[ -f "$LAST_RUN_FILE" ]]; then
    LAST_RUN_DATE=$(cat "$LAST_RUN_FILE")
else
    LAST_RUN_DATE=0
fi

# Get interval since last successful update
TIME_SINCE_RUN=$(( (CURRENT_DATE - LAST_RUN_DATE) / 86400 ))

# If it's been >60 days, we can renew certs via LetsEncrypt
if [[ $TIME_SINCE_RUN -ge 60 ]]; then
    getssl vaultmaster.site

    # Reset counter only on success
    if [[ $? -eq 0 ]]; then
        echo "$CURRENT_DATE" > "$LAST_RUN_FILE"
    fi
fi