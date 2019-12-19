# Azure Functions configurations
## Create project
func init TwitterIntegrationFunction --python
cd TwitterIntegrationFunction

## Create a function
func new --name HttpTrigger --template "HTTP trigger"

## Deploy your function
### func azure functionapp publish <YOUR_AZURE_APPNAME>
func azure functionapp publish TwitterIntegrationFunction

## Create a topic "twitter_data" in Kafka inside docker
docker-compose exec kafka  \
kafka-topics --create --topic twitter_data --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

# Twitter REST API configuration

# Get your bearer token
BEARER_TOKEN=$(curl -u '<CONSUMER API KEY>:<CONSUMER API SECRET>' 'https://api.twitter.com/oauth2/token' --data 'grant_type=client_credentials' | grep -o 'access_token":".*[^"}]' | cut -b16-)

curl -X GET -H "Authorization: Bearer $BEARER_TOKEN"  "https://api.twitter.com/labs/1/tweets?ids=1067094924124872705&format=detailed"

