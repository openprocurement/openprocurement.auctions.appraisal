# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)


class AppraisalAuctionDocumentResourceTest(BaseAppraisalAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False


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
