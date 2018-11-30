# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta

from openprocurement.auctions.core.tests.contract import (
    AuctionContractResourceTestMixin,
    AuctionContractDocumentResourceTestMixin
)
from openprocurement.auctions.core.tests.plugins.contracting.v3_1.tests.contract import (
    AuctionContractV3_1ResourceTestCaseMixin
)
from openprocurement.auctions.core.utils import (
    get_now,
    get_related_award_of_contract
)

from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest, test_bids,
)


DOCUMENTS = {
    'contract': {
        'name': 'contract_signed.pdf',
        'type': 'contractSigned',
        'description': 'contract signed'
    },
    'rejection': {
        'name': 'rejection_protocol.pdf',
        'type': 'rejectionProtocol',
        'description': 'rejection protocol'
    },
    'act': {
        'name': 'act.pdf',
        'type': 'act',
        'description': 'act'
    }
}



class AppraisalAuctionContractResourceTest(
    BaseAppraisalAuctionWebTest,
    AuctionContractResourceTestMixin,
    AuctionContractV3_1ResourceTestCaseMixin,
):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        self.initial_data['value']['amount'] = 479.0 / 2
        super(AppraisalAuctionContractResourceTest, self).setUp()
        # Create award
        authorization = self.app.authorization
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
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.app.authorization = authorization
        self.award = auction['awards'][0]
        self.award_id = self.award['id']
        self.award_value = self.award['value']
        self.award_suppliers = self.award['suppliers']

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token
        ), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
        self.assertEqual(response.json["data"]["author"], 'auction_owner')

        self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token
        ), {"data": {"status": "active"}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        auction = response.json['data']
        self.award_contract_id = auction['contracts'][0]['id']

    def upload_contract_document(self, contract, doc_type):
        # Uploading contract document
        response = self.app.post('/auctions/{}/contracts/{}/documents?acc_token={}'.format(
            self.auction_id, contract['id'], self.auction_token
        ), upload_files=[
            ('file', DOCUMENTS[doc_type]['name'], 'content')
        ])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual(
            DOCUMENTS[doc_type]['name'], response.json["data"]["title"]
        )

        # Patching it's documentType to needed one
        response = self.app.patch_json(
            '/auctions/{}/contracts/{}/documents/{}?acc_token={}'.format(
                self.auction_id, contract['id'], doc_id, self.auction_token
            ),
            {"data": {
                "description": DOCUMENTS[doc_type]['description'],
                "documentType": DOCUMENTS[doc_type]['type']
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(
            response.json["data"]["documentType"], DOCUMENTS[doc_type]['type']
        )

    def check_related_award_status(self, contract, status):
        # Checking related award status
        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        contract = self.app.get('/auctions/{}/contracts/{}'.format(
            self.auction_id, contract['id']
        )).json['data']

        award = get_related_award_of_contract(
            contract, {'awards': response.json['data']}
        )

        response = self.app.get('/auctions/{}/awards/{}'.format(
            self.auction_id, award['id']
        ))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["status"], status)



class AppraisalAuctionContractDocumentResourceTest(BaseAppraisalAuctionWebTest, AuctionContractDocumentResourceTestMixin):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_bids
    docservice = True

    def setUp(self):
        super(AppraisalAuctionContractDocumentResourceTest, self).setUp()
        # Create award
        authorization = self.app.authorization
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
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.app.authorization = authorization
        self.award = auction['awards'][0]
        self.award_id = self.award['id']
        self.award_value = self.award['value']
        self.award_suppliers = self.award['suppliers']

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')
        self.assertEqual(response.json["data"]["author"], 'auction_owner')

        self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token
        ), {"data": {"status": "active"}})
        # Assure contract for award is created
        response = self.app.get('/auctions/{}/contracts'.format(self.auction_id))
        contract = response.json['data'][0]
        self.contract_id = contract['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionContractResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionContractDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
