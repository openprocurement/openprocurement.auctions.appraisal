# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    apply_patch,
    context_unpack,
    json_view,
    opresource,
    save_auction,
)
from openprocurement.auctions.appraisal.validation import (
    validate_patch_auction_data, validate_update_auction_in_not_allowed_status
)
from openprocurement.auctions.core.interfaces import IAuctionManager
from openprocurement.auctions.core.views.mixins import AuctionResource

from openprocurement.auctions.appraisal.utils import check_status


patch_validators = (validate_update_auction_in_not_allowed_status, validate_patch_auction_data)


@opresource(name='appraisal:Auction',
            path='/auctions/{auction_id}',
            auctionsprocurementMethodType="appraisal",
            description="Open Contracting compatible data exchange format. See http://ocds.open-contracting.org/standard/r/master/#auction for more info")
class AppraisalAuctionResource(AuctionResource):

    @json_view(content_type="application/json", validators=patch_validators, permission='edit_auction')
    def patch(self):
        self.request.registry.getAdapter(self.context, IAuctionManager).change_auction(self.request)
        auction = self.context

        if self.request.authenticated_role == 'chronograph' and not auction.suspended:
            apply_patch(self.request, save=False, src=self.request.validated['auction_src'])
            check_status(self.request)
            save_auction(self.request)
        else:
            apply_patch(self.request, src=self.request.validated['auction_src'])

        self.LOGGER.info('Updated auction {}'.format(auction.id),
                         extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_patch'}))
        return {'data': auction.serialize(auction.status)}
