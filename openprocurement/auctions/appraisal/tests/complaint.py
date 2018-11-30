# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseInsiderAuctionWebTest
from openprocurement.auctions.core.tests.complaint import (
    AuctionComplaintResourceTestMixin,
    InsiderAuctionComplaintDocumentResourceTestMixin
)


@unittest.skip("option not available")
class InsiderAuctionComplaintResourceTest(BaseInsiderAuctionWebTest, AuctionComplaintResourceTestMixin):
    """Test Case for Auction Complaint resource"""


@unittest.skip("option not available")
class InsiderAuctionComplaintDocumentResourceTest(BaseInsiderAuctionWebTest, InsiderAuctionComplaintDocumentResourceTestMixin):

    def setUp(self):
        super(InsiderAuctionComplaintDocumentResourceTest, self).setUp()
        # Create complaint
        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.initial_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(InsiderAuctionComplaintDocumentResourceTest))
    tests.addTest(unittest.makeSuite(InsiderAuctionComplaintResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
