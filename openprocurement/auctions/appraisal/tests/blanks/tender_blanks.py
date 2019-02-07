# -*- coding: utf-8 -*-
from copy import deepcopy
from uuid import uuid4
from datetime import timedelta, datetime
from iso8601 import parse_date
import pytz

from isodate import parse_datetime

from openprocurement.auctions.core.tests.base import JSON_RENDERER_ERROR
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE, TZ, get_now, calculate_business_date
)

from openprocurement.auctions.appraisal.tests.base import TEST_ROUTE_PREFIX
from openprocurement.auctions.appraisal.models import AppraisalAuction

# AppraisalAuctionTest


def create_role(self):
    fields = set([
        'awardCriteriaDetails', 'awardCriteriaDetails_en', 'awardCriteriaDetails_ru',
        'description', 'description_en', 'description_ru', 'tenderAttempts',
        'features', 'guarantee', 'hasEnquiries', 'items', 'lots', 'minimalStep', 'mode',
        'procurementMethodRationale', 'procurementMethodRationale_en', 'procurementMethodRationale_ru',
        'procurementMethodType', 'procuringEntity',
        'submissionMethodDetails', 'submissionMethodDetails_en', 'submissionMethodDetails_ru',
        'title', 'title_en', 'title_ru', 'value', 'auctionPeriod', 'lotIdentifier',
        'auctionParameters', 'bankAccount', 'registrationFee',
    ])
    if SANDBOX_MODE:
        fields.add('procurementMethodDetails')
    self.assertEqual(set(self.auction._fields) - self.auction._options.roles['create'].fields, fields)


def edit_role(self):
    fields = set([
        'bankAccount', 'description', 'title', 'title_en', 'title_ru',
        'minimalStep', 'items', 'tenderAttempts', 'description', 'description_en',
        'description_ru', 'registrationFee', 'guarantee', 'hasEnquiries', 'lotIdentifier',
        'features', 'value'
    ])
    role = self.auction._options.roles['edit_active.tendering_during_rectification_period']

    if SANDBOX_MODE:
        fields.add('procurementMethodDetails')

    if role.function.__name__ == 'blacklist':
        self.assertEqual(set(self.auction._fields) - role.fields, fields)
    else:
        self.assertEqual(set(self.auction._fields).intersection(role.fields), fields)


# AppraisalAuctionResourceTest


def create_auction_invalid(self):
    request_path = '/auctions'
    response = self.app.post(request_path, 'data', status=415)
    self.assertEqual(response.status, '415 Unsupported Media Type')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description':
            u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
    ])

    response = self.app.post(
        request_path, 'data', content_type='application/json', status=422)
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        JSON_RENDERER_ERROR
    ])

    response = self.app.post_json(request_path, 'data', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'not_data': {}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': []}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': {'procurementMethodType': 'invalid_value'}}, status=415)
    self.assertEqual(response.status, '415 Unsupported Media Type')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'procurementMethodType is not implemented', u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': {'invalid_field': 'invalid_value', 'procurementMethodType': self.initial_data['procurementMethodType']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Rogue field', u'location':
            u'body', u'name': u'invalid_field'}
    ])

    response = self.app.post_json(request_path, {'data': {'value': 'invalid_value', 'procurementMethodType': self.initial_data['procurementMethodType']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [
            u'Please use a mapping for this field or Value instance instead of unicode.'], u'location': u'body', u'name': u'value'}
    ])

    response = self.app.post_json(request_path, {'data': {'procurementMethod': 'invalid_value', 'procurementMethodType': self.initial_data['procurementMethodType']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertIn({u'description': [u"Value must be one of ['open', 'selective', 'limited']."], u'location': u'body', u'name': u'procurementMethod'}, response.json['errors'])
    #self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'tenderPeriod'}, response.json['errors'])
    # self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'minimalStep'}, response.json['errors'])
    #self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'enquiryPeriod'}, response.json['errors'])
    self.assertIn({u'description': [u'This field is required.'], u'location': u'body', u'name': u'value'}, response.json['errors'])

    response = self.app.post_json(request_path, {'data': {'enquiryPeriod': {'endDate': 'invalid_value'}, 'procurementMethodType': self.initial_data['procurementMethodType']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'endDate': [u"Could not parse invalid_value. Should be ISO8601."]}, u'location': u'body', u'name': u'enquiryPeriod'}
    ])

    response = self.app.post_json(request_path, {'data': {'enquiryPeriod': {'endDate': '9999-12-31T23:59:59.999999'}, 'procurementMethodType': self.initial_data['procurementMethodType']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'endDate': [u'date value out of range']}, u'location': u'body', u'name': u'enquiryPeriod'}
    ])

    self.initial_data['tenderPeriod'] = self.initial_data.pop('auctionPeriod')
    response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    self.initial_data['auctionPeriod'] = self.initial_data.pop('tenderPeriod')
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'startDate': [u'This field is required.']}, u'location': u'body', u'name': u'auctionPeriod'}
    ])

    self.initial_data['tenderPeriod'] = {'startDate': '2014-10-31T00:00:00', 'endDate': '2014-10-01T00:00:00'}
    response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    self.initial_data.pop('tenderPeriod')
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'startDate': [u'period should begin before its end']}, u'location': u'body', u'name': u'tenderPeriod'}
    ])

    #data = self.initial_data['tenderPeriod']
    #self.initial_data['tenderPeriod'] = {'startDate': '2014-10-31T00:00:00', 'endDate': '2015-10-01T00:00:00'}
    #response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    #self.initial_data['tenderPeriod'] = data
    #self.assertEqual(response.status, '422 Unprocessable Entity')
    #self.assertEqual(response.content_type, 'application/json')
    #self.assertEqual(response.json['status'], 'error')
    #self.assertEqual(response.json['errors'], [
        #{u'description': [u'period should begin after enquiryPeriod'], u'location': u'body', u'name': u'tenderPeriod'}
    #])

    now = get_now()
    #self.initial_data['awardPeriod'] = {'startDate': now.isoformat(), 'endDate': now.isoformat()}
    #response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    #del self.initial_data['awardPeriod']
    #self.assertEqual(response.status, '422 Unprocessable Entity')
    #self.assertEqual(response.content_type, 'application/json')
    #self.assertEqual(response.json['status'], 'error')
    #self.assertEqual(response.json['errors'], [
        #{u'description': [u'period should begin after tenderPeriod'], u'location': u'body', u'name': u'awardPeriod'}
    #])

    data = self.initial_data['auctionPeriod']
    self.initial_data['auctionPeriod'] = {'startDate': (now + timedelta(days=15)).isoformat(), 'endDate': (now + timedelta(days=15)).isoformat()}
    self.initial_data['awardPeriod'] = {'startDate': (now + timedelta(days=14)).isoformat(), 'endDate': (now + timedelta(days=14)).isoformat()}
    response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    self.initial_data['auctionPeriod'] = data
    del self.initial_data['awardPeriod']
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'period should begin after auctionPeriod'], u'location': u'body', u'name': u'awardPeriod'}
    ])
    #
    # data = self.initial_data['minimalStep']
    # self.initial_data['minimalStep'] = {'amount': '1000.0'}
    # response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    # self.initial_data['minimalStep'] = data
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': [u'value should be less than value of auction'], u'location': u'body', u'name': u'minimalStep'}
    # ])
    #
    # data = self.initial_data['minimalStep']
    # self.initial_data['minimalStep'] = {'amount': '100.0', 'valueAddedTaxIncluded': False}
    # response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    # self.initial_data['minimalStep'] = data
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': [u'valueAddedTaxIncluded should be identical to valueAddedTaxIncluded of value of auction'], u'location': u'body', u'name': u'minimalStep'}
    # ])
    #
    # data = self.initial_data['minimalStep']
    # self.initial_data['minimalStep'] = {'amount': '100.0', 'currency': "USD"}
    # response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    # self.initial_data['minimalStep'] = data
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': [u'currency should be identical to currency of value of auction'], u'location': u'body', u'name': u'minimalStep'}
    # ])
    #
    # auction_data = deepcopy(self.initial_data)
    # auction_data['value'] = {'amount': '100.0', 'currency': "USD"}
    # auction_data['minimalStep'] = {'amount': '5.0', 'currency': "USD"}
    # response = self.app.post_json(request_path, {'data': auction_data}, status=422)
    # self.assertEqual(response.status, '422 Unprocessable Entity')
    # self.assertEqual(response.content_type, 'application/json')
    # self.assertEqual(response.json['status'], 'error')
    # self.assertEqual(response.json['errors'], [
    #     {u'description': [u'currency should be only UAH'], u'location': u'body', u'name': u'value'}
    # ])

    data = self.initial_data["procuringEntity"]["contactPoint"]["telephone"]
    del self.initial_data["procuringEntity"]["contactPoint"]["telephone"]
    response = self.app.post_json(request_path, {'data': self.initial_data}, status=422)
    self.initial_data["procuringEntity"]["contactPoint"]["telephone"] = data
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'contactPoint': {u'email': [u'telephone or email should be present']}}, u'location': u'body', u'name': u'procuringEntity'}
    ])


def create_auction_auctionPeriod(self):
    data = self.initial_data.copy()
    if SANDBOX_MODE:
        data['procurementMethodDetails'] = 'quick, accelerator=1440'

    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    auction_id = response.json['data']['id']

    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    auction = response.json['data']
    self.assertIn('tenderPeriod', auction)
    self.assertIn('auctionPeriod', auction)
    self.assertNotIn('startDate', auction['auctionPeriod'])
    if SANDBOX_MODE:
        auction_startDate = parse_date(data['auctionPeriod']['startDate'], None)
        if not auction_startDate.tzinfo:
            auction_startDate = TZ.localize(auction_startDate)
        tender_endDate = parse_date(auction['tenderPeriod']['endDate'], None)
        if not tender_endDate.tzinfo:
            tender_endDate = TZ.localize(tender_endDate)
        self.assertLessEqual((auction_startDate - tender_endDate).total_seconds(), 70)
    else:
        self.assertEqual(
            parse_date(data['auctionPeriod']['startDate']).date(),
            parse_date(auction['auctionPeriod']['shouldStartAfter'], TZ).date()
        )
        self.assertEqual(parse_date(auction['tenderPeriod']['endDate']).date(), parse_date(auction['auctionPeriod']['shouldStartAfter'], TZ).date())
        self.assertGreater(parse_date(auction['tenderPeriod']['endDate']).time(), parse_date(auction['auctionPeriod']['shouldStartAfter'], TZ).time())


def create_auction_generated(self):
    document = {
        'id': '1' * 32,
        'documentType': 'x_dgfAssetFamiliarization',
        'title': u'\u0443\u043a\u0440.doc',
        'accessDetails': 'access details',
        'format': 'application/msword',
        'datePublished': get_now().isoformat(),
        'dateModified': get_now().isoformat(),
    }

    data = self.initial_data.copy()
    data['documents'] = [document]
    #del data['awardPeriod']
    data.update({'id': 'hash', 'doc_id': 'hash2', 'auctionID': 'hash3'})

    response = self.app.post_json('/auctions', {'data': data})
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}
    auction_id = response.json['data']['id']

    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    auction = response.json['data']
    for key in ['procurementMethodDetails', 'submissionMethodDetails']:
        if key in auction:
            auction.pop(key)
    self.assertEqual(set(auction), set([
        u'procurementMethodType', u'id', u'date', u'dateModified', u'auctionID', u'status', u'enquiryPeriod',
        u'tenderPeriod', u'minimalStep', u'items', u'value', u'procuringEntity', u'next_check',
        u'procurementMethod', u'awardCriteria', u'submissionMethod', u'title', u'owner', u'auctionPeriod',
        u'tenderAttempts', u'auctionParameters', u'bankAccount', u'registrationFee', u'lotIdentifier', u'registrationFee',
        u'guarantee', u'description', u'rectificationPeriod'
    ]))
    self.assertNotEqual(data['id'], auction['id'])
    self.assertNotEqual(data['doc_id'], auction['id'])
    self.assertNotEqual(data['auctionID'], auction['auctionID'])
    # Check all field of document in post data appear in created auction


def create_auction(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/auctions', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn(response.json['data']['id'], response.headers['Location'])
    auction_id = response.json['data']['id']

    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    auction = response.json['data']

    if self.initial_organization == self.test_financial_organization:
        self.assertEqual(set(auction) - set(self.initial_data), set([
            u'id', u'dateModified', u'auctionID', u'date', u'status', u'procurementMethod',
            u'awardCriteria', u'submissionMethod', u'next_check', u'owner', u'enquiryPeriod', u'tenderPeriod',
            u'minimalStep', u'rectificationPeriod'
        ]))
    else:
        self.assertEqual(set(auction) - set(self.initial_data), set([
            u'id', u'dateModified', u'auctionID', u'date', u'status', u'procurementMethod',
            u'awardCriteria', u'submissionMethod', u'next_check', u'owner', u'enquiryPeriod', u'tenderPeriod',
            u'minimalStep', u'rectificationPeriod'
        ]))

    response = self.app.get('/auctions/{}'.format(auction['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(set(response.json['data']), set(auction))
    self.assertEqual(response.json['data'], auction)

    response = self.app.post_json('/auctions?opt_jsonp=callback', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/javascript')
    self.assertIn('callback({"', response.body)

    response = self.app.post_json('/auctions?opt_pretty=1', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)

    response = self.app.post_json('/auctions', {"data": self.initial_data, "options": {"pretty": True}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)

    auction_data = deepcopy(self.initial_data)
    auction_data['guarantee'] = {"amount": 100500, "currency": "USD"}
    response = self.app.post_json('/auctions', {'data': auction_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    data = response.json['data']
    self.assertIn('guarantee', data)
    self.assertEqual(data['guarantee']['amount'], 100500)
    self.assertEqual(data['guarantee']['currency'], "USD")


def check_daylight_savings_timezone(self):
    data = deepcopy(self.initial_data)
    ua_tz = pytz.timezone('Europe/Kiev')
    response = self.app.post_json('/auctions', {'data': data})
    timezone_before = parse_date(response.json['data']['tenderPeriod']['endDate']).astimezone(tz=ua_tz)
    timezone_before = timezone_before.strftime('%Z')
    now = get_now()
    list_of_timezone_bools = []
    # check if DST working with different time periods
    for i in (10, 90, 180, 210, 240):
        data.update({
            "auctionPeriod": {
                "startDate": calculate_business_date(now, timedelta(days=i), None, working_days=True).isoformat(),
            }})
        response = self.app.post_json('/auctions', {'data': data})
        timezone_after = parse_date(response.json['data']['tenderPeriod']['endDate']).astimezone(tz=ua_tz)
        timezone_after = timezone_after.strftime('%Z')
        list_of_timezone_bools.append(timezone_before != timezone_after)
    self.assertTrue(any(list_of_timezone_bools))


def tender_period_validation(self):
    data = deepcopy(self.initial_data)
    data['auctionPeriod']['startDate'] = (get_now() + timedelta(days=1)).isoformat()
    response = self.app.post_json('/auctions', {'data': data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(
        response.json['errors'][0]['description'][0],
        'tenderPeriod should be at least 7 working days'
    )

    response = self.app.post_json('/auctions', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    tender_period = {
        'startDate': parse_datetime(response.json['data']['tenderPeriod']['startDate']),
        'endDate': parse_datetime(response.json['data']['tenderPeriod']['endDate']),
    }

    # Check if tenderPeriod last more than 7 working days
    expected_end_date = calculate_business_date(tender_period['startDate'], timedelta(days=7), None, working_days=True)
    self.assertGreaterEqual(tender_period['endDate'], expected_end_date)

    if SANDBOX_MODE:
        data = deepcopy(self.initial_data)
        data['procurementMethodDetails'] = 'quick, accelerator=1440'
        period_duration = 500
        data['auctionPeriod']['startDate'] = (get_now() + timedelta(seconds=period_duration)).isoformat()

        response = self.app.post_json('/auctions', {"data": data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        tender_period = {
            'startDate': parse_datetime(response.json['data']['tenderPeriod']['startDate']),
            'endDate': parse_datetime(response.json['data']['tenderPeriod']['endDate']),
        }
        delta = tender_period['endDate'] - tender_period['startDate']
        self.assertAlmostEqual(delta.total_seconds(), 500, delta=100)


def rectification_period_generation(self):
    response = self.app.post_json('/auctions', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    tender_period = {
        'startDate': parse_datetime(response.json['data']['tenderPeriod']['startDate']),
        'endDate': parse_datetime(response.json['data']['tenderPeriod']['endDate']),
    }
    rectification_period = {
        'startDate': parse_datetime(response.json['data']['rectificationPeriod']['startDate']),
        'endDate': parse_datetime(response.json['data']['rectificationPeriod']['endDate']),
    }

    self.assertEqual(tender_period['startDate'], rectification_period['startDate'])

    # Check if there is 5 working days between rectificationPeriod.endDate and tenderPeriod.endDate
    expected_end_date = calculate_business_date(rectification_period['endDate'], timedelta(days=5), None, working_days=True)
    self.assertEqual(tender_period['endDate'], expected_end_date)


def edit_after_rectification_period(self):
    response = self.app.post_json('/auctions', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    # Change rectification period
    fromdb = self.db.get(auction_id)
    fromdb = AppraisalAuction(fromdb)

    fromdb.tenderPeriod.startDate = calculate_business_date(
        fromdb.tenderPeriod.startDate,
        -timedelta(days=15),
        fromdb,
        working_days=True
    )
    fromdb.tenderPeriod.endDate = calculate_business_date(
        fromdb.tenderPeriod.startDate,
        timedelta(days=7),
        fromdb,
        working_days=True
    )
    fromdb = fromdb.store(self.db)
    self.assertEqual(fromdb.id, auction_id)

    # Check that nothing changed after patch
    unique_descr = 'description_' + uuid4().hex
    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'description': unique_descr}},
        headers=access_header
    )

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertNotEqual(response.json['data']['description'], unique_descr)


# AppraisalAuctionProcessTest


def first_bid_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    response = self.app.post_json('/auctions',
                                  {"data": self.initial_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    # switch to active.tendering
    self.set_status('active.tendering')
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    if self.initial_organization == self.test_financial_organization:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True, 'eligible': True}})
    else:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True}})
    bid_id = response.json['data']['id']
    bid_token = response.json['access']['token']
    bids_tokens = {bid_id: bid_token}
    # create second bid
    self.app.authorization = ('Basic', ('broker', ''))
    if self.initial_organization == self.test_financial_organization:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True, 'eligible': True}})
    else:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True}})
    bids_tokens[response.json['data']['id']] = response.json['access']['token']
    # switch to active.auction
    self.set_status('active.auction')

    # get auction info
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}/auction'.format(auction_id))
    auction_bids_data = response.json['data']['bids']

    # check bid participationUrl
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bid_id, bid_token))
    self.assertIn('participationUrl', response.json['data'])

    # posting auction results
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

    now = get_now()
    auction_result = {
        'bids': [
            {
                "id": b['id'],
                "date": (now - timedelta(seconds=i)).isoformat(),
                "value": {"amount": value_threshold * 2},

            }
            for i, b in enumerate(auction_bids_data)
        ]
    }

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award = [i for i in response.json['data'] if i['status'] == 'pending'][0]
    award_id = award['id']

    # Upload rejectProtocol
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
        self.auction_id, award_id, owner_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']

    response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, owner_token), {"data": {
        "description": "rejection protocol",
        "documentType": 'rejectionProtocol'
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json["data"]["documentType"], 'rejectionProtocol')
    self.assertEqual(response.json["data"]["author"], 'auction_owner')
    # set award as unsuccessful
    response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
                                   {"data": {"status": "unsuccessful"}})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award2 = [i for i in response.json['data'] if i['status'] == 'pending'][0]
    award2_id = award2['id']
    self.assertNotEqual(award_id, award2_id)
    # create first award complaint
    # self.app.authorization = ('Basic', ('broker', ''))
    # response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(auction_id, award_id, bid_token),
    #                               {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.initial_organization, 'status': 'claim'}})
    # complaint_id = response.json['data']['id']
    # complaint_owner_token = response.json['access']['token']
    # # create first award complaint #2
    # response = self.app.post_json('/auctions/{}/awards/{}/complaints?acc_token={}'.format(auction_id, award_id, bid_token),
    #                               {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.initial_organization}})
    # # answering claim
    # self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(auction_id, award_id, complaint_id, owner_token), {"data": {
    #     "status": "answered",
    #     "resolutionType": "resolved",
    #     "resolution": "resolution text " * 2
    # }})
    # # satisfying resolution
    # self.app.patch_json('/auctions/{}/awards/{}/complaints/{}?acc_token={}'.format(auction_id, award_id, complaint_id, complaint_owner_token), {"data": {
    #     "satisfied": True,
    #     "status": "resolved"
    # }})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award = [i for i in response.json['data'] if i['status'] == 'pending'][0]
    award_id = award['id']
    # Upload auction protocol
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
        self.auction_id, award_id, owner_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']

    response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, owner_token), {"data": {
        "description": "auction protocol",
        "documentType": 'auctionProtocol'
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
    self.assertEqual(response.json["data"]["author"], 'auction_owner')
    # set award as active
    self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token), {"data": {"status": "active"}})
    # get contract id
    response = self.app.get('/auctions/{}'.format(auction_id))
    contract_id = response.json['data']['contracts'][-1]['id']
    # create auction contract document for test
    response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(auction_id, contract_id, owner_token), upload_files=[('file', 'name.doc', 'content')], status=201)
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    # after stand slill period
    self.app.authorization = ('Basic', ('chronograph', ''))
    self.set_status('complete', {'status': 'active.awarded'})
    # time travel
    auction = self.db.get(auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)
    # sign contract

    # Upload document
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json(
        '/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, contract_id, owner_token),
        params={
            'data': {
                'documentType': 'contractSigned',
                'title': 'Signed contract',
                'format': 'application/msword',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32
            }
        })
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['title'], 'Signed contract')
    self.assertEqual(response.json['data']['documentType'], 'contractSigned')

    # Patch dateSigned field
    signature_date = get_now().isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract_id, owner_token
    ), {"data": {"dateSigned": signature_date}})
    self.assertEqual(response.status, '200 OK')


    self.app.authorization = ('Basic', ('broker', ''))
    self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token), {"data": {"status": "active"}})
    # check status
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'complete')

    response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(auction_id, contract_id, owner_token), upload_files=[('file', 'name.doc', 'content')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (complete) auction status")

    response = self.app.patch_json('/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(auction_id, contract_id, doc_id, owner_token), {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) auction status")

    response = self.app.put('/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(auction_id, contract_id, doc_id, owner_token), upload_files=[('file', 'name.doc', 'content3')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) auction status")


def auctionUrl_in_active_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    response = self.app.post_json('/auctions',
                                  {"data": self.initial_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    # switch to active.tendering
    response = self.set_status(
        'active.tendering',
        {
            "auctionPeriod": {"startDate": calculate_business_date(get_now(), timedelta(days=10), None, working_days=True).isoformat()}
        }
    )
    self.assertIn("auctionPeriod", response.json['data'])
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    if self.initial_organization == self.test_financial_organization:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], 'qualified': True, 'eligible': True}})
    else:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], 'qualified': True}})
    # switch to active.qualification
    self.set_status('active.auction', {'status': 'active.tendering'})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"id": auction_id}})
    self.assertIn('auctionUrl', response.json['data'])
    self.assertIn(auction_id, response.json['data']['auctionUrl'])


def suspended_auction(self):
    self.app.authorization = ('Basic', ('broker', ''))
    # empty auctions listing
    response = self.app.get('/auctions')
    self.assertEqual(response.json['data'], [])
    # create auction
    auction_data = deepcopy(self.initial_data)
    auction_data['suspended'] = True
    response = self.app.post_json('/auctions',
                                  {"data": auction_data})
    auction_id = self.auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    self.assertNotIn('suspended', response.json['data'])

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], True)
    self.assertNotIn('next_check', response.json['data'])

    self.app.authorization = authorization
    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')

    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], False)
    self.assertIn('next_check', response.json['data'])

    self.app.authorization = authorization
    # switch to active.tendering
    self.set_status('active.tendering')
    # create bid
    self.app.authorization = ('Basic', ('broker', ''))
    if self.initial_organization == self.test_financial_organization:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True, 'eligible': True}})
    else:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True}})
    bid_id = response.json['data']['id']
    bid_token = response.json['access']['token']
    # create second bid
    self.app.authorization = ('Basic', ('broker', ''))
    if self.initial_organization == self.test_financial_organization:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True, 'eligible': True}})
    else:
        response = self.app.post_json('/auctions/{}/bids'.format(auction_id),
                                      {'data': {'tenderers': [self.initial_organization], "value": {"amount": 450}, 'qualified': True}})

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], True)
    self.assertNotIn('next_check', response.json['data'])

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], False)
    self.assertIn('next_check', response.json['data'])

    self.app.authorization = authorization

    # switch to active.auction
    self.set_status('active.auction')

    # get auction info
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}/auction'.format(auction_id))
    auction_bids_data = response.json['data']['bids']

    # check bid participationUrl
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bid_id, bid_token))
    self.assertIn('participationUrl', response.json['data'])

    # posting auction results
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

    now = get_now()
    auction_result = {
        'bids': [
            {
                "id": b['id'],
                "date": (now - timedelta(seconds=i)).isoformat(),
                "value": {"amount": value_threshold * 2},

            }
            for i, b in enumerate(auction_bids_data)
        ]
    }

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))

    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], True)
    self.assertNotIn('next_check', response.json['data'])

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], False)

    self.app.authorization = authorization
    # set award as unsuccessful
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.post_json(
        '/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, owner_token),
        params={
            'data': {
                'documentType': 'rejectionProtocol',
                'title': 'rejection protocol',
                'format': 'application/msword',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32
            }
        })
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['title'], 'rejection protocol')
    self.assertEqual(response.json['data']['documentType'], 'rejectionProtocol')

    response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
                                   {"data": {"status": "unsuccessful"}})
    self.assertEqual(response.json['data']['status'], 'unsuccessful')
    # get awards
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    self.assertEqual(len(response.json['data']), 2)
    self.assertEqual(response.json['data'][0]['status'], 'unsuccessful')
    # get pending award
    award2_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    self.assertNotEqual(award_id, award2_id)

    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}/awards?acc_token={}'.format(auction_id, owner_token))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

    response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
        self.auction_id, award_id, owner_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
    doc_id = response.json["data"]['id']

    response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(auction_id, award_id, doc_id, owner_token), {"data": {"documentType": 'auctionProtocol'}})
    # set award as active
    self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token), {"data": {"status": "active"}})

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], True)
    self.assertNotIn('next_check', response.json['data'])

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], False)

    self.app.authorization = authorization

    response = self.app.patch_json(
        '/auctions/{}/awards/{}?acc_token={}'.format(auction_id, award_id, owner_token),
        {"data": {"status": "active"}},
        status=403
    )
    self.assertEqual(response.json['errors'][0]['description'], "Can\'t update award in current (active) status")
    # get contract id
    response = self.app.get('/auctions/{}'.format(auction_id))
    contract_id = response.json['data']['contracts'][-1]['id']

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": True}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], True)
    self.assertNotIn('next_check', response.json['data'])

    response = self.app.patch_json('/auctions/{}'.format(auction_id), {"data": {"suspended": False}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']['suspended'], False)

    self.app.authorization = authorization

    # create auction contract document for test
    response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(auction_id, contract_id, owner_token), upload_files=[('file', 'name.doc', 'content')], status=201)
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    # after stand slill period
    self.app.authorization = ('Basic', ('chronograph', ''))
    self.set_status('complete', {'status': 'active.awarded'})
    # time travel
    auction = self.db.get(auction_id)
    for i in auction.get('awards', []):
        i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
    self.db.save(auction)
    # sign contract
    self.app.authorization = ('Basic', ('broker', ''))

    # Upload document
    response = self.app.post_json(
        '/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, contract_id, owner_token),
        params={
            'data': {
                'documentType': 'contractSigned',
                'title': 'Signed contract',
                'format': 'application/msword',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32
            }
        })
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['title'], 'Signed contract')
    self.assertEqual(response.json['data']['documentType'], 'contractSigned')

    # Patch dateSigned field
    signature_date = get_now().isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract_id, owner_token
    ), {"data": {"dateSigned": signature_date}})
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/auctions/{}/contracts/{}?acc_token={}'.format(auction_id, contract_id, owner_token),
        {"data": {"status": "active"}}
    )
    self.assertEqual(response.json['data']['status'], 'active')
    # check status
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'complete')


def move_draft_to_active_tendering(self):
    data = self.initial_data.copy()
    data['status'] = 'draft'

    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'draft')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    # Move from draft to active.tendering

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active.tendering')


def move_draft_to_wrong_status(self):
    data = self.initial_data.copy()
    data['status'] = 'draft'

    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'draft')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    # Move from draft to active.tendering

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'complete'}},
        headers=access_header,
        status=422
    )
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['description'], 'Can\'t switch auction in such status (complete)')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(response.json['data']['status'], 'draft')


def auction_Administrator_change(self):
    response = self.app.post_json('/auctions', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    auction = response.json['data']

    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction['id']),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    response = self.app.post_json('/auctions/{}/questions'.format(auction['id']), {
        'data': {'title': 'question title', 'description': 'question description',
                 'author': self.initial_organization}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    question = response.json['data']

    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('administrator', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction['id']),
                                   {'data': {'mode': u'test', 'procuringEntity': {"identifier": {"id": "00000000"}}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['mode'], u'test')
    self.assertEqual(response.json['data']["procuringEntity"]["identifier"]["id"], "00000000")

    response = self.app.patch_json('/auctions/{}/questions/{}'.format(auction['id'], question['id']),
                                   {"data": {"answer": "answer"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {"location": "url", "name": "role", "description": "Forbidden"}
    ])
    self.app.authorization = authorization

    response = self.app.post_json('/auctions', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    auction = response.json['data']
    auction_token = response.json['access']['token']

    response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
        auction['id'], auction_token
    ), {'data': {'reason': 'cancellation reason', 'status': 'active'}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    self.app.authorization = ('Basic', ('administrator', ''))
    response = self.app.patch_json('/auctions/{}'.format(auction['id']), {'data': {'mode': u'test'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['mode'], u'test')


def listing(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    auctions = []

    for i in range(3):
        offset = get_now().isoformat()
        response = self.app.post_json('/auctions', {'data': self.initial_data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')

        auction_id = response.json['data']['id']
        owner_token = response.json['access']['token']
        access_header = {'X-Access-Token': str(owner_token)}

        response = self.app.patch_json(
            '/auctions/{}'.format(auction_id),
            {'data': {'status': 'active.tendering'}},
            headers=access_header
        )
        auctions.append(response.json['data'])

    ids = ','.join([i['id'] for i in auctions])

    while True:
        response = self.app.get('/auctions')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in auctions]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]),
                     set([i['dateModified'] for i in auctions]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in auctions]))

    while True:
        response = self.app.get('/auctions?offset={}'.format(offset))
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/auctions?limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('prev_page', response.json)
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.get('/auctions', params=[('opt_fields', 'status')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status']))
    self.assertIn('opt_fields=status', response.json['next_page']['uri'])

    response = self.app.get('/auctions', params=[('opt_fields', 'status,enquiryPeriod')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status', u'enquiryPeriod']))
    self.assertIn('opt_fields=status%2CenquiryPeriod', response.json['next_page']['uri'])

    response = self.app.get('/auctions?descending=1')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in auctions]))
    self.assertEqual([i['dateModified'] for i in response.json['data']],
                     sorted([i['dateModified'] for i in auctions], reverse=True))

    response = self.app.get('/auctions?descending=1&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    test_auction_data2 = self.initial_data.copy()
    test_auction_data2['mode'] = 'test'
    response = self.app.post_json('/auctions', {'data': test_auction_data2})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    while True:
        response = self.app.get('/auctions?mode=test')
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/auctions?mode=_all_')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 4)


def listing_changes(self):
    response = self.app.get('/auctions?feed=changes')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    auctions = []

    for i in range(3):
        response = self.app.post_json('/auctions', {'data': self.initial_data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        auction_id = response.json['data']['id']
        owner_token = response.json['access']['token']
        access_header = {'X-Access-Token': str(owner_token)}

        response = self.app.patch_json(
            '/auctions/{}'.format(auction_id),
            {'data': {'status': 'active.tendering'}},
            headers=access_header
        )
        auctions.append(response.json['data'])

    ids = ','.join([i['id'] for i in auctions])

    while True:
        response = self.app.get('/auctions?feed=changes')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(','.join([i['id'] for i in response.json['data']]), ids)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in auctions]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]),
                     set([i['dateModified'] for i in auctions]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in auctions]))

    response = self.app.get('/auctions?feed=changes&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('prev_page', response.json)
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.get('/auctions?feed=changes', params=[('opt_fields', 'status')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status']))
    self.assertIn('opt_fields=status', response.json['next_page']['uri'])

    response = self.app.get('/auctions?feed=changes', params=[('opt_fields', 'status,enquiryPeriod')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status', u'enquiryPeriod']))
    self.assertIn('opt_fields=status%2CenquiryPeriod', response.json['next_page']['uri'])

    response = self.app.get('/auctions?feed=changes&descending=1')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in auctions]))
    self.assertEqual([i['dateModified'] for i in response.json['data']],
                     sorted([i['dateModified'] for i in auctions], reverse=True))

    response = self.app.get('/auctions?feed=changes&descending=1&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(TEST_ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    test_auction_data2 = self.initial_data.copy()
    test_auction_data2['mode'] = 'test'
    response = self.app.post_json('/auctions', {'data': test_auction_data2})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    while True:
        response = self.app.get('/auctions?feed=changes&mode=test')
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/auctions?feed=changes&mode=_all_')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 4)


def listing_draft(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    auctions = []

    for i in range(3):
        response = self.app.post_json('/auctions', {'data': self.initial_data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        auction_id = response.json['data']['id']
        owner_token = response.json['access']['token']
        access_header = {'X-Access-Token': str(owner_token)}

        response = self.app.patch_json(
            '/auctions/{}'.format(auction_id),
            {'data': {'status': 'active.tendering'}},
            headers=access_header
        )

        auctions.append(response.json['data'])

        response = self.app.post_json('/auctions', {'data': self.initial_data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')

    ids = ','.join([i['id'] for i in auctions])

    while True:
        response = self.app.get('/auctions')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in auctions]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]),
                     set([i['dateModified'] for i in auctions]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in auctions]))


def patch_auction(self):
    response = self.app.get('/auctions')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/auctions', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    auction = response.json['data']
    dateModified = auction.pop('dateModified')
    auction['rectificationPeriod'].pop('invalidationDate')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token),
                                   {'data': {'status': 'cancelled'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['status'], 'cancelled')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'status': 'cancelled'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['status'], 'cancelled')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token),
                                   {'data': {'procuringEntity': {'kind': 'defense'}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('kind', response.json['data']['procuringEntity'])

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'procurementMethodRationale': 'Open'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction = response.json['data']
    new_auction.pop('dateModified')
    new_auction['rectificationPeriod'].pop('invalidationDate')
    self.assertEqual(auction, new_auction)

    date_modified_to_patch = (datetime.now() + timedelta(days=30)).isoformat()
    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'dateModified': date_modified_to_patch}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction2 = response.json['data']
    new_dateModified2 = new_auction2.pop('dateModified')
    new_auction2['rectificationPeriod'].pop('invalidationDate')
    self.assertEqual(new_auction, new_auction2)
    self.assertNotEqual(date_modified_to_patch, new_dateModified2)
    # self.assertEqual(new_dateModified, new_dateModified2)

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'items': [self.initial_data['items'][0]]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'enquiryPeriod': {'endDate': new_dateModified2}}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    new_auction = response.json['data']
    self.assertIn('startDate', new_auction['enquiryPeriod'])

    auction_data = self.db.get(auction['id'])
    auction_data['status'] = 'complete'
    self.db.save(auction_data)

    response = self.app.patch_json('/auctions/{}?acc_token={}'.format(
        auction['id'], owner_token
    ), {'data': {'status': 'active.auction'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update auction in current (complete) status")


def check_bids_invalidation(self):
    self.app.authorization = ('Basic', ('broker', ''))

    # Auction creation
    data = self.initial_data.copy()
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.auction_id = auction_id
    self.set_status('active.tendering')

    # Create and activate bid
    response = self.app.post_json(
        '/auctions/{}/bids'.format(auction_id),
        {'data': {'tenderers': [self.initial_organization], "status": "draft", 'qualified': True, 'eligible': True}}
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    bidder_id = response.json['data']['id']
    bid_token = response.json['access']['token']

    self.app.patch_json(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token),
        {'data': {'status': 'active'}}
    )

    # Empty patch on auction
    self.app.patch_json(
        'auctions/{}'.format(auction_id),
        {'data': {}},
        headers=access_header
    )

    # Check if bid invalidated
    response = self.app.get(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token)
    )
    self.assertEqual(response.json['data']['status'], 'invalid')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertIn('invalidationDate', response.json['data']['rectificationPeriod'])
    invalidation_date = response.json['data']['rectificationPeriod']['invalidationDate']

    # Activate bid again and check if status changes
    self.app.patch_json(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token),
        {'data': {'status': 'active'}}
    )

    response = self.app.get(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token)
    )
    self.assertEqual(response.json['data']['status'], 'active')

    # Change rectification period
    fromdb = self.db.get(auction_id)
    fromdb = AppraisalAuction(fromdb)

    fromdb.tenderPeriod.startDate = calculate_business_date(
        fromdb.tenderPeriod.startDate,
        -timedelta(days=15),
        fromdb,
        working_days=True
    )
    fromdb.tenderPeriod.endDate = calculate_business_date(
        fromdb.tenderPeriod.startDate,
        timedelta(days=7),
        fromdb,
        working_days=True
    )
    fromdb = fromdb.store(self.db)
    self.assertEqual(fromdb.id, auction_id)

    # Check that nothing changed after patch
    self.app.patch_json(
        'auctions/{}'.format(auction_id),
        {'data': {}},
        headers=access_header
    )
    response = self.app.get(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token)
    )
    self.assertEqual(response.json['data']['status'], 'active')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertEqual(invalidation_date, response.json['data']['rectificationPeriod']['invalidationDate'])
