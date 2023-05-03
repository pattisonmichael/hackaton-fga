import openfga_sdk
import asyncio
from openfga_sdk.api import open_fga_api
from openfga_sdk.credentials import Credentials, CredentialConfiguration
api_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino4TzF1WEpUMkZ5UHRqZ3RmZDZoMiJ9.eyJodHRwczovL2ZnYS5kZXYvY2xhaW1zL3N0b3JlX3RpZXIiOiJmcmVlIiwiaHR0cHM6Ly9mZ2EuZGV2L2NsYWltcy9jdXN0b21lcl9pZCI6IjAxR1pFODg1N1JSMFpSN0U2REJIUlFBOUVNIiwiaHR0cHM6Ly9mZ2EuZGV2L2NsYWltcy9zdG9yZV9pZCI6IjAxR1pFODg2Qks3TkM5NTlYTkUwREo3UFpFIiwiaXNzIjoiaHR0cHM6Ly9mZ2EudXMuYXV0aDAuY29tLyIsInN1YiI6IjBGU3Rjekh6c0lNTkVXY3BUTmQ1OXZaZmR5MVB5OXdrQGNsaWVudHMiLCJhdWQiOiJodHRwczovL2FwaS51czEuZmdhLmRldi8iLCJpYXQiOjE2ODMwOTU1MTgsImV4cCI6MTY4MzE4MTkxOCwiYXpwIjoiMEZTdGN6SHpzSU1ORVdjcFROZDU5dlpmZHkxUHk5d2siLCJzY29wZSI6InJlYWQ6dHVwbGVzIHdyaXRlOnR1cGxlcyBjaGVjazp0dXBsZXMgZXhwYW5kOnR1cGxlcyByZWFkOmF1dGhvcml6YXRpb25fbW9kZWxzIHdyaXRlOmF1dGhvcml6YXRpb25fbW9kZWxzIHJlYWQ6YXNzZXJ0aW9ucyB3cml0ZTphc3NlcnRpb25zIHJlYWQ6Y2hhbmdlcyBsaXN0Om9iamVjdHMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.G2O8Drp6YD2VEOtHTQlHncFzGVs5F_HUBxzlvjRKYijjEgiZN2r7zXzUmMAej716afr-I3PL2A9yFBMivjXSkzmzeDalFEbJWre3LFsH7Pr1Cx1GtqPfwyGrRyoy12A0nC_xU6KpVwVVMv5SRzd8fxouekxtjfCM0iBZH3nlvjxBJzugwTIOIeNj0XV3a8yVb2yr0acJgyb_0t--g27X1FlnkvM26FN7qJ01Wj9Co-10B6-N0LKJ9VbMLcVeMjOvatYVR0oE3PrMCndCDzK8QGd5fiCbgA5ckIdLmwogUj-4hfUE70UIyBMvYxW3vXarr7dcuZqt6Tb93ua0F3orsQ"
credentials = Credentials(method='api_token', configuration=CredentialConfiguration(api_token=api_token))
configuration = openfga_sdk.Configuration(
    api_scheme = 'https',
    api_host = 'fga.us.auth0.com',
    credentials = credentials,
    store_id = "01GZE886BK7NC959XNE0DJ7PZE"
)
api_instance=None
api_client=None
async def api_setup():
    # Enter a context with an instance of the API client
    async with openfga_sdk.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        return open_fga_api.OpenFgaApi(api_client)


# Get a store
async def get_store():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)

    response = await api_instance.get_store()
    print(response)
    # response = Store({"id": "01FQH7V8BEG3GPQW93KTRFR8JB", "name": "FGA Demo Store", "created_at": "2022-01-01T00:00:00.000Z", "updated_at": "2022-01-01T00:00:00.000Z"})
    await api_client.close()

async def mainasync():
    async with openfga_sdk.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = open_fga_api.OpenFgaApi(api_client)
        response = await api_instance.get_store()
        print(response)
        # response = Store({"id": "01FQH7V8BEG3GPQW93KTRFR8JB", "name": "FGA Demo Store", "created_at": "2022-01-01T00:00:00.000Z", "updated_at": "2022-01-01T00:00:00.000Z"})
        await api_client.close()

def main():
    
    asyncio.run(mainasync())


if __name__ == "__main__":
    main()