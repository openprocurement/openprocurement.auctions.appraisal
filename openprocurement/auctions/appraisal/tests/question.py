# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.question import AuctionQuestionResourceTestMixin

from openprocurement.auctions.appraisal.tests.base import BaseAppraisalAuctionWebTest


class AppraisalAuctionQuestionResourceTest(BaseAppraisalAuctionWebTest, AuctionQuestionResourceTestMixin):
    pass


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionQuestionResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
