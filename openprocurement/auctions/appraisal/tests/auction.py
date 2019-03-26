# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.blanks.auction_blanks import (
    get_auction_auction_not_found,
    post_auction_auction_document
)
from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest,
    test_bids,
    test_organization,
    test_appraisal_auction_data
)
from openprocurement.auctions.appraisal.tests.blanks.auction_blanks import (
    # AppraisalAuctionAuctionResourceTest
    get_auction_auction,
    post_auction_auction,
    patch_auction_auction,
    # AppraisalAuctionBidInvalidationAuctionResourceTest
    post_auction_all_invalid_bids,
    post_auction_one_bid_without_value,
    post_auction_zero_bids,
    post_auction_one_valid_bid,
    # AppraisalAuctionDraftBidAuctionResourceTest
    post_auction_all_draft_bids,
    # AppraisalAuctionSameValueAuctionResourceTest
    post_auction_auction_not_changed,
    post_auction_auction_reversed,
    # AppraisalAuctionNoBidsResourceTest
    post_auction_no_bids,
    # AppraisalAuctionBridgePatchPeriod
    set_auction_period,
    reset_auction_period,
)


class AppraisalAuctionAuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_bids

    test_get_auction_auction_not_found = snitch(get_auction_auction_not_found)
    test_get_auction_auction = snitch(get_auction_auction)
    test_post_auction_auction = snitch(post_auction_auction)
    test_patch_auction_auction = snitch(patch_auction_auction)
    test_post_auction_auction_document = snitch(post_auction_auction_document)


class AppraisalAuctionBidInvalidationAuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.auction'
    initial_data = test_appraisal_auction_data
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            "eligible": True
        }
        for i in range(3)
    ]

    test_post_auction_all_invalid_bids = unittest.skip("zero minimalstep")(snitch(post_auction_all_invalid_bids))
    test_post_auction_one_bid_without_value = snitch(post_auction_one_bid_without_value)
    test_post_auction_zero_bids = snitch(post_auction_zero_bids)
    test_post_auction_one_valid_bid = snitch(post_auction_one_valid_bid)


class AppraisalAuctionDraftBidAuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            "eligible": True,
            'status': 'draft'
        }
        for i in range(3)
    ]

    test_post_auction_all_draft_bids = snitch(post_auction_all_draft_bids)


class AppraisalAuctionSameValueAuctionResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            'qualified': True,
            'eligible': True
        }
        for i in range(3)
    ]

    test_post_auction_auction_not_changed = snitch(post_auction_auction_not_changed)
    test_post_auction_auction_reversed = snitch(post_auction_auction_reversed)


class AppraisalAuctionNoBidsResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.auction'

    test_post_auction_zero_bids = snitch(post_auction_no_bids)


class AppraisalAuctionBridgePatchPeriod(BaseAppraisalAuctionWebTest):
    initial_status = 'active.tendering'

    test_set_auction_period = snitch(set_auction_period)
    test_reset_auction_period = snitch(reset_auction_period)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionBidInvalidationAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionDraftBidAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionSameValueAuctionResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionNoBidsResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionBridgePatchPeriod))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
