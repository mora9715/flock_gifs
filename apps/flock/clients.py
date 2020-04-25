from python_http_client import Client
from urllib.parse import urlencode

from django.conf import settings


class PatchedClient(Client):
    # These are the supported HTTP verbs
    methods = {'delete', 'get', 'patch', 'post', 'put'}

    def __init__(self,
                 host,
                 request_headers=None,
                 version=None,
                 url_path=None,
                 append_slash=False,
                 timeout=None,
                 token=None):
        self.host = host
        self.request_headers = request_headers or {}
        self._version = version
        # _url_path keeps track of the dynamically built url
        self._url_path = url_path or []
        # APPEND SLASH set
        self.append_slash = append_slash
        self.timeout = timeout
        self.token = token

    def _build_url(self, query_params):
        url = ''
        count = 0
        while count < len(self._url_path):
            if count == 0:
                url += '/{}'.format(self._url_path[count])
            else:
                url += '.{}'.format(self._url_path[count])
            count += 1

        # add slash
        if self.append_slash:
            url += '/'

        if not query_params:
            query_params = {
                'token': self.token
            }
        else:
            query_params['token'] = self.token

        url_values = urlencode(sorted(query_params.items()), True)
        url = '{}?{}'.format(url, url_values)

        if self._version:
            url = self._build_versioned_url(url)
        else:
            url = '{}{}'.format(self.host, url)
        return url

    def _build_client(self, name=None):
        url_path = self._url_path + [name] if name else self._url_path
        return PatchedClient(
            host=self.host,
            version=self._version,
            request_headers=self.request_headers,
            url_path=url_path,
            append_slash=self.append_slash,
            timeout=self.timeout,
            token=self.token
        )


class FlockAPIClient:
    def __init__(self, timeout=10, endpoint=settings.FLOCK_ENDPOINT, port=443, protocol='https', version=1,
                 token=settings.FLOCK_TOKEN):
        self._timeout = timeout
        self._version = version
        self._port = port
        self._protocol = protocol
        self._endpoint = endpoint
        self._url = '{}://{}:{}'.format(self._protocol, self._endpoint, self._port)
        self._auth_t = token
        self._headers = {
            'content-type': "application/json",
        }
        self._build_client()

    def _build_client(self):
        self.client = PatchedClient(
            host=self._url,
            request_headers=self._headers,
            timeout=self._timeout,
            append_slash=True,
            version=self._version,
            token=self._auth_t
        )
