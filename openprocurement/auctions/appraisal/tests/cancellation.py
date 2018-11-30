# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest, test_bids,
)
from openprocurement.auctions.core.tests.cancellation import (
    AuctionCancellationResourceTestMixin,
    AuctionCancellationDocumentResourceTestMixin
)


class AppraisalAuctionCancellationResourceTest(BaseAppraisalAuctionWebTest,
                                             AuctionCancellationResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids


class AppraisalAuctionCancellationDocumentResourceTest(BaseAppraisalAuctionWebTest,
                                                     AuctionCancellationDocumentResourceTestMixin):

    def setUp(self):
        super(AppraisalAuctionCancellationDocumentResourceTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
            self.auction_id, self.auction_token
        ), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionCancellationResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionCancellationDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
