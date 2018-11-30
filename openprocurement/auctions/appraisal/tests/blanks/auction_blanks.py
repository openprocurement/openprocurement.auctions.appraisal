from copy import deepcopy
from datetime import timedelta

from openprocurement.auctions.core.utils import get_now

# InsiderAuctionAuctionResourceTest


def get_auction_auction(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}/auction'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertNotEqual(auction, self.initial_data)
    self.assertIn('dateModified', auction)
    self.assertIn('minimalStep', auction)
    self.assertNotIn("procuringEntity", auction)
    self.assertNotIn("tenderers", auction["bids"][0])
    self.assertNotIn("value", auction["bids"][0])
    self.assertNotIn("value", auction["bids"][1])

    self.set_status('active.auction')

    response = self.app.get('/auctions/{}/auction'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertNotEqual(auction, self.initial_data)
    self.assertIn('dateModified', auction)
    self.assertIn('minimalStep', auction)
    self.assertNotIn("procuringEntity", auction)
    self.assertNotIn("tenderers", auction["bids"][0])
    self.assertNotIn("value", auction["bids"][0])
    self.assertNotIn("value", auction["bids"][1])

    response = self.app.get('/auctions/{}/auction?opt_jsonp=callback'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/javascript')
    self.assertIn('callback({"data": {"', response.body)

    response = self.app.get('/auctions/{}/auction?opt_pretty=1'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "data": {\n        "', response.body)

    self.set_status('active.qualification')

    response = self.app.get('/auctions/{}/auction'.format(self.auction_id), status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't get auction info in current (active.qualification) auction status")


def post_auction_auction(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't report auction results in current (active.tendering) auction status")

    self.set_status('active.auction')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                  {'data': {'bids': [{'invalid_field': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'invalid_field': u'Rogue field'}, u'location': u'body', u'name': u'bids'}
    ])

    patch_data = {
        'bids': [
            {
                "id": self.initial_bids[1]['id'],
                "value": {
                    "amount": 419,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    }

    patch_data['bids'].append({
        "value": {
            "amount": 409,
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    })

    patch_data['bids'][1]['id'] = "some_id"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], {u'id': [u'Hash value is wrong length.']})

    patch_data['bids'][1]['id'] = self.initial_bids[0]['id']

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertIn("value", auction["bids"][0])
    self.assertIn("value", auction["bids"][1])
    self.assertEqual('active.qualification', auction["status"])
    for i, status in enumerate(['pending', 'pending.waiting']):
        self.assertIn("tenderers", auction["bids"][i])
        self.assertIn("name", auction["bids"][i]["tenderers"][0])
        # self.assertIn(auction["awards"][0]["id"], response.headers['Location'])
        self.assertEqual(auction["awards"][i]['bid_id'], patch_data["bids"][i]['id'])
        self.assertEqual(auction["awards"][i]['value']['amount'], patch_data["bids"][i]['value']['amount'])
        self.assertEqual(auction["awards"][i]['suppliers'], self.initial_bids[i]['tenderers'])
        self.assertEqual(auction["awards"][i]['status'], status)
        if status == 'pending':
            self.assertIn("verificationPeriod", auction["awards"][i])

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't report auction results in current (active.qualification) auction status")


def patch_auction_auction(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id), {'data': {}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update auction urls in current (active.tendering) auction status")

    self.set_status('active.auction')

    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id),
                                   {'data': {'bids': [{'invalid_field': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'invalid_field': u'Rogue field'}, u'location': u'body', u'name': u'bids'}
    ])

    patch_data = {
        'auctionUrl': u'http://auction-sandbox.openprocurement.org/auctions/{}'.format(self.auction_id),
        'bids': [
            {
                "id": self.initial_bids[1]['id'],
                "participationUrl": u'http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}'.format(
                    self.auction_id, self.initial_bids[1]['id'])
            }
        ]
    }

    patch_data['bids'].append({
        "participationUrl": u'http://auction-sandbox.openprocurement.org/auctions/{}?key_for_bid={}'.format(
            self.auction_id, self.initial_bids[0]['id'])
    })

    patch_data['bids'][1]['id'] = "some_id"

    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], {u'id': [u'Hash value is wrong length.']})

    patch_data['bids'][1]['id'] = self.initial_bids[0]['id']

    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertEqual(auction["bids"][0]['participationUrl'], patch_data["bids"][1]['participationUrl'])
    self.assertEqual(auction["bids"][1]['participationUrl'], patch_data["bids"][0]['participationUrl'])

    self.set_status('complete')

    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can't update auction urls in current (complete) auction status")

# InsiderAuctionBidInvalidationAuctionResourceTest


def post_auction_all_invalid_bids(self):
    self.app.authorization = ('Basic', ('auction', ''))

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

    bids = deepcopy(self.initial_bids)

    bids[0]['value'] = bids[1]['value'] = {'amount': value_threshold - 1}

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': bids}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']
    self.assertLess(auction["bids"][0]['value']['amount'], value_threshold)
    self.assertLess(auction["bids"][1]['value']['amount'], value_threshold)
    self.assertNotIn("value", auction["bids"][2])
    self.assertEqual(auction["bids"][0]['status'], 'invalid')
    self.assertEqual(auction["bids"][1]['status'], 'invalid')
    self.assertEqual(auction["bids"][2]['status'], 'invalid')
    self.assertEqual('unsuccessful', auction["status"])


def post_auction_one_bid_without_value(self):
    self.app.authorization = ('Basic', ('auction', ''))

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

    bids = deepcopy(self.initial_bids)
    bids[0]['value'] = {'amount': value_threshold * 3}
    bids[1]['value'] = {'amount': value_threshold * 2}

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': bids}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']

    self.assertEqual(auction["bids"][0]['value']['amount'], bids[0]['value']['amount'])
    self.assertEqual(auction["bids"][1]['value']['amount'], bids[1]['value']['amount'])

    self.assertGreater(auction["bids"][0]['value']['amount'], value_threshold)
    self.assertGreater(auction["bids"][1]['value']['amount'], value_threshold)
    self.assertNotIn("value", auction["bids"][2])

    self.assertEqual(auction["bids"][0]['status'], 'active')
    self.assertEqual(auction["bids"][1]['status'], 'active')
    self.assertEqual(auction["bids"][2]['status'], 'invalid')

    self.assertEqual('active.qualification', auction["status"])

    for i, status in enumerate(['pending', 'pending.waiting']):
        self.assertIn("tenderers", auction["bids"][i])
        self.assertIn("name", auction["bids"][i]["tenderers"][0])
        # self.assertIn(auction["awards"][0]["id"], response.headers['Location'])
        self.assertEqual(auction["awards"][i]['bid_id'], bids[i]['id'])
        self.assertEqual(auction["awards"][i]['value']['amount'], bids[i]['value']['amount'])
        self.assertEqual(auction["awards"][i]['suppliers'], bids[i]['tenderers'])
        self.assertEqual(auction["awards"][i]['status'], status)
        if status == 'pending':
            self.assertIn("verificationPeriod", auction["awards"][i])


def post_auction_one_valid_bid(self):
    self.app.authorization = ('Basic', ('auction', ''))
    
    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']
    
    bids = deepcopy(self.initial_bids)
    bids[0]['value'] = {'amount': value_threshold}

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': [bids[0]]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']

    self.assertEqual('active.qualification', auction["status"])
    self.assertEqual(len(auction['awards']), 1)
    self.assertEqual(auction['awards'][0]['status'], 'pending')


def post_auction_zero_bids(self):
    self.app.authorization = ('Basic', ('auction', ''))

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),{'data': {'bids': []}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']

    self.assertEqual('unsuccessful', auction["status"])

# InsiderAuctionDraftBidAuctionResourceTest


def post_auction_all_draft_bids(self):
        self.app.authorization = ('Basic', ('auction', ''))

        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        bids = deepcopy(self.initial_bids)
        bids[0]['value'] = {'amount': value_threshold * 3}
        bids[1]['value'] = {'amount': value_threshold * 2}

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': bids}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')

        response = self.app.get('/auctions/{}'.format(self.auction_id))
        auction = response.json['data']

        self.assertNotIn("bids", auction)
        self.assertEqual('unsuccessful', auction["status"])

# InsiderAuctionSameValueAuctionResourceTest


def post_auction_auction_not_changed(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')
    auction = response.json['data']
    value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

    bids = deepcopy(self.initial_bids)
    bids[0]['value'] = bids[1]['value'] = bids[2]['value'] = {'amount': value_threshold * 2}

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': bids}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertEqual('active.qualification', auction["status"])
    self.assertEqual(auction["awards"][0]['bid_id'], bids[0]['id'])
    self.assertEqual(auction["awards"][0]['value']['amount'], bids[0]['value']['amount'])
    self.assertEqual(auction["awards"][0]['suppliers'], bids[0]['tenderers'])


def post_auction_auction_reversed(self):
        self.app.authorization = ('Basic', ('auction', ''))

        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        patch_data = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},


                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.assertEqual(auction["awards"][0]['bid_id'], patch_data['bids'][2]['id'])
        self.assertEqual(auction["awards"][0]['value']['amount'], patch_data['bids'][2]['value']['amount'])
        self.assertEqual(auction["awards"][0]['suppliers'], self.initial_bids[2]['tenderers'])

# InsiderAuctionNoBidsResourceTest


def post_auction_no_bids(self):
    self.app.authorization = ('Basic', ('auction', ''))

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    self.assertEqual(response.status, '200 OK')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),{'data': {'bids': []}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']

    self.assertEqual('unsuccessful', auction["status"])
    self.assertNotIn('bids', auction)
