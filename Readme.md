Invoke lambda  from terminal

1. Add json with request data.
``
{"queryStringParameters":{"title":"Wiki"}}
``

or 
``
{"queryStringParameters":{"title":"Washington,_D.C."}}
``
etc.

2. 
Run from the project dir the command

`-- function` is a name of handler function from serverless.yaml

`-p` path to request data file.

``
serverless invoke --function wikiPageInfo -p req_data.json`` 

Response example 
```shell script
(proj_env) ➜  untitled1 serverless invoke --function wikiPageInfo -p req_data.json
{
    "statusCode": 200,
    "body": "{\"latest_update_time\": \"2019-10-05T19:18:00\", \"number_updates_last_month\": 2}"
}

```


The same can be checked online by calling url :

https://sd0h0uwh64.execute-api.us-east-1.amazonaws.com/dev/ping?title=Wiki   

with `title`- parameter for different pages. 

or 


https://sd0h0uwh64.execute-api.us-east-1.amazonaws.com/dev/ping
