# -*- coding: utf-8 -*-
import unittest
from openprocurement.auctions.core.tests.bidder import (
    AuctionBidderDocumentResourceTestMixin,
    AuctionBidderDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.bidder_blanks import create_auction_bidder
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest,
    test_organization,
)
from openprocurement.auctions.appraisal.tests.blanks.bidder_blanks import (
    # AppraisalAuctionBidderResourceTest
    create_auction_bidder_invalid,
    create_auction_bidder_without_value,
    patch_auction_bidder,
    get_auction_bidder,
    bid_id_signature_verified_active_bid,
    bid_id_signature_verified_draft_active_bid,
    delete_auction_bidder,
    get_auction_auctioners,
    bid_Administrator_change,
    # AppraisalAuctionBidderDocumentResourceTest
    create_auction_bidder_document_nopending,
    patch_auction_bidder_document
)


class AppraisalAuctionBidderResourceTest(BaseAppraisalAuctionWebTest):
    initial_status = 'active.tendering'
    test_financial_organization = test_organization

    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)
    test_create_auction_bidder_without_value = snitch(create_auction_bidder_without_value)
    test_patch_auction_bidder = snitch(patch_auction_bidder)
    test_get_auction_bidder = snitch(get_auction_bidder)
    test_bid_id_signature_verified_active_bid = snitch(bid_id_signature_verified_active_bid)
    test_bid_id_signature_verified_draft_active_bid = snitch(bid_id_signature_verified_draft_active_bid)
    test_delete_auction_bidder = snitch(delete_auction_bidder)
    test_get_auction_auctioners = snitch(get_auction_auctioners)
    test_bid_Administrator_change = snitch(bid_Administrator_change)


class AppraisalAuctionBidderDocumentResourceTest(BaseAppraisalAuctionWebTest,
                                               AuctionBidderDocumentResourceTestMixin):
    initial_status = 'active.tendering'

    def setUp(self):
        super(AppraisalAuctionBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [self.initial_organization], 'qualified': True, 'eligible': True}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']

    test_create_auction_bidder_document_nopending = snitch(create_auction_bidder_document_nopending)
    test_patch_auction_bidder_document = snitch(patch_auction_bidder_document)


class AppraisalAuctionBidderDocumentWithDSResourceTest(AppraisalAuctionBidderDocumentResourceTest,
                                                     AuctionBidderDocumentResourceTestMixin,
                                                     AuctionBidderDocumentWithDSResourceTestMixin
                                                     ):
    docservice = True


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionBidderResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionBidderDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionBidderDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
