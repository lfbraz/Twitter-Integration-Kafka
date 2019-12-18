# Create project
func init TwitterIntegrationFunction --python
cd TwitterIntegrationFunction

# Create a function
func new --name HttpTrigger --template "HTTP trigger"

# Deploy your function
## func azure functionapp publish <YOUR_AZURE_APPNAME>
func azure functionapp publish TwitterIntegrationFunction
