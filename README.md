Description
-------------
This is a docker image to build imgpoller container.

Prerequisites
-------------
- Pre-Required image: ubuntu:18.04
- Required Container: Vault. The access tokens for GIT and Slack are taken from the environment variables, these environment variables refer the vault secret for the values. So, the vault container should be set-up first.
- Follow the steps to create access token for Git.
     
	1. Open your github account and go to settings under the profile section on the top right corner.
	2. Now select Developer settings then Personal Access Tokens from the next windows
	3. Then select sufficient privileges and generate token. Secure this token in the Vault as variable GIT_ACCESS_TOKEN
- Follow the steps to create a slack app to receive build notifications from imgpoller.
   1. Go to https://api.slack.com/ and login to your slack account. 
   2. Click on start building
   3. Click on "Create a Slack App" and and create yourown app with suitable name.
   4. Now add "Incoming webhook" --> "Activate Incoming Webhooks" to "ON" --> "Add new webhook to workspace" --> Select the Channel
   5. Now check "OAuth & Permissions" tab for access token for the newly created App. (Add scopes if needed)
   6. Secure this token in the Vault as variable SLACK_TOKEN

Environment variables
------------------------
- Sample env file


    `#source /root/imgpoller.conf`

    `ENV=' -e VAULT_ADDR=https://vault:8200'`

    `ENV+=' -e VAULT_ROLE_ID='$VAULT_ROLE_ID`

    `ENV+=' -e VAULT_SECRET_ID='$VAULT_SECRET_ID`

    `ENV+=' -e VAULT_APPROLE='$VAULT_APPROLE`

    `ENV+=' -e GIT_BASE_URL=https://api.github.com -e GIT_POLL_INTERVAL=60 -e GIT_BASE_URL=https://api.github.com  -e USER_ID=1000'`

    `ENV+=' -e GIT_ACCESS_TOKEN='VAULT:GIT_ACCESS_TOKEN`

    `ENV+=' -e GIT_REPOS=AncyPaul/newnew/master:/root/newnew'`

    `ENV+=' -e SLACK_TOKEN='VAULT:SLACK_TOKEN`

    `ENV+=' -e SLACK_CHANNEL=business'`

    `ENV+=' -e SLACK_ICON_URL=https://www.ecloudcontrol.com/wp-content/uploads/2020/09/appz-images-icon-v2.png'`

    `ENV+=' -e SLACK_USER=appz-bot'`

    `ENV+=' -e APPZ_ENV=s2shape-dev'`

- GIT_ACCESS_TOKEN is the token from github
- GIT_REPOS is the location of remote repo
- SLACK_TOKEN is the token from slack
- SLACK_CHANNEL is the slack channel name
- SLACK_ICON_URL is the url of the image to set the slack icon
- SLACK_USER is the name of bot user displayed on each notification
