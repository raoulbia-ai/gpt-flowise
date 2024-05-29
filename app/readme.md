cybcai.azurecr.io > value

Application (client) ID (see Overview pane) > value

docker_push_sp_secret > value

docker tag cybc_ai_app:latest cybcai.azurecr.io/cybc_ai_app:latest
docker push cybcai.azurecr.io/cybc_ai_app:latest

Authentication

`docker login cybcai.azurecr.io --username <username> --password <password>`

Replace <username> with your Azure Container Registry username, and <password> with your Azure Container Registry password.

If you don't know your Azure Container Registry username and password, you can retrieve them from the Azure portal:

1. Go to your Azure Container Registry resource.
2. Click on "Access keys" in the left-hand menu.
3. Here you can see your "Login server" (which is the registry name), "Username", and "Password".

After you've logged in, you should be able to push your Docker image to your Azure Container Registry.

Service Principal

Register the ACR with Azure Active Directory (AAD):

Open the Azure Portal and go to your Azure Container Registry.
In the left-hand menu, click on "Access keys" under "Settings".
Ensure "Admin user" is enabled. This is a temporary step to get immediate access

1. Create a Service Principal:

Go to "Azure Active Directory" in the Azure portal.
Navigate to "App registrations" and click "New registration".
Fill in the required details and click "Register".

2. Generate a Client Secret:

In the "Certificates & secrets" section of your service principal, click "New client secret".
Add a description and set the expiration period.
Click "Add" and copy the client secret value.

3. Assign Roles to the Service Principal:

Go to your Azure Container Registry in the Azure portal.
Navigate to "Access control (IAM)".
Click "+ Add" and select "Add role assignment".
Choose "AcrPull" or "AcrPush" based on your needs.
In the "Assign access to" dropdown, select "User, group, or service principal".
Click "Select members" and search for the service principal you created.
Select the service principal and click "Select", then "Review + assign".

After completing these steps, use the following command to log in to ACR:
`docker login <RegistryName>.azurecr.io --username <appId> --password-stdin <password>`

Replace <RegistryName>, <appId>, and <password> with your actual registry name, application (client) ID, and client secret, respectively.

curl -F "url=https://cybcai.azurewebsites.net/webhook" https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/setWebhook