# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import (
    BaseInsiderAuctionWebTest, test_bids,
)
from openprocurement.auctions.core.tests.cancellation import (
    AuctionCancellationResourceTestMixin,
    AuctionCancellationDocumentResourceTestMixin
)


class InsiderAuctionCancellationResourceTest(BaseInsiderAuctionWebTest,
                                             AuctionCancellationResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids


class InsiderAuctionCancellationDocumentResourceTest(BaseInsiderAuctionWebTest,
                                                     AuctionCancellationDocumentResourceTestMixin):

    def setUp(self):
        super(InsiderAuctionCancellationDocumentResourceTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
            self.auction_id, self.auction_token
        ), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(InsiderAuctionCancellationResourceTest))
    tests.addTest(unittest.makeSuite(InsiderAuctionCancellationDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
