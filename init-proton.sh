#!/bin/bash
# Init script to create and grant privileges to pulsebot user

# Wait for Proton to be ready
echo "Waiting for Proton to start..."
sleep 5

# Run privilege grants using proton admin user
echo "Creating pulsebot user and granting privileges..."

# Create user pulsebot with no password
proton-client --user=proton --password='proton@t+' --query="CREATE USER IF NOT EXISTS pulsebot IDENTIFIED WITH plaintext_password BY '';"

# Grant CREATE DATABASE and all privileges on pulsebot database to pulsebot user
proton-client --user=proton --password='proton@t+' --query="GRANT CREATE DATABASE ON *.* TO pulsebot;"
proton-client --user=proton --password='proton@t+' --query="GRANT ALL ON pulsebot.* TO pulsebot;"

echo "User created and privileges granted successfully!"

# Verify grants
echo "Verifying grants for pulsebot user:"
proton-client --user=proton --password='proton@t+' --query="SHOW GRANTS FOR pulsebot;"
