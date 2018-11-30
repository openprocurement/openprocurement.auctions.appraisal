# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.question import AuctionQuestionResourceTestMixin

from openprocurement.auctions.appraisal.tests.base import BaseInsiderAuctionWebTest


class InsiderAuctionQuestionResourceTest(BaseInsiderAuctionWebTest, AuctionQuestionResourceTestMixin):
    pass


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(InsiderAuctionQuestionResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
