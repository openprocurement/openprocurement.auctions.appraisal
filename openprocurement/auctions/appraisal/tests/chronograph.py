# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.plugins.awarding.v3_1.tests.chronograph import (
    AuctionAwardSwitchResourceTestMixin
)


from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest, test_bids,
)
from openprocurement.auctions.appraisal.tests.blanks.chronograph_blanks import (
    # AppraisalAuctionSwitchAuctionResourceTest
    switch_to_auction,
    # AppraisalAuctionDontSwitchSuspendedAuction2ResourceTest
    switch_suspended_auction_to_auction,
)


class AppraisalAuctionSwitchAuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_bids = test_bids

    test_switch_to_auction = snitch(switch_to_auction)


class AppraisalAuctionAwardSwitchResourceTest(BaseAppraisalAuctionWebTest, AuctionAwardSwitchResourceTestMixin):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AppraisalAuctionAwardSwitchResourceTest, self).setUp()
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
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


class AppraisalAuctionAwardSwitch2ResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = test_bids

    def setUp(self):
        super(AppraisalAuctionAwardSwitch2ResourceTest, self).setUp()
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
                    "value": {"amount": 101 * (i + 1)},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.award = self.first_award = auction['awards'][0]
        # self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        # self.second_award_id = self.second_award['id']
        self.app.authorization = authorization


class AppraisalAuctionDontSwitchSuspendedAuction2ResourceTest(BaseAppraisalAuctionWebTest):
    initial_bids = test_bids

    test_switch_suspended_auction_to_auction = snitch(switch_suspended_auction_to_auction)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionSwitchAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionAuctionPeriodResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionAwardSwitchResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionAwardSwitch2ResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionDontSwitchSuspendedAuction2ResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
