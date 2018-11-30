# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest
from openprocurement.auctions.core.tests.plugins.transferring.mixins import AuctionOwnershipChangeTestCaseMixin


class AuctionOwnershipChangeResourceTest(BaseAppraisalAuctionWebTest, AuctionOwnershipChangeTestCaseMixin):

    def setUp(self):
        super(AuctionOwnershipChangeResourceTest, self).setUp()
        self.not_used_transfer = self.create_transfer()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionOwnershipChangeResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
