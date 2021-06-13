Finding the Cloud Tasks location from App Engine
================================================

When using the Google [Cloud Tasks][cloudtasks] API you need to [specify the project ID and location][cloudtasks-location]. It would be good to not hard-code these for your app, and instead determine the values when the application starts or on first using the API.

This code is for the blog post at  https://buxty.com/b/2021/06/finding-the-cloud-tasks-location/

Included is a complete (as of June 2021) list of the App Engine short region code prefixes.

App Engine region       | Short prefix   |
------------------------|----------------|
asia-east1              | zde            |
asia-east2              | n              |
asia-northeast1         | b              |
asia-northeast2         | u              |
asia-northeast3         | v              |
asia-south1             | j              |
asia-southeast1         | zas            |
asia-southeast2         | zet            |
australia-southeast1    | f              |
europe-central2         | zlm            |
europe-west             | e              |
europe-west2            | g              |
europe-west3            | h              |
europe-west6            | o              |
northamerica-northeast1 | k              |
southamerica-east1      | i              |
us-central              | s              |
us-east1                | p              |
us-east4                | d              |
us-west1                | zuw            |
us-west2                | m              |
us-west3                | zwm            |
us-west4                | zwn            |

[cloudtasks]: https://cloud.google.com/tasks
[cloudtasks-location]: https://cloud.google.com/tasks/docs/creating-appengine-tasks
