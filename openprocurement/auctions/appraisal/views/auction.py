# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    apply_patch,
    context_unpack,
    json_view,
    opresource,
    remove_draft_bids,
    save_auction,
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.views.mixins import AuctionAuctionResource
from openprocurement.auctions.core.validation import validate_insider_auction_auction_data

from openprocurement.auctions.appraisal.utils import invalidate_empty_bids, merge_auction_results


@opresource(name='appraisal:Auction Auction',
            collection_path='/auctions/{auction_id}/auction',
            path='/auctions/{auction_id}/auction/{auction_lot_id}',
            auctionsprocurementMethodType="appraisal",
            description="Appraisal auction auction data")
class AppraisalAuctionAuctionResource(AuctionAuctionResource):

    @json_view(permission='auction')
    def collection_get(self):
        if self.request.validated['auction_status'] not in ['active.tendering', 'active.auction']:
            self.request.errors.add('body', 'data', 'Can\'t get auction info in current ({}) auction status'.format(
                self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        return {'data': self.request.validated['auction'].serialize("auction_view")}

    @json_view(content_type="application/json", permission='auction', validators=(validate_insider_auction_auction_data, ))
    def collection_post(self):
        auction = self.context.serialize()
        adapter = self.request.registry.getAdapter(self.context, IAuctionManager)
        merge_auction_results(auction, self.request)
        apply_patch(self.request, save=False, src=self.request.validated['auction_src'])
        remove_draft_bids(self.request)
        auction = self.request.validated['auction']
        invalidate_empty_bids(auction)
        if any([i.status == 'active' for i in auction.bids]):
            self.request.content_configurator.start_awarding()
        else:
            adapter.pendify_auction_status('unsuccessful')
        if save_auction(self.request):
            self.LOGGER.info('Report auction results',
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_auction_post'}))
            return {'data': self.request.validated['auction'].serialize(self.request.validated['auction'].status)}
