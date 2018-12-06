# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)

from openprocurement.auctions.appraisal.tests.blanks.document_blanks import patch_auction_document


class AppraisalAuctionDocumentResourceTest(BaseAppraisalAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False

    test_patch_auction_document = snitch(patch_auction_document)


class AppraisalAuctionDocumentWithDSResourceTest(AppraisalAuctionDocumentResourceTest, AuctionDocumentWithDSResourceTestMixin):
    docservice = True

    test_create_auction_document_pas = None
    test_put_auction_document_pas = None


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
