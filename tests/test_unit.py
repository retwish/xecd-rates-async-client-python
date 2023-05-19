from xecd_rates_client import XecdClient
import unittest
import aiohttp
from unittest.mock import MagicMock
import json

with open('tests/data/testdata.json') as json_data:
    data = json.load(json_data)


class XecdClientUnitTest(unittest.IsolatedAsyncioTestCase):

    def mock_session(self, data, value):
        mock = aiohttp.ClientSession
        mock.get = MagicMock()
        mock.get.return_value.__aenter__.return_value.status = value
        mock.get.return_value.__aenter__.return_value.json.return_value = data

    async def asyncSetUp(self):
        self.xecd = XecdClient('accountId', 'apiKey')

    async def testAccountInfo(self):
        self.mock_session(data=data["fakeAccountInfo"], value=200)
        self.assertEqual(data["fakeAccountInfo"], await self.xecd.account_info())

    async def testCurrencies(self):
        self.mock_session(data=data["fakeCurrencies"], value=200)
        self.assertEqual(data["fakeCurrencies"], await self.xecd.currencies())

    async def testConvertFrom(self):
        self.mock_session(data=data["fakeConvertFrom"], value=200)
        self.assertEqual(data["fakeConvertFrom"], await self.xecd.convert_from("EUR", "CAD", 55))

    async def testConvertTo(self):
        self.mock_session(data=data["fakeConvertTo"], value=200)
        self.assertEqual(data["fakeConvertTo"], await self.xecd.convert_to("RUB", "CAD", 55))

    async def testHistoricRate(self):
        self.mock_session(data=data["fakeHistoricRate"], value=200)
        self.assertEqual(data["fakeHistoricRate"], await self.xecd.historic_rate("2016-12-25", "12:34", "EUR", "CAD", 55))

    async def testHistoricRatePeriod(self):
        self.mock_session(data=data["fakeHistoricRatePeriod"], value=200)
        self.assertEqual(data["fakeHistoricRatePeriod"], await self.xecd.historic_rate_period(55, "EUR", "RUB", "2016-02-28T12:00", "2016-03-03T12:00"))

    async def testMonthlyAverage(self):
        self.mock_session(data=data["fakeMonthlyAverage"], value=200)
        self.assertEqual(data["fakeMonthlyAverage"], await self.xecd.monthly_average(55, "CAD", "EUR", 2017, 5))
