# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.tender import (
    AuctionResourceTestMixin,
    DgfInsiderResourceTestMixin,
    ExtractCredentialsMixin
)
from openprocurement.auctions.core.tests.blanks.tender_blanks import (
    # AuctionTest
    simple_add_auction,
    # AuctionProcessTest
    one_valid_bid_auction,
    one_invalid_bid_auction,
)

from openprocurement.auctions.core.constants import DGF_ELIGIBILITY_CRITERIA

from openprocurement.auctions.appraisal.models import AppraisalAuction
from openprocurement.auctions.appraisal.tests.base import (
    test_insider_auction_data,
    test_organization,
    BaseAppraisalAuctionWebTest, BaseAppraisalWebTest,
    test_insider_auction_data_with_schema
)
from openprocurement.auctions.appraisal.tests.blanks.tender_blanks import (
    # AppraisalAuctionTest
    create_role,
    edit_role,
    # AppraisalAuctionResourceTest
    create_auction_invalid,
    create_auction_auctionPeriod,
    create_auction_generated,
    create_auction,
    check_daylight_savings_timezone,
    # AppraisalAuctionProcessTest
    first_bid_auction,
    auctionUrl_in_active_auction,
    suspended_auction
)


class AppraisalAuctionTest(BaseAppraisalWebTest):
    auction = AppraisalAuction
    initial_data = test_insider_auction_data

    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class AppraisalAuctionResourceTest(BaseAppraisalWebTest, AuctionResourceTestMixin, DgfInsiderResourceTestMixin):
    initial_status = 'active.tendering'
    initial_data = test_insider_auction_data
    initial_organization = test_organization
    eligibility_criteria = DGF_ELIGIBILITY_CRITERIA
    test_financial_organization = test_organization

    test_check_daylight_savings_timezone = snitch(check_daylight_savings_timezone)
    test_create_auction_invalid = snitch(create_auction_invalid)
    test_create_auction_auctionPeriod = snitch(create_auction_auctionPeriod)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction = snitch(create_auction)


class AppraisalAuctionProcessTest(BaseAppraisalAuctionWebTest):
    test_financial_organization = test_organization
    docservice = True

    # setUp = BaseAppraisalWebTest.setUp
    def setUp(self):
        super(AppraisalAuctionProcessTest.__bases__[0], self).setUp()

    def test_auctionParameters(self):
        data = deepcopy(self.initial_data)
        self.app.authorization = ('Basic', ('broker', ''))

        # Create auction with invalid auctionParameters
        data['auctionParameters'] = {'dutchSteps': 42, 'type': 'dutch'}
        response = self.app.post_json('/auctions', {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'], [
            {
                "location": "body", "name": "auctionParameters", "description": {
                    "type": ["Value must be one of ['english', 'insider']."]
                }
            }
        ])

        data['auctionParameters'] = {'dutchSteps': 112, 'type': 'insider'}
        response = self.app.post_json('/auctions', {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'], [
            {
                "location": "body", "name": "auctionParameters", "description": {
                    "dutchSteps": ["Int value should be less than 99."]
                }
            }
        ])

        # Create auction with auctionParameters values
        data = deepcopy(self.initial_data)
        response = self.app.post_json('/auctions', {'data': data})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['data']['auctionParameters']['dutchSteps'],
            data['auctionParameters']['dutchSteps']
        )
        self.assertEqual(response.json['data']['auctionParameters']['type'], 'insider')
        auction_id = self.auction_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        #  Patch auctionParameters (Not allowed)
        response = self.app.patch_json('/auctions/{}?acc_token={}'.format(auction_id, owner_token), {
            'data': {'auctionParameters': {'dutchSteps': 50, 'type': 'english'}}
        })
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(
            response.json['data']['auctionParameters']['dutchSteps'],
            data['auctionParameters']['dutchSteps']
        )
        self.assertEqual(response.json['data']['auctionParameters']['type'], 'insider')

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(auction_id), {
            'data': {'auctionParameters': {'dutchSteps': 99, 'type': 'insider'}}
        })
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['auctionParameters']['dutchSteps'], 99)
        self.assertEqual(response.json['data']['auctionParameters']['type'], 'insider')

    test_one_valid_bid_auction = unittest.skip('option not available')(snitch(one_valid_bid_auction))
    test_one_invalid_bid_auction = unittest.skip('option not available')(snitch(one_invalid_bid_auction))
    test_first_bid_auction = snitch(first_bid_auction)
    test_auctionUrl_in_active_auction = snitch(auctionUrl_in_active_auction)
    test_suspended_auction = snitch(suspended_auction)


class AppraisalAuctionSchemaResourceTest(AppraisalAuctionResourceTest):
    initial_data = test_insider_auction_data_with_schema

    # def test_create_auction_with_bad_schemas_code(self):
    #     response = self.app.get('/auctions')
    #     self.assertEqual(response.status, '200 OK')
    #     self.assertEqual(len(response.json['data']), 0)
    #     bad_initial_data = deepcopy(self.initial_data)
    #     bad_initial_data['items'][0]['classification']['id'] = "42124210-6"
    #     response = self.app.post_json('/auctions', {"data": bad_initial_data},
    #                                   status=422)
    #     self.assertEqual(response.status, '422 Unprocessable Entity')
    #     self.assertEqual(response.content_type, 'application/json')
    #     self.assertEqual(response.json['errors'],
    #                      [{
    #                          "location": "body",
    #                          "name": "items",
    #                          "description": [{
    #                              "schema_properties": ["classification id mismatch with schema_properties code"]
    #                          }]
    #                      }])


class AppraisalAuctionSchemaProcessTest(AppraisalAuctionProcessTest):
    initial_data = test_insider_auction_data_with_schema


class AuctionExtractCredentialsTest(BaseAppraisalAuctionWebTest, ExtractCredentialsMixin):
    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AppraisalAuctionProcessTest))
    suite.addTest(unittest.makeSuite(AppraisalAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AppraisalAuctionTest))
    suite.addTest(unittest.makeSuite(AppraisalAuctionSchemaResourceTest))
    suite.addTest(unittest.makeSuite(AppraisalAuctionSchemaProcessTest))
    suite.addTest(unittest.makeSuite(AuctionExtractCredentialsTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
