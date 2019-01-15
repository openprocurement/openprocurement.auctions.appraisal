# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    BaseWebTest,
    BaseAuctionWebTest,
    test_organization as base_test_organization,
    test_auction_data, base_test_bids, test_document_data,
    MOCK_CONFIG as BASE_MOCK_CONFIG,
    test_item_data
)
from openprocurement.auctions.core.utils import (
    apply_data_patch,
    connection_mock_config,
    calculate_business_date
)


from openprocurement.auctions.appraisal.constants import DEFAULT_PROCUREMENT_METHOD_TYPE

now = datetime.now()

PARTIAL_MOCK_CONFIG = {
    "auctions.appraisal": {
        "use_default": True,
        "plugins": {
            "appraisal.migration": None
        },
        "migration": False,
        "aliases": [],
        "accreditation": {
            "create": [1],
            "edit": [2]
        }
    }
}
MOCK_CONFIG_PARTIAL_AUCTION = {
    "url": "http://auction-sandbox.openprocurement.org",
    "public_key": "fe3b3b5999a08e68dfe62687c2ae147f62712ceace58c1ffca8ea819eabcb5d1"
    }


MOCK_CONFIG = connection_mock_config(
    PARTIAL_MOCK_CONFIG,
    base=BASE_MOCK_CONFIG,
    connector=('plugins', 'api', 'plugins', 'auctions.core', 'plugins')
)

TEST_ROUTE_PREFIX = '/api/{}'.format(MOCK_CONFIG['config']['main']['api_version'])

MOCK_CONFIG = connection_mock_config(
    MOCK_CONFIG_PARTIAL_AUCTION,
    base=MOCK_CONFIG,
    connector=('config','auction')
)

test_appraisal_auction_data = deepcopy(test_auction_data)
test_appraisal_auction_data['auctionPeriod'] = {
    'startDate': calculate_business_date(now, timedelta(days=8), None, working_days=True).isoformat()
}
test_appraisal_auction_data['lotIdentifier'] = 'Q24421K222'
for item in test_appraisal_auction_data['items']:
    item['classification']['scheme'] = 'CPV'
    item['classification']['id'] = '51413000-0'

test_appraisal_auction_data['auctionParameters'] = {
    'type': 'insider',
    'dutchSteps': 88
}
test_appraisal_auction_data.update({
    'description': 'description of appraisal auction',
    'registrationFee': {
        'amount': 700.87,
        'currency': 'UAH'
    },
    'guarantee': {
        'amount': 1000.99,
        'currency': 'UAH'
    },
    'bankAccount': {
        'bankName': 'name of bank',
        'accountIdentification': [
            {
                'scheme': 'accountNumber',
                'id': '111111-8',
                'description': 'some description'
            }
        ]
    }
})

appraisal_document_data = deepcopy(test_document_data)
appraisal_document_data['documentType'] = 'x_dgfAssetFamiliarization'
del appraisal_document_data['hash']
appraisal_document_data['accessDetails'] = 'access details'

test_appraisal_auction_data['documents'] = [
    appraisal_document_data
]

del test_appraisal_auction_data['dgfID']
del test_appraisal_auction_data['dgfDecisionDate']
del test_appraisal_auction_data['dgfDecisionID']

schema_properties = {
    "code": "06000000-2",
    "version": "001",
    "properties": {
        "region": "Вінницька область",
        "district": "м.Вінниця",
        "cadastral_number": "1",
        "area": 1,
        "forms_of_land_ownership": ["державна"],
        "co_owners": False,
        "availability_of_utilities": True,
        "current_use": True
   }
 }

test_appraisal_auction_data_with_schema = deepcopy(test_appraisal_auction_data)
# test_appraisal_auction_data_with_schema['items'][0]['classification']['id'] = schema_properties['code']
# test_appraisal_auction_data_with_schema['items'][0]['schema_properties'] = schema_properties

test_organization = deepcopy(base_test_organization)
test_organization['additionalIdentifiers'] = [{
    "scheme": u"UA-FIN",
    "id": u"А01 457213"
}]

test_bids = []
for i in base_test_bids:
    bid = deepcopy(i)
    bid.update({'eligible': True})
    bid.update({'qualified': True})
    bid['tenderers'] = [test_organization]
    test_bids.append(bid)

test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]

for data in test_appraisal_auction_data, test_appraisal_auction_data_with_schema:
    data["procurementMethodType"] = DEFAULT_PROCUREMENT_METHOD_TYPE
    del data['minimalStep']


# Single item data
test_appraisal_item_data = deepcopy(test_item_data)
test_appraisal_item_data['id'] = '1' * 32
test_appraisal_item_data.update(
    {
        "unit": {"code": "code"},
        "classification": {
            "scheme": "CPV",
            "id": "73110000-6",
            "description": "Description"
        },
        "address": {"countryName": "Ukraine"},
        "quantity": 5,
        "additionalClassifications": [
            {
                "scheme": u"UA-EDR",
                "id": u"111111-4",
                "description": u"папір і картон гофровані, паперова й картонна тара"
            }
        ]
    }
)

class BaseAppraisalWebTest(BaseWebTest):

    """Base Web Test to test openprocurement.auctions.appraisal.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseAppraisalAuctionWebTest(BaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_appraisal_auction_data
    initial_organization = test_organization
    mock_config = MOCK_CONFIG

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": now.isoformat(),
                    "endDate": (now + timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": now.isoformat(),
                    "endDate": calculate_business_date(now, timedelta(days=8), None, working_days=True).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": now.isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=8),
                        None,
                        working_days=True
                    ).isoformat()
                },
                "auctionPeriod": {
                    "startDate": now.isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": now.isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=8),
                        None,
                        working_days=True
                    ).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=2)).isoformat(),
                    "endDate": now.isoformat()
                },
                "awardPeriod": {
                    "startDate": now.isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": now.isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": 
                        calculate_business_date(now, -timedelta(days=20), None, working_days=True).isoformat(),
                    "endDate": calculate_business_date(
                        calculate_business_date(now, -timedelta(days=20), None, working_days=True),
                        timedelta(days=8),
                        None,
                        working_days=True
                    ).isoformat()
                },
                "auctionPeriod": {
                    "startDate": calculate_business_date(
                        calculate_business_date(now, -timedelta(days=20), None, working_days=True),
                        timedelta(days=8),
                        None,
                        working_days=True
                    ).isoformat()
,
                    "endDate": calculate_business_date(
                        calculate_business_date(now, -timedelta(days=20), None, working_days=True),
                        timedelta(days=10),
                        None,
                        working_days=True
                    ).isoformat()

                },
                "awardPeriod": {
                    "startDate": calculate_business_date(
                        calculate_business_date(now, -timedelta(days=20), None, working_days=True),
                        timedelta(days=10),
                        None,
                        working_days=True
                    ).isoformat(),
                    "endDate": now.isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": now.isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=8),
                        None,
                        working_days=True
                    ).isoformat()
                },
                "auctionPeriod": {
                    "startDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=11),
                        None,
                        working_days=True
                    ).isoformat(),
                    "endDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=10),
                        None,
                        working_days=True
                    ).isoformat(),
                },
                "awardPeriod": {
                    "startDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=10),
                        None,
                        working_days=True
                    ).isoformat(),
                    "endDate": calculate_business_date(
                        now - timedelta(days=20),
                        timedelta(days=10),
                        None,
                        working_days=True
                    ).isoformat()
                }
            })

            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=11)).isoformat(),
                                "endDate": (now - timedelta(days=10)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)
        auction = self.db.get(self.auction_id)
        auction.update(apply_data_patch(auction, data))
        self.db.save(auction)
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        #response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response
