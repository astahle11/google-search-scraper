
This is primarily for my own learning purposes and has no update/development committments.

Basic implementation of google search result extracting with pagination. Output is stored in results.json. This script requires an AWS account set up to use an API gateway; the API gateway link is entered in the script, and all requests are sent through the gateway. In this way, the API is used as a proxy to avoid exceeding request rate limits - the idea behind this being that AWS hosts a large amount of servers, and you are unlikely to end up using the same IP address among multiple requests. 

This article provides instructions on how to set up an API gateway: https://medium.com/@chikim79/using-aws-api-gateway-as-proxy-to-another-http-endpoints-5271d78c5bd6

