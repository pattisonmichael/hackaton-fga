# main.py
from __future__ import annotations
from fastapi import FastAPI, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
import openfga_sdk
import asyncio
from openfga_sdk import WriteRequest,TupleKeys,TupleKey
from openfga_sdk.api import open_fga_api
from openfga_sdk.credentials import Credentials, CredentialConfiguration
from typing import Any, Dict, List
import json
import re
from pydantic import BaseModel, Field
client_id = "0FStczHzsIMNEWcpTNd59vZfdy1Py9wk"
client_secret ="R1QGcNkdXs-FQjE-W5EYQhlkeU8MRM6VL9sRmbS7aWVBe8ulnL8x-9yf8YY5aUSr"
api_audience = "https://api.us1.fga.dev/"
api_issuer = "fga.us.auth0.com"

pattern_user_role = r"^/api/v2/users/(.*?)/roles$"
pattern_add_role = r"^/api/v2/roles/(.*?)/users$"
pattern_user_role_org = r"^/api/v2/organizations/(.*?)/members$"
pattern_role_perm = r"^/api/v2/roles/(.*?)/permissions$"
pattern_user_perm = r"^/api/v2/users/(.*?)/permissions$"

credentials = Credentials(method='client_credentials', configuration=CredentialConfiguration(client_id=client_id,client_secret=client_secret,api_audience=api_audience,api_issuer=api_issuer))

configuration = openfga_sdk.Configuration(
    api_scheme = 'https',
    api_host = 'api.us1.fga.dev',
    credentials = credentials,
    store_id = "01GZE886BK7NC959XNE0DJ7PZE",
)
configuration.debug=True

fga={}

async def api_setup():
    # Enter a context with an instance of the API client
    api_client = openfga_sdk.ApiClient(configuration)
        # Create an instance of the API class
    api_instance = open_fga_api.OpenFgaApi(api_client)
    return api_instance,api_client



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("startup with logstream")
    (api_instance,api_client) = await api_setup()
    fga["instance"]=api_instance
    fga["client"]=api_client
    yield
    # Clean up the ML models and release the resources
    print("shutdown")
    await api_client.close()


app = FastAPI(lifespan=lifespan)

# class Item(BaseModel):
#     name: str
#     description: str
#     price: float
# class LogData(BaseModel):
#     date: str
#     type: str
#     description: str
#     client_id: str
#     client_name: str
#     ip: str
#     user_agent: str
#     user_id: str
#     log_id: str
# class LogItem(BaseModel):
#     log_id: str
#     #
#     data: LogData
#     #data: Model
#     #{ "log_id": "",  "data": { "date": "2020-01-29T17:26:50.193Z", "type": "sapi", "description": "Create a log stream", "client_id": "", "client_name": "", "ip": "", "user_agent": "", "user_id": "", "log_id": "" }}    
# class Logs(BaseModel):
#     logs: list[LogItem]    
    
@app.get("/")
async def root():
    return "ok"
#@app.post("/items/")
#async def create_item(item: Item):
#    print("received")
#    return {"item": item}

@app.post("/log/")
#async def create_log(logs: Logs):
async def create_log(request: Request):
    print("logstream received")
    raw_data = await request.body()
    print (raw_data)
    try:
        data = json.loads(raw_data.decode("utf-8"))
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data"}

    for log in data["logs"]:
        if (log["data"]["type"] == "sapi"):
            print ("SAPI")
            method=log["data"]["details"]["request"]["method"]
            path=log["data"]["details"]["request"]["path"]
            body=log["data"]["details"]["request"]["body"]
            statuscode=log["data"]["details"]["response"]["statusCode"]
            match_user = re.match(pattern_user_role,path)
            match_org = re.match(pattern_user_role_org,path)
            match_role_perm = re.match(pattern_role_perm,path)
            match_user_perm = re.match(pattern_user_perm,path)
            #match_del = re.match(pattern_delete_role,path)
            if (method=="post" and match_user and statuscode==204):
                user=match_user.group(1)
                role=body["roles"][0]
                print ("Add role " + role)
                tuple = WriteRequest(
                    writes=TupleKeys(
                        tuple_keys=[
                            TupleKey(
                                user=f"user:{user}",
                                relation="member",
                                object=f"role:{role}",
                            ),
                        ],
                    ),
                    #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
                    print (response)
                except:
                    pass

            elif (method=="delete" and match_user and statuscode==204):
                #print ("remove role" +  match_del.group(1))
                user=match_user.group(1)
                role=body["roles"][0]
                print ("del role " + role)
                #{"user":"user:auth0|6113fe503ee95c0069d42db9","relation":"member","object":"role:rol_99SMnYdy6mILoSFJ"}
                tuple = WriteRequest(
                    deletes=TupleKeys(
                        tuple_keys=[
                            TupleKey(
                                user=f"user:{user}",
                                relation="member",
                                object=f"role:{role}",
                            ),
                        ],
                    ),
                    #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                )

                print (tuple)
                try:
                    api_instance = fga["instance"]
                    response=await api_instance.write(tuple)
                    print (response)
                except:
                    pass

            elif (method=="post" and match_org and statuscode==204):
                org=match_org.group(1)
                user=body["members"][0]
                print ("Add user to org " + org)
                tuple = WriteRequest(
                    writes=TupleKeys(
                        tuple_keys=[
                            TupleKey(
                                user=f"user:{user}",
                                relation="member",
                                object=f"org:{org}",
                            ),
                        ],
                    ),
                    #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
                    print (response)
                except:
                    pass
            elif (method=="delete" and match_org and statuscode==204):
                org=match_org.group(1)
                user=body["members"][0]
                print ("remove user from org " + org)
                tuple = WriteRequest(
                    deletes=TupleKeys(
                        tuple_keys=[
                            TupleKey(
                                user=f"user:{user}",
                                relation="member",
                                object=f"org:{org}",
                            ),
                        ],
                    ),
                    #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
                    print (response)
                except:
                    pass
            elif (method=="post" and match_role_perm and statuscode==201):
                role=match_role_perm.group(1)
                perms=body["permissions"]
                print ("Add perm to role " + role)
                for perm in perms:
                    print ("perm " + str(perm))
                    perm_name=perm["permission_name"].replace(":","_")
                    tuple = WriteRequest(
                        writes=TupleKeys(
                            tuple_keys=[
                                TupleKey(
                                    user=f"role:{role}#member",
                                    relation="has_permission",
                                    object=f"permission:{perm_name}",
                                ),
                            ],
                        ),
                        #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
                        print (response)
                    except:
                        pass
            elif (method=="delete" and match_role_perm and statuscode==204):
                role=match_role_perm.group(1)
                perms=body["permissions"]
                for perm in perms:
                    print ("remove perm from role " + str(perm))
                    perm_name=perm["permission_name"].replace(":","_")
                    tuple = WriteRequest(
                        deletes=TupleKeys(
                            tuple_keys=[
                                TupleKey(
                                    user=f"role:{role}#member",
                                    relation="has_permission",
                                    object=f"permission:{perm_name}",
                                ),
                            ],
                        ),
                        #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
                        print (response)
                    except:
                        pass

            elif (method=="post" and match_user_perm and statuscode==201):
                user=match_user_perm.group(1)
                perms=body["permissions"]
                print ("Add perm to user " + user)
                for perm in perms:
                    print ("perm " + str(perm))
                    perm_name=perm["permission_name"].replace(":","_")
                    tuple = WriteRequest(
                        writes=TupleKeys(
                            tuple_keys=[
                                TupleKey(
                                    user=f"user:{user}",
                                    relation="has_permission",
                                    object=f"permission:{perm_name}",
                                ),
                            ],
                        ),
                        #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
                        print (response)
                    except:
                        pass
            elif (method=="delete" and match_user_perm and statuscode==204):
                user=match_user_perm.group(1)
                perms=body["permissions"]
                for perm in perms:
                    print ("remove perm from user " + str(perm))
                    perm_name=perm["permission_name"].replace(":","_")
                    tuple = WriteRequest(
                        deletes=TupleKeys(
                            tuple_keys=[
                                TupleKey(
                                    user=f"user:{user}",
                                    relation="has_permission",
                                    object=f"permission:{perm_name}",
                                ),
                            ],
                        ),
                        #authorization_model_id="1uHxCSuTP0VKPYSnkq1pbb1jeZw",
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
                        print (response)
                    except:
                        pass
    return {"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
