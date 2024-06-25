import requests as r
import certifi

print(certifi.where())

r.get('https://google.com', verify='C:\\Users\\astahle\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\certifi\\cacert.pem')