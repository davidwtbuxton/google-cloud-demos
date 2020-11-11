Notes for using the gcloud CLI
==============================

- Installing the Google Cloud SDK: https://cloud.google.com/sdk/docs/install
- gcloud CLI overview: https://cloud.google.com/sdk/gcloud
- gcloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- gcloud CLI cheat sheet: https://cloud.google.com/sdk/docs/cheatsheet


These examples use environment variables in some places.

- `$PROJECT` - your GCP project ID, e.g. "dbux-test".


IAM (Identity & Access Management)
----------------------------------

Check what permissions have been granted on your project to whom.

How-to guides for IAM: https://cloud.google.com/iam/docs/how-to


- List default roles.

        gcloud iam roles list --format="table(name,title,description)"

- List the permissions granted by a role.

        gcloud iam roles describe roles/appengine.appAdmin

- List who has what role on a project.

        gcloud projects get-iam-policy $PROJECT --format="table(bindings.role,bindings.members)" --flatten="bindings[].members"

- Add a member with a role on a project.

        gcloud projects add-iam-policy-binding $PROJECT --member="user:david@example.com"  --role="roles/editor"

- Remove a member's role on a project.

        gcloud projects remove-iam-policy-binding $PROJECT --member="user:david@example.com" --role="roles/editor"


Services (APIs)
---------------

The many parts of GCP are divided into services, each of which is controlled by one or more APIs. Some services are enabled by default, others must be explicitly enabled before they can be used.

- List all available services.
- Show which services are enabled or disabled on a project.
- Enable a service on a project.
- Disable a service on a project.


App Engine
----------

- Enable the App Engine service for a project.


Debug / meta
------------

The gcloud CLI has a "meta" command for peeking under the covers. This can be useful when you think you have hit a bug in the CLI itself, or for exploring how the command-line arguments are translated to Google Cloud Platform API requests.

Show the documentation for the "meta" command:

    gcloud meta --help
