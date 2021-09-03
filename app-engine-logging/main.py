"""
Demo for using Cloud Logging with the Bottle web framework on App Engine.

The google-cloud-logging library does not automatically add the trace
context to log records (it only does that for Flask and Django) so we
need a custom logging handler that can return the appropriate data.
"""
import logging

import bottle
import google.cloud.logging
from google.cloud.logging_v2.handlers._helpers import _parse_trace_span


def get_request_data_from_bottle():
    request = bottle.request
    # Values for X-Cloud-Trace-Context look like
    # 67be30409c0d133e413a3c43a60fdfb9/1219332184181630439;o=1
    trace_context = request.headers.get('X-Cloud-Trace-Context')
    trace_id, span_id = _parse_trace_span(trace_context)
    http_request = {
        'protocol': request.environ.get('SERVER_PROTOCOL'),
        'referer': request.headers.get('Referer'),
        'remoteIp': request.remote_addr,
        'requestMethod': request.method,
        'requestSize': request.content_length,
        'requestUrl': request.url,
        'userAgent': request.headers.get('User-Agent'),
    }

    return http_request, trace_id, span_id


class BottleHandler(google.cloud.logging.handlers.AppEngineHandler):
    def emit(self, record):
        http_request, trace_id, span_id = get_request_data_from_bottle()

        if trace_id:
            trace_id = f'projects/{self.project_id}/traces/{trace_id}'

        record.http_request = http_request
        record.trace = trace_id
        record.span_id = span_id

        return super().emit(record)


class LoggingClient(google.cloud.logging.Client):
    def get_default_handler(self, **kw):
        return BottleHandler(self, **kw)


LoggingClient().setup_logging()
app = bottle.Bottle()


@app.route('/')
def home():
    logging.info('OK!')
    bottle.response.content_type = 'text/plain'

    return 'OK'
