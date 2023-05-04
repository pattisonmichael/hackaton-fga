# main.py
from __future__ import annotations
from fastapi import FastAPI, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
import openfga_sdk
import os
from dotenv import load_dotenv
from openfga_sdk import WriteRequest,TupleKeys,TupleKey
from openfga_sdk.api import open_fga_api
from openfga_sdk.credentials import Credentials, CredentialConfiguration
from typing import Any, Dict, List
import json
import re
from pydantic import BaseModel, Field

load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
api_audience = os.environ.get("API_AUDIENCE")
api_issuer = os.environ.get("API_ISSUER")


pattern_user_role = r"^/api/v2/users/(.*?)/roles$"
pattern_add_role = r"^/api/v2/roles/(.*?)/users$"
pattern_user_role_org = r"^/api/v2/organizations/(.*?)/members$"
pattern_role_perm = r"^/api/v2/roles/(.*?)/permissions$"
pattern_user_perm = r"^/api/v2/users/(.*?)/permissions$"

credentials = Credentials(method='client_credentials', configuration=CredentialConfiguration(client_id=client_id,client_secret=client_secret,api_audience=api_audience,api_issuer=api_issuer))

configuration = openfga_sdk.Configuration(
    api_scheme = 'https',
    api_host = os.environ.get("API_HOST"),
    credentials = credentials,
    store_id = os.environ.get("STORE_ID"),
)
#configuration.debug=True

fga={}

async def api_setup():
    # Enter a context with an instance of the API client
    
    api_client = openfga_sdk.ApiClient(configuration)
        # Create an instance of the API class
    api_instance = open_fga_api.OpenFgaApi(api_client)
    return api_instance,api_client



@asynccontextmanager
async def lifespan(app: FastAPI):

    (api_instance,api_client) = await api_setup()
    fga["instance"]=api_instance
    fga["client"]=api_client
    yield
   
    await api_client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return "ok"

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
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
                except:
                    pass

            elif (method=="delete" and match_user and statuscode==204):
                user=match_user.group(1)
                role=body["roles"][0]
                print ("del role " + role)
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
                )

                print (tuple)
                try:
                    api_instance = fga["instance"]
                    response=await api_instance.write(tuple)
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
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
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
                )
                print (tuple)
                api_instance = fga["instance"]
                try:
                    response=await api_instance.write(tuple)
                except:
                    pass

            elif (method=="post" and match_role_perm and statuscode==201):
                role=match_role_perm.group(1)
                perms=body["permissions"]
                for perm in perms:
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
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
                    except:
                        pass

            elif (method=="delete" and match_role_perm and statuscode==204):
                role=match_role_perm.group(1)
                perms=body["permissions"]
                for perm in perms:
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
                    )
                    print (tuple)
                    api_instance = fga["instance"]
                    try:
                        response=await api_instance.write(tuple)
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
