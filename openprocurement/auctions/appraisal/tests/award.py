# -*- coding: utf-8 -*-
import unittest

from datetime import timedelta

from openprocurement.auctions.core.tests.award import (
    AuctionAwardDocumentResourceTestMixin
)
from openprocurement.auctions.core.tests.plugins.awarding.v3_1.tests.award import (
    AuctionAwardProcessTestMixin,
    CreateAuctionAwardTestMixin

)
from openprocurement.auctions.core.utils import get_now, get_related_contract_of_award

from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest,
    test_bids,
)


class AppraisalAuctionCreateAwardTest(BaseAppraisalAuctionWebTest, CreateAuctionAwardTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids


class AppraisalAuctionAwardProcessTest(BaseAppraisalAuctionWebTest, AuctionAwardProcessTestMixin):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_bids
    docservice = True

    def upload_rejection_protocol(self, award):
        owner_token = self.auction_token
        award_id = award['id']

        response = self.app.post(
            '/auctions/{}/awards/{}/documents?acc_token={}'.format(
                self.auction_id, award_id, owner_token
            ), upload_files=[('file', 'rejection_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual(
            'rejection_protocol.pdf', response.json["data"]["title"]
        )

        response = self.app.patch_json(
            '/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(
                self.auction_id, award_id, doc_id, owner_token
            ),
            {"data": {
                "description": "rejection protocol",
                "documentType": 'rejectionProtocol'
            }})

        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(
            response.json["data"]["documentType"], 'rejectionProtocol'
        )

    def set_award_unsuccessful(self, award):
        response = self.app.get(
            '/auctions/{}/contracts'.format(self.auction_id)
        )

        contract = get_related_contract_of_award(
            award['id'], {'contracts': response.json['data']}
        )

        response = self.app.post(
            '/auctions/{}/contracts/{}/documents?acc_token={}'.format(
                self.auction_id, contract['id'], self.auction_token
            ), upload_files=[('file', 'rejection_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json['data']['id']

        response = self.app.patch_json(
            '/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(
                self.auction_id, contract['id'], doc_id, self.auction_token
            ),
            {"data": {
                "description": "rejection protocol",
                "documentType": 'rejectionProtocol'
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')

        response = self.app.patch_json(
            '/auctions/{}/contracts/{}?acc_token={}'.format(
                self.auction_id, contract['id'], self.auction_token
            ), {'data': {'status': 'cancelled'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'cancelled')

        response = self.app.get('/auctions/{}/awards/{}'.format(
            self.auction_id, award['id']
        ))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'unsuccessful')

    def upload_auction_protocol(self, award):
        award_id = award['id']
        bid_token = self.initial_bids_tokens[award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, bid_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, bid_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json(
            '/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, self.auction_token),
            {"data": {
                "description": "auction protocol",
                "documentType": 'auctionProtocol'
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.get('/auctions/{}/awards/{}/documents'.format(self.auction_id,award_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual('auctionProtocol', response.json["data"][0]["documentType"])
        self.assertEqual('auction_protocol.pdf', response.json["data"][0]["title"])
        self.assertEqual('bid_owner', response.json["data"][0]["author"])
        self.assertEqual('auctionProtocol', response.json["data"][1]["documentType"])
        self.assertEqual('auction_owner', response.json["data"][1]["author"])

    def setUp(self):
        super(AppraisalAuctionAwardProcessTest, self).setUp()

        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']

        # auction['value']['amount'] = 234.5
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


class AppraisalAuctionAwardDocumentResourceTest(BaseAppraisalAuctionWebTest,
                                              AuctionAwardDocumentResourceTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AppraisalAuctionAwardDocumentResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()

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
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionCreateAwardTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionAwardProcessTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionAwardDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
