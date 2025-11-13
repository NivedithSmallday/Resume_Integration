import os
import webbrowser
import msal

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

def get_access_token(application_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority='https://login.microsoftonline.com/consumers/'
    )

    refresh_token = None
    if os.path.exists('refresh_token.txt'):
        with open('refresh_token.txt', 'r') as file:
            refresh_token = file.read().strip()

    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
    else:
        auth_url = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_url)
        code = input("Enter the authorization code: ")
        if not code:
            raise ValueError("Authorization code is empty")
        token_response = client.acquire_token_by_authorization_code(code=code, scopes=scopes)

    if 'access_token' in token_response:
        if 'refresh_token' in token_response:
            with open('refresh_token.txt', 'w') as file:
                file.write(token_response['refresh_token'])
        return token_response['access_token']
    else:
        raise Exception("Failed to acquire access token: " + str(token_response))
