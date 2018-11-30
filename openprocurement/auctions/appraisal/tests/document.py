# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.appraisal.tests.base import BaseInsiderAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.document import (
    AuctionDocumentResourceTestMixin,
    AuctionDocumentWithDSResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.document_blanks import (
    # InsiderAuctionDocumentWithDSResourceTest
    create_auction_document_vdr,
    put_auction_document_vdr,
)
from openprocurement.auctions.appraisal.tests.blanks.document_blanks import (
    patch_auction_document
)


class InsiderAuctionDocumentResourceTest(BaseInsiderAuctionWebTest, AuctionDocumentResourceTestMixin):
    docservice = False
    test_patch_auction_document = snitch(patch_auction_document)


class InsiderAuctionDocumentWithDSResourceTest(InsiderAuctionDocumentResourceTest, AuctionDocumentWithDSResourceTestMixin):
    docservice = True

    test_create_auction_document_vdr = snitch(create_auction_document_vdr)
    test_put_auction_document_vdr = snitch(put_auction_document_vdr)
    test_patch_auction_document = snitch(patch_auction_document)

    test_create_auction_document_pas = None
    test_create_auction_document_vdr = None
    test_put_auction_document_pas = None
    test_put_auction_document_vdr = None


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(InsiderAuctionDocumentResourceTest))
    tests.addTest(unittest.makeSuite(InsiderAuctionDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
