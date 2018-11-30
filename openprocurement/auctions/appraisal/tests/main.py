# -*- coding: utf-8 -*-

import unittest

from openprocurement.auctions.appraisal.tests import (
    auction, award, bidder, cancellation, chronograph, complaint, contract, document, migration, tender, question
)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(auction.suite())
    suite.addTest(award.suite())
    suite.addTest(bidder.suite())
    suite.addTest(cancellation.suite())
    suite.addTest(chronograph.suite())
    suite.addTest(complaint.suite())
    suite.addTest(contract.suite())
    suite.addTest(document.suite())
    suite.addTest(migration.suite())
    suite.addTest(question.suite())
    suite.addTest(tender.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
