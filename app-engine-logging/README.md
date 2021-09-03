Cloud Logging and the Bottle web framework
==========================================

This is a demo for using Cloud Logging with the [Bottle web framework][bottle] on App Engine.

The google-cloud-logging library does not automatically add the trace context to log records (it only does that for Flask and Django) so we need a custom logging handler that can return the appropriate data.

[bottle]: https://bottlepy.org
