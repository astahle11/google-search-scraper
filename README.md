
This is primarily for my own learning purposes and has no update/development committments. This is a basic implementation of google search result extracting with pagination. Output is stored in results.json. 

This script uses an AWS API gateway as a proxy. All requests are sent through the gateway. AWS hosts a large amount of servers and you are unlikely to end up using the same IP address consecutively; in this way, we are using it as a proxy.

I used this article to help set up an API gateway: https://medium.com/@chikim79/using-aws-api-gateway-as-proxy-to-another-http-endpoints-5271d78c5bd6

