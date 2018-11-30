# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.core.views.mixins import AuctionCancellationDocumentResource


@opresource(name='appraisal:Auction Cancellation Documents',
            collection_path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents',
            path='/auctions/{auction_id}/cancellations/{cancellation_id}/documents/{document_id}',
            auctionsprocurementMethodType="appraisal",
            description="Appraisal auction cancellation documents")
class InsiderAuctionCancellationDocumentResource(AuctionCancellationDocumentResource):
    pass
