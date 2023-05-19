from aiohttp import ClientSession, BasicAuth


class XecdApiUri(object):
    CURRENCIES_REQUEST_URI = 'currencies.json'
    ACCOUNT_INFO_REQUEST_URI = 'account_info.json'
    CONVERT_FROM_REQUEST_URI = 'convert_from.json'
    CONVERT_TO_REQUEST_URI = 'convert_to.json'
    HISTORIC_RATE_REQUEST_URI = 'historic_rate.json'
    HISTORIC_RATE_PERIOD_REQUEST_URI = 'historic_rate/period.json'
    MONTHLY_AVERAGE_REQUEST_URI = 'monthly_average.json'


class XecdClient(XecdApiUri):
    """XECD REST API Client"""

    def __init__(self, account_id, api_key, options={}):
        self.options = {
            'auth': {
                'user': account_id,
                'password': api_key
            },
            'baseUrl': 'https://xecdapi.xe.com/v1/',
            'qs': {}
        }
        self.options.update(options)

    async def _send(self, ops):
        self.options.update(ops)
        # cached for debugging purposes
        url = self.options["url"]
        username = self.options['auth']['user']
        password = self.options['auth']['password']
        qs = self.options['qs']
        async with ClientSession(auth=BasicAuth(username, password)) as session:
            async with session.get(url, params=qs) as resp:
                data = await resp.json()
                return data

    async def account_info(
        self,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.ACCOUNT_INFO_REQUEST_URI
        }
        ops.update(options)
        return await self._send(ops)

    async def currencies(
        self,
        obsolete=False,
        language="en",
        iso=['*'],
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.CURRENCIES_REQUEST_URI,
            'qs': {
                'obsolete': True if obsolete else False,
                'language': language,
                'iso': ','.join(iso)  # format: abc,def,ghi
            }
        }
        ops.update(options)
        return await self._send(ops)

    async def convert_from(
        self,
        from_currency="USD",
        to_currency="*",
        amount=1,
        obsolete=False,
        inverse=False,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.CONVERT_FROM_REQUEST_URI,
            'qs': {
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'obsolete': True if obsolete else False,
                'inverse': True if inverse else False
            }
        }
        ops.update(options)
        return await self._send(ops)

    async def convert_to(
        self,
        to_currency="USD",
        from_currency="*",
        amount=1,
        obsolete=False,
        inverse=False,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.CONVERT_TO_REQUEST_URI,
            'qs': {
                'to': to_currency,
                'from': from_currency,
                'amount': amount,
                'obsolete': True if obsolete else False,
                'inverse': True if inverse else False
            }
        }
        ops.update(options)
        return await self._send(ops)

    async def historic_rate(
        self,
        date,
        time,
        from_currency="USD",
        to_currency="*",
        amount=1,
        obsolete=False,
        inverse=False,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.HISTORIC_RATE_REQUEST_URI,
            'qs': {
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'date': date,
                'time': time,
                'obsolete': True if obsolete else False,
                'inverse': True if inverse else False
            }
        }
        ops.update(options)
        return await self._send(ops)

    async def historic_rate_period(
        self,
        amount=1,
        from_currency="USD",
        to_currency="*",
        start_timestamp=None,
        end_timestamp=None,
        interval="DAILY",
        obsolete=False,
        inverse=False,
        page=1,
        per_page=30,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.HISTORIC_RATE_PERIOD_REQUEST_URI,
            'qs': {
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'start_timestamp': start_timestamp if (start_timestamp is not None) else None,
                'end_timestamp': end_timestamp if (end_timestamp is not None) else None,
                'interval': interval,
                'obsolete': True if obsolete else False,
                'inverse': True if inverse else False,
                'page': page,
                'per_page': per_page

            }
        }
        ops.update(options)
        return await self._send(ops)

    async def monthly_average(
        self,
        amount=1,
        from_currency="USD",
        to_currency="*",
        year=None,
        month=None,
        obsolete=False,
        inverse=False,
        options={}
    ):
        ops = {
            'url': self.options['baseUrl'] + self.MONTHLY_AVERAGE_REQUEST_URI,
            'qs': {
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'year': year,
                'month': month,
                'obsolete': True if obsolete else False,
                'inverse': True if inverse else False
            }
        }
        ops.update(options)
        return await self._send(ops)
