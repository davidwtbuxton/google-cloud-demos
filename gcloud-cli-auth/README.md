Accessing Google APIs with local SDK credentials
================================================

Many Google APIs can be accessed by using App Engine's default application credentials.

This shows how to use the gcloud SDK to configure application default credentials, which can then be used either with Google's libraries, or to obtain an auth token for use with a tool such as curl.

Suppose your App Engine application needs to make requests to the sheets API. The code would look something like:

    import googleapiclient.discovery

    def get_spreadsheet_metadata(spreadsheet_id):
        service = googleapiclient.discovery.build("sheets", "v4")
        request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
        response = request.execute()

        return response

When running on App Engine, the google-auth library obtains an access token for the default service account, with the necessary authentication scopes, and adds the necessary "Authorization: Bearer [token]" header to the HTTP request.

When running in a local development environment, the google-auth library calls out to the gcloud command to obtain a token.

You need to configure the application default credentials for gcloud:

    SCOPES="https://www.googleapis.com/auth/spreadsheets.readonly,https://www.googleapis.com/auth/cloud-platform.readonly"
    PROJECT="my-gcp-project-example"
    gcloud auth application-default login --scopes "$SCOPES"
    gcloud auth application-default set-quota-project "$PROJECT"
