# -*- coding: utf-8 -*-
from email.header import Header
from openprocurement.api.utils import get_now


def patch_auction_document(self):
    if hasattr(self, 'dgf_platform_legal_details_from') and get_now() > self.dgf_platform_legal_details_from:
        response = self.app.get('/auctions/{}/documents'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            u'Місце та форма прийому заяв на участь в аукціоні та банківські реквізити для зарахування гарантійних внесків',
            response.json["data"][0]["title"])
        self.assertEqual('x_dgfPlatformLegalDetails', response.json["data"][0]["documentType"])
        doc_id = response.json["data"][0]['id']

        response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
            self.auction_id, doc_id, self.auction_token
        ), {"data": {
            'format': 'application/msword',
            "documentType": 'notice'
        }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'First document should be document with x_dgfPlatformLegalDetails documentType'],
             u'location': u'body', u'name': u'documents'}
        ])

    response = self.app.post('/auctions/{}/documents?acc_token={}'.format(
        self.auction_id, self.auction_token
    ), upload_files=[('file', str(Header(u'укр.doc', 'utf-8')), 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    # dateModified = response.json["data"]['dateModified']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual(u'укр.doc', response.json["data"]["title"])
    self.assertNotIn("documentType", response.json["data"])

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {
        "documentOf": "lot"
    }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'relatedItem'},
    ])

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {
        "documentOf": "lot",
        "relatedItem": '0' * 32
    }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'relatedItem should be one of lots'], u'location': u'body', u'name': u'relatedItem'}
    ])

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {
        "documentOf": "item",
        "relatedItem": '0' * 32
    }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'relatedItem should be one of items'], u'location': u'body', u'name': u'relatedItem'}
    ])

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {
        "description": "document description",
        "documentType": 'notice'
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertIn("documentType", response.json["data"])
    self.assertEqual(response.json["data"]["documentType"], 'notice')

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {
        "documentType": None
    }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertNotIn("documentType", response.json["data"])

    response = self.app.get('/auctions/{}/documents/{}'.format(self.auction_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('document description', response.json["data"]["description"])
    # self.assertTrue(dateModified < response.json["data"]["dateModified"])

    self.set_status('active.auction')

    response = self.app.patch_json('/auctions/{}/documents/{}?acc_token={}'.format(
        self.auction_id, doc_id, self.auction_token
    ), {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update document in current (active.auction) auction status")


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

    # Create document
    response = self.app.post(
        '/auctions/{}/documents'.format(auction_id),
        headers=access_header,
        upload_files=[('file', str(Header(u'укр.doc', 'utf-8')), 'content')]
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json['data']['id']

    # Check if bid invalidated
    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token))
    self.assertEqual(response.json['data']['status'], 'invalid')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertIn('invalidationDate', response.json['data']['rectificationPeriod'])
    invalidation_date = response.json['data']['rectificationPeriod']['invalidationDate']

    # Activate bid again and check if status changes
    self.app.patch_json(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token),
        {'data': {'status': 'active'}}
    )

    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token))
    self.assertEqual(response.json['data']['status'], 'active')

    # Put document
    response = self.app.put(
        '/auctions/{}/documents/{}'.format(auction_id, doc_id),
        headers=access_header,
        upload_files=[('file', str(Header(u'укр.doc', 'utf-8')), 'content')]
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token))
    self.assertEqual(response.json['data']['status'], 'invalid')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertIn('invalidationDate', response.json['data']['rectificationPeriod'])
    self.assertNotEqual(invalidation_date, response.json['data']['rectificationPeriod']['invalidationDate'])
    invalidation_date = response.json['data']['rectificationPeriod']['invalidationDate']

    response = self.app.patch_json(
        '/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token),
        {'data': {'status': 'active'}}
    )
    self.assertEqual(response.json['data']['status'], 'active')

    # Patch document
    response = self.app.patch_json(
        '/auctions/{}/documents/{}'.format(self.auction_id, doc_id),
        {"data": {
                "description": "document description"
        }},
        headers=access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get('/auctions/{}/bids/{}?acc_token={}'.format(auction_id, bidder_id, bid_token))
    self.assertEqual(response.json['data']['status'], 'invalid')

    response = self.app.get('/auctions/{}'.format(auction_id))
    self.assertIn('invalidationDate', response.json['data']['rectificationPeriod'])
    self.assertNotEqual(invalidation_date, response.json['data']['rectificationPeriod']['invalidationDate'])
