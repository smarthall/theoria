from base import PollingProvider
import requests


class InvalidCredentialsError(Exception):
    pass


class iiNet(PollingProvider):
    REFRESH_INTERVAL = 30 * 60 # 30 minutes
    LOGIN_INTERVAL = 60 * 60 * 24 * 14 # 2 weeks
    API_ENDPOINT = 'https://toolbox.iinet.net.au/cgi-bin/api.cgi'

    def __init__(self, cache, username, password, *args, **kwargs):
        super(iiNet, self).__init__(
                refresh_interval=iiNet.REFRESH_INTERVAL,
                *args,
                **kwargs
        )

        self._cache = cache
        self._username = username
        self._password = password

        self._fetch_session_token()

    def _cache_key(self, ctype):
        data = {
                'user': self._username,
                'pass': self._password,
        }
        return 'netusage-iiNet-%s-%s' % (str(data), ctype)

    def _cache_get(self, ctype, default=None):
        return self._cache.get(self._cache_key(ctype), default)

    def _cache_store(self, ctype, item, ttl):
        self._cache.store_item(self._cache_key(ctype), item, ttl)

    def _fetch_session_token(self, fromcache=True):
        cache_key = 'session_tokens'
        if fromcache:
            tokens = self._cache_get(cache_key)

            if tokens is not None:
                return tokens

        response = requests.get(iiNet.API_ENDPOINT, {
            '_USERNAME': self._username,
            '_PASSWORD': self._password,
        })

        json = response.json()

        if json['success'] != 1:
            raise InvalidCredentialsError()

        token = json['token']
        s_token = ''
        for service in json['response']['service_list']:
            if 'Usage' in service['actions']:
                s_token = service['s_token']
                break

        tokens = (token, s_token)
        self._cache_store(cache_key, tokens, iiNet.LOGIN_INTERVAL)

        return tokens

    def _fetch_usage_data(self, fromcache=True):
        cache_key = 'usage_data'
        if fromcache:
            data = self._cache_get(cache_key)

            if data is not None:
                return data

        token, s_token = self._fetch_session_token(fromcache)

        response = requests.get(iiNet.API_ENDPOINT + '?Usage', {
            '_TOKEN': token,
            '_SERVICE': s_token,
        })

        result = response.json()['response']

        self._cache_store(cache_key, result, iiNet.REFRESH_INTERVAL)

        return result

    def provide(self):
        return self._fetch_usage_data()

