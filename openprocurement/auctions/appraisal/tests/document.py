# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)

from openprocurement.auctions.appraisal.tests.blanks.document_blanks import (
    patch_auction_document,
    check_bids_invalidation,
    put_access_details
)


class AppraisalAuctionDocumentResourceTest(BaseAppraisalAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False
    initial_status = 'active.tendering'

    test_patch_auction_document = snitch(patch_auction_document)
    test_check_bids_invalidation = snitch(check_bids_invalidation)


class AppraisalAuctionDocumentWithDSResourceTest(AppraisalAuctionDocumentResourceTest, AuctionDocumentWithDSResourceTestMixin):
    docservice = True
    initial_status = 'active.tendering'

    test_create_auction_document_pas = None
    test_put_auction_document_pas = None
    test_put_access_details = snitch(put_access_details)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
