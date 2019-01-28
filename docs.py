# -*- coding: utf-8 -*-
import json
import os
from datetime import timedelta, datetime
from uuid import uuid4
from copy import deepcopy

from webtest import TestApp

from openprocurement.auctions.core.tests.base import PrefixedRequestClass, base_test_bids
from openprocurement.auctions.core.utils import get_now

import openprocurement.auctions.appraisal.tests.base as base_test
from openprocurement.auctions.appraisal.tests.base import (
    test_appraisal_auction_data as base_test_auction_data,
    BaseAppraisalAuctionWebTest
)


now = datetime.now()

test_auction_data = base_test_auction_data.copy()

test_auction_data["procurementMethodType"] = "appraisal.insider"

test_bids = []
for i in base_test_bids:
    bid = deepcopy(i)
    bid.update({'eligible': True})
    bid.update({'qualified': True})
    bid['tenderers'] = [base_test.test_organization]
    test_bids.append(bid)

bid = {
    "data": {
        "tenderers": [
            {
                "address": {
                    "countryName": "Україна",
                    "locality": "м. Вінниця",
                    "postalCode": "21100",
                    "region": "м. Вінниця",
                    "streetAddress": "вул. Островського, 33"
                },
                "contactPoint": {
                    "email": "soleksuk@gmail.com",
                    "name": "Сергій Олексюк",
                    "telephone": "+380 (432) 21-69-30"
                },
                "identifier": {
                    "scheme": u"UA-EDR",
                    "id": u"00137256",
                    "uri": u"http://www.sc.gov.ua/"
                },
                "name": "ДКП «Школяр»"
            }
        ],
        "status": "draft",
        "qualified": True,
        "eligible": True
    }
}

bid2 = {
    "data": {
        "tenderers": [
            {
                "address": {
                    "countryName": "Україна",
                    "locality": "м. Львів",
                    "postalCode": "79013",
                    "region": "м. Львів",
                    "streetAddress": "вул. Островського, 34"
                },
                "contactPoint": {
                    "email": "aagt@gmail.com",
                    "name": "Андрій Олексюк",
                    "telephone": "+380 (322) 91-69-30"
                },
                "identifier": {
                    "scheme": u"UA-EDR",
                    "id": u"00137226",
                    "uri": u"http://www.sc.gov.ua/"
                },
                "name": "ДКП «Книга»"
            }
        ],
        "qualified": True,
        "eligible": True,
        "value": {
            "amount": 501
        }
    }
}

question = {
    "data": {
        "author": {
            "address": {
                "countryName": "Україна",
                "locality": "м. Вінниця",
                "postalCode": "21100",
                "region": "м. Вінниця",
                "streetAddress": "вул. Островського, 33"
            },
            "contactPoint": {
                "email": "soleksuk@gmail.com",
                "name": "Сергій Олексюк",
                "telephone": "+380 (432) 21-69-30"
            },
            "identifier": {
                "id": "00137226",
                "legalName": "Державне комунальне підприємство громадського харчування «Школяр»",
                "scheme": "UA-EDR",
                "uri": "http://sch10.edu.vn.ua/"
            },
            "name": "ДКП «Школяр»"
        },
        "description": "Просимо додати таблицю потрібної калорійності харчування",
        "title": "Калорійність"
    }
}

answer = {
    "data": {
        "answer": "Таблицю додано в файлі \"Kalorijnist.xslx\""
    }
}

cancellation = {
    'data': {
        'reason': 'cancellation reason'
    }
}

test_max_uid = uuid4().hex

test_auction_maximum_data = test_auction_data.copy()
test_auction_maximum_data.update({
    "title_en": u"Cases with state awards",
    "title_ru": u"футляры к государственным наградам",
    "procuringEntity": {
        "name": u"Державне управління справами",
        "identifier": {
            "scheme": u"UA-EDR",
            "id": u"00037256",
            "uri": u"http://www.dus.gov.ua/"
        },
        "address": {
            "countryName": u"Україна",
            "postalCode": u"01220",
            "region": u"м. Київ",
            "locality": u"м. Київ",
            "streetAddress": u"вул. Банкова, 11, корпус 1"
        },
        "contactPoint": {
            "name": u"Державне управління справами",
            "telephone": u"0440000000"
        },
        'kind': 'general'
    },
    "items": [
        {
            "id": test_max_uid,
            "description": u"Земля для військовослужбовців",
            "classification": {
                "scheme": u"CPV",
                "id": u"45255120-6",
                "description": u"Земельні ділянки"
            },
            "unit": {
                "name": u"item",
                "code": u"44617100-9"
            },
            "quantity": 5
        }
    ],
})


test_complaint_data = {'data':
        {
            'title': 'complaint title',
            'description': 'complaint description',
            'author': bid["data"]["tenderers"][0]
        }
    }

prolongation_short = {
    'decisionID': 'ZM-937-99-92',
    'description': 'Prolongation description',
    'reason': 'other',
    'documents': [],
    'datePublished': get_now().isoformat(),
}

prolongation_long = {
    'decisionID': 'ZM-937-99-92-2',
    'description': 'Long prolongation description',
    'reason': 'other',
    'documents': [],
    'datePublished': get_now().isoformat(),
}


class AuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_data = test_auction_data
    initial_bids = test_bids
    docservice = True
    record_http = True

    def setUp(self):
        super(AuctionResourceTest, self).setUp()

        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('broker', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        if self.docservice:
            self.setUpDS()
            self.app.app.registry.docservice_url = 'http://public.docs-sandbox.ea.openprocurement.org'

        self.app.hostname = 'https://lb.api-sandbox.ea2.openprocurement.net/api/2.3/auctions'

    def generate_docservice_url(self):
        return super(AuctionResourceTest, self).generate_docservice_url().replace('/localhost/', '/public.docs-sandbox.ea.openprocurement.org/')

    def test_docs_acceleration(self):
        data = test_auction_data.copy()
        data['procurementMethodDetails'] = 'quick, accelerator=1440'
        data['submissionMethodDetails'] = 'quick'
        data['mode'] = 'test'
        data["auctionPeriod"] = {
            "startDate": (now + timedelta(minutes=5)).isoformat()
        }
        with open('docs/source/tutorial/auction-post-acceleration.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')
        auction = response.json['data']
        self.auction_id = auction['id']
        owner_token = response.json['access']['token']

    def test_docs_2pc(self):
        # Creating auction in draft status
        #
        data = test_auction_data.copy()
        data['status'] = 'draft'

        with open('docs/source/tutorial/auction-post-2pc.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')

        auction = response.json['data']
        self.auction_id = auction['id']
        owner_token = response.json['access']['token']

        # switch to 'active.tendering'

        with open('docs/source/tutorial/auction-patch-2pc.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token),
                                           {'data': {"status": 'active.tendering'}})
            self.assertEqual(response.status, '200 OK')

    def test_docs_tutorial(self):
        request_path = '/auctions?opt_pretty=1'

        # Exploring basic rules
        #

        with open('docs/source/tutorial/auction-listing.http', 'w') as self.app.file_obj:
            self.app.authorization = ('Basic', ('broker', ''))
            response = self.app.get('/auctions')
            self.assertEqual(response.status, '200 OK')
            self.app.file_obj.write("\n")

        with open('docs/source/tutorial/auction-post-attempt.http', 'w') as self.app.file_obj:
            response = self.app.post(request_path, 'data', status=415)
            self.assertEqual(response.status, '415 Unsupported Media Type')

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/tutorial/auction-post-attempt-json.http', 'w') as self.app.file_obj:
            self.app.authorization = ('Basic', ('broker', ''))
            response = self.app.post(
                request_path, 'data', content_type='application/json', status=422)
            self.assertEqual(response.status, '422 Unprocessable Entity')

        # Creating auction
        #

        with open('docs/source/tutorial/auction-post-attempt-json-data.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": test_auction_data})
            self.assertEqual(response.status, '201 Created')

        auction = response.json['data']
        owner_token = response.json['access']['token']
        access_header = {'X-Access-Token': str(owner_token)}

        with open('docs/source/tutorial/auction-switch-to-active-tendering.http', 'w') as self.app.file_obj:
            self.app.patch_json(
                '/auctions/{}'.format(auction['id']),
                {'data': {'status': 'active.tendering'}},
                headers=access_header
             )

        with open('docs/source/tutorial/blank-auction-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(auction['id']))
            self.assertEqual(response.status, '200 OK')

        self.app.get('/auctions')
        with open('docs/source/tutorial/initial-auction-listing.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions')
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/create-auction-procuringEntity.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/auctions?opt_pretty=1', {"data": test_auction_maximum_data})
            self.assertEqual(response.status, '201 Created')

        response = self.app.post_json('/auctions?opt_pretty=1', {"data": test_auction_data})
        self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-listing-after-procuringEntity.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions')
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        # Modifying auction
        #

        tenderPeriod_endDate = get_now() + timedelta(days=15, seconds=10)
        with open('docs/source/tutorial/patch-items-value-periods.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction['id'], owner_token), {'data':
                {
                    "tenderPeriod": {
                        "endDate": tenderPeriod_endDate.isoformat()
                    }
                }
            })

        self.app.get(request_path)
        with open('docs/source/tutorial/auction-listing-after-patch.http', 'w') as self.app.file_obj:
            self.app.authorization = None
            response = self.app.get(request_path)
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))
        self.auction_id = auction['id']

        # Uploading documentation
        #

        with open('docs/source/tutorial/upload-auction-notice.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'Notice.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "technicalSpecifications",
                    "description": "document description",
                }})
            self.assertEqual(response.status, '201 Created')

        doc_id = response.json["data"]["id"]
        with open('docs/source/tutorial/auction-documents.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents/{}'.format(
                self.auction_id, doc_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/upload-award-criteria.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'AwardCriteria.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        doc_id = response.json["data"]["id"]

        with open('docs/source/tutorial/auction-documents-2.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/update-award-criteria.http', 'w') as self.app.file_obj:
            response = self.app.put_json('/auctions/{}/documents/{}?acc_token={}'.format(self.auction_id, doc_id, owner_token),
                {'data': {
                    'title': u'AwardCriteria-2.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/auction-documents-3.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/upload-first-auction-illustration.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'first_illustration.jpeg',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'image/jpeg',
                    "documentType": "illustration",
                    "description": "First illustration description",
                    "index": 1
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-documents-4.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/upload-second-auction-illustration.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'second_illustration.jpeg',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'image/jpeg',
                    "documentType": "illustration",
                    "description": "Second illustration description",
                    "index": 2
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/upload-third-auction-illustration.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'third_illustration.jpeg',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'image/jpeg',
                    "documentType": "illustration",
                    "description": "Third illustration description",
                    "index": 2
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-documents-5.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/add-asset-familiarization-document.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/documents?acc_token={}'.format(self.auction_id, owner_token),
                {'data': {
                    'title': u'Familiarization with bank asset',
                    "documentType": "x_dgfAssetFamiliarization",
                    'accessDetails': "Familiar with asset: days, time, address",
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-documents-6.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/documents'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        # Enquiries
        #

        with open('docs/source/tutorial/ask-question.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/questions'.format(
                self.auction_id), question, status=201)
            question_id = response.json['data']['id']
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/answer-question.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/questions/{}?acc_token={}'.format(
                self.auction_id, question_id, owner_token), answer, status=200)
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/list-question.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/questions'.format(
                self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/get-answer.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/questions/{}'.format(
                self.auction_id, question_id))
            self.assertEqual(response.status, '200 OK')

        # Registering bid
        #

        self.app.authorization = ('Basic', ('broker', ''))
        bids_access = {}
        with open('docs/source/tutorial/register-bidder.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids'.format(
                self.auction_id), bid)
            bid1_id = response.json['data']['id']
            bids_access[bid1_id] = response.json['access']['token']
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/activate-bidder.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/bids/{}?acc_token={}'.format(
                self.auction_id, bid1_id, bids_access[bid1_id]), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')

        # Proposal Uploading
        #

        with open('docs/source/tutorial/upload-bid-proposal.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids/{}/documents?acc_token={}'.format(self.auction_id, bid1_id, bids_access[bid1_id]),
                {'data': {
                    'title': u'Proposal.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/bidder-documents.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/bids/{}/documents?acc_token={}'.format(
                self.auction_id, bid1_id, bids_access[bid1_id]))
            self.assertEqual(response.status, '200 OK')

        # Second bidder registration
        #

        with open('docs/source/tutorial/register-2nd-bidder.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/bids'.format(
                self.auction_id), bid2)
            bid2_id = response.json['data']['id']
            bids_access[bid2_id] = response.json['access']['token']
            self.assertEqual(response.status, '201 Created')

        # Auction
        #
        self.set_status('active.auction', {'status': 'active.tendering'})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {"data": {"id": self.auction_id}})
        self.assertIn('auctionUrl', response.json['data'])

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/tutorial/auction-url.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}'.format(self.auction_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/bidder-participation-url.http', 'w') as self.app.file_obj:
            response = self.app.get(
                '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid1_id, bids_access[bid1_id]))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/bidder2-participation-url.http', 'w') as self.app.file_obj:
            response = self.app.get(
                '/auctions/{}/bids/{}?acc_token={}'.format(self.auction_id, bid2_id, bids_access[bid2_id]))
            self.assertEqual(response.status, '200 OK')

        # Confirming qualification
        #

        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}/auction'.format(self.auction_id))
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                      {'data': {'bids': test_bids}})

        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        with open('docs/source/tutorial/get-awards.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(len(response.json['data']), 2)

        # get waiting award
        award = [i for i in response.json['data'] if i['status'] == 'pending.waiting'][0]
        award_id = award['id']

        with open('docs/source/qualification/award-waiting-cancel.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id, bids_access[award['bid_id']]), {"data": {"status": "cancelled"}})
            self.assertEqual(response.status, '200 OK')

        # get pending award
        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]

        with open('docs/source/tutorial/bidder-auction-protocol.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, bids_access[bid2_id]),
                {'data': {
                    'title': u'SignedAuctionProtocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "auctionProtocol",
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/owner-auction-protocol.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, owner_token),
                {'data': {
                    'title': u'SignedAuctionProtocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    "documentType": "auctionProtocol",
                }})
            self.assertEqual(response.status, '201 Created')

#        with open('docs/source/tutorial/verify-protocol.http', 'w') as self.app.file_obj:
#            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(self.auction_id, award_id, owner_token), {"data": {"status": "pending.payment"}})
#            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/confirm-qualification.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(self.auction_id, award_id, owner_token), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')

        response = self.app.get('/auctions/{}/contracts'.format(self.auction_id))
        self.contract_id = response.json['data'][0]['id']

        ####  Set contract value

        auction = self.db.get(self.auction_id)
        for i in auction.get('awards', []):
            i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
        self.db.save(auction)

        #### Setting contract period

        period_dates = {"period": {"startDate": (now).isoformat(), "endDate": (now + timedelta(days=365)).isoformat()}}
        with open('docs/source/tutorial/auction-contract-period.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
            self.auction_id, self.contract_id, owner_token), {'data': {'period': period_dates["period"]}})
        self.assertEqual(response.status, '200 OK')

        #### Uploading contract documentation
        #

        with open('docs/source/tutorial/auction-contract-upload-document.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, self.contract_id, owner_token),
                {'data': {
                    'title': u'contract_first_document.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-contract-get-documents.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/contracts/{}/documents'.format(
                self.auction_id, self.contract_id))
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/auction-contract-upload-second-document.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, self.contract_id, owner_token),
                {'data': {
                    'title': u'contract_second_document.doc',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/msword',
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/auction-contract-get-documents-again.http', 'w') as self.app.file_obj:
            response = self.app.get('/auctions/{}/contracts/{}/documents'.format(
                self.auction_id, self.contract_id))
        self.assertEqual(response.status, '200 OK')

        # signDocument
        with open('docs/source/tutorial/upload-contractSigned-doc.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/contracts/{}/documents?acc_token={}'.format(self.auction_id, self.contract_id, owner_token),
                {'data': {
                    'title': u'signDocument.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    'documentType': 'contractSigned'
                }})
            self.assertEqual(response.status, '201 Created')


        #### Setting contract signature date and Contract signing
        #

        auction = self.db.get(self.auction_id)
        for i in auction.get('awards', []):
            i['complaintPeriod']['endDate'] = i['complaintPeriod']['startDate']
        self.db.save(auction)

        with open('docs/source/tutorial/auction-contract-sign.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
                    self.auction_id, self.contract_id, owner_token), {'data': {'status': 'active', "dateSigned": get_now().isoformat()}})
            self.assertEqual(response.status, '200 OK')


        # Preparing the cancellation request
        #

        self.set_status('active.awarded')
        with open('docs/source/tutorial/prepare-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
                self.auction_id, owner_token), cancellation)
            self.assertEqual(response.status, '201 Created')

        cancellation_id = response.json['data']['id']

        # Filling cancellation with protocol and supplementary documentation
        #

        with open('docs/source/tutorial/upload-cancellation-doc.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/cancellations/{}/documents?acc_token={}'.format(self.auction_id, cancellation_id, owner_token),
                {'data': {
                    'title': u'Notice.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            cancellation_doc_id = response.json['data']['id']
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/tutorial/patch-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(
                self.auction_id, cancellation_id, cancellation_doc_id, owner_token), {'data': {"description": 'Changed description'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/update-cancellation-doc.http', 'w') as self.app.file_obj:
            response = self.app.put_json('/auctions/{}/cancellations/{}/documents/{}?acc_token={}'.format(self.auction_id, cancellation_id, cancellation_doc_id, owner_token),
                {'data': {
                    'title': u'Notice-2.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                }})
            self.assertEqual(response.status, '200 OK')

        # Activating the request and cancelling auction
        #

        with open('docs/source/tutorial/active-cancellation.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/cancellations/{}?acc_token={}'.format(
                self.auction_id, cancellation_id, owner_token), {"data": {"status": "active"}})
            self.assertEqual(response.status, '200 OK')

    def test_docs_disqualification(self):

        self.create_auction()
        self.set_status('active.tendering')

        # create bids
        self.set_status('active.tendering')
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.post_json('/auctions/{}/bids'.format(self.auction_id),
                                      {'data': {"qualified": True, 'tenderers': [bid["data"]["tenderers"][0]], "eligible": True}})
        self.initial_bids_tokens[response.json['data']['id']] = response.json['access']['token']
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.post_json('/auctions/{}/bids'.format(self.auction_id),
                                      {'data': {"qualified": True, 'tenderers': [bid2["data"]["tenderers"][0]], "value": {"amount": 475}, "eligible": True}})
        self.initial_bids_tokens[response.json['data']['id']] = response.json['access']['token']
        # get auction info
        self.set_status('active.auction')
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.get('/auctions/{}/auction'.format(self.auction_id))
        auction_bids_data = response.json['data']['bids']
        auction_bids_data[0]['value'] = {'amount': 500}
        auction_bids_data[1]['value'] = {'amount': 510}

        # posting auction results
        self.app.authorization = ('Basic', ('auction', ''))
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id),
                                      {'data': {'bids': auction_bids_data}})
        # get awards
        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')

        award = [i for i in response.json['data'] if i['status'] == 'pending'][0]
        award_id = award['id']
        bid_token = self.initial_bids_tokens[award['bid_id']]

        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, bid_token), {'data': {
                'title': u'auction_protocol.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
                'documentType': 'auctionProtocol',
            }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token), {'data': {
                'title': u'Unsuccessful_Reason.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
            }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, self.auction_token),
            {'data': {
                'title': u'RejectionProtocol.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
                'documentType': 'rejectionProtocol'
            }})
        self.assertEqual(response.status, '201 Created')

        response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token), {"data": {"status": "unsuccessful"}})
        self.assertEqual(response.status, '200 OK')

        response = self.app.get('/auctions/{}/awards'.format(self.auction_id))
        award = [i for i in response.json['data'] if i['status'] == 'pending'][0]
        award_id2 = award['id']
        bid_token = self.initial_bids_tokens[award['bid_id']]

        self.app.authorization = ('Basic', ('broker', ''))

        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id2, bid_token), {'data': {
                'title': u'auction_protocol.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/pdf',
                'documentType': 'auctionProtocol',
            }})
        self.assertEqual(response.status, '201 Created')

        with open('docs/source/qualification/upload-rejectionProtocol-doc.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id2, self.auction_token),
                {'data': {
                    'title': u'RejectionProtocol.pdf',
                    'url': self.generate_docservice_url(),
                    'hash': 'md5:' + '0' * 32,
                    'format': 'application/pdf',
                    'documentType': 'rejectionProtocol'
                }})
            self.assertEqual(response.status, '201 Created')

        with open('docs/source/qualification/award-active-disqualify.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
                self.auction_id, award_id2, self.auction_token), {"data": {"status": "unsuccessful", "title": "Disqualified", "description": "Candidate didn’t sign the auction protocol in 3 business days"}})
            self.assertEqual(response.status, '200 OK')
