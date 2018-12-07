# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest
from openprocurement.auctions.core.tests.plugins.transferring.mixins import AuctionOwnershipChangeTestCaseMixin
from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.appraisal.tests.blanks.transferring_blanks import (
    new_owner_can_change,
)


class AuctionOwnershipChangeResourceTest(BaseAppraisalAuctionWebTest, AuctionOwnershipChangeTestCaseMixin):
    initial_status = 'active.tendering'

    test_new_owner_can_change = snitch(new_owner_can_change)

    def setUp(self):
        super(AuctionOwnershipChangeResourceTest, self).setUp()
        self.not_used_transfer = self.create_transfer()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AuctionOwnershipChangeResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
