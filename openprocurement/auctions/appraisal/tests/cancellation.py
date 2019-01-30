# -*- coding: utf-8 -*-
import unittest
import mock

from datetime import timedelta
from openprocurement.auctions.core.utils import get_now

from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.appraisal.tests.base import (
    BaseAppraisalAuctionWebTest, test_bids
)
from openprocurement.auctions.core.tests.cancellation import (
    AuctionCancellationResourceTestMixin,
    AuctionCancellationDocumentResourceTestMixin
)

from openprocurement.auctions.appraisal.tests.blanks.cancellation_blanks import check_cancellation_document_type_required


class AppraisalAuctionCancellationResourceTest(BaseAppraisalAuctionWebTest,
                                             AuctionCancellationResourceTestMixin):
    initial_status = 'active.tendering'
    initial_bids = test_bids


class BaseCancellationDocumentTest(BaseAppraisalAuctionWebTest):

    def setUp(self):
        super(BaseCancellationDocumentTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations?acc_token={}'.format(
            self.auction_id, self.auction_token
        ), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']

        self.patch_document_type_required_from = mock.patch(
            'openprocurement.auctions.appraisal.models.DOCUMENT_TYPE_REQUIRED_FROM',
            get_now() + timedelta(days=10)
        )
        self.mock_document_type_required_from = self.patch_document_type_required_from.start()

    def tearDown(self):
        self.patch_document_type_required_from.stop()


class AppraisalAuctionCancellationDocumentResourceTest(BaseCancellationDocumentTest,
                                                     AuctionCancellationDocumentResourceTestMixin):
    pass


class AppraisalAuctionCancellationWithDSDocumentResourceTest(BaseCancellationDocumentTest):
    docservice = True

    test_check_cancellation_document_type_required = snitch(check_cancellation_document_type_required)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AppraisalAuctionCancellationResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionCancellationDocumentResourceTest))
    tests.addTest(unittest.makeSuite(AppraisalAuctionCancellationWithDSDocumentResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
