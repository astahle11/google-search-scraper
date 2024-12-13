
This is primarily for my own learning purposes and has no update/development committments.

Basic implementation of google search result extracting with pagination. Output is stored in results.json. This script requires an AWS account set up to use an API gateway; the API gateway link is entered in the script, and all requests are sent through the gateway. Essentially, we're leveraging the AWS network in our favor. AWS hosts a large amount of servers and you are unlikely to end up using the same IP address among consecutive requests. 

I used this article to help set up an API gateway: https://medium.com/@chikim79/using-aws-api-gateway-as-proxy-to-another-http-endpoints-5271d78c5bd6

