# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    json_view,
    context_unpack,
    APIResource,
    save_auction,
    opresource,
    apply_patch
)

from openprocurement.auctions.appraisal.validation import (
    validate_item_data,
    validate_patch_item_data,
    validate_change_item
)

post_validators = (validate_change_item, validate_item_data)
patch_validators = (validate_change_item, validate_patch_item_data)


@opresource(name='appraisal:Auction Items',
            collection_path='/auctions/{auction_id}/items',
            path='/auctions/{auction_id}/items/{item_id}',
            auctionsprocurementMethodType="appraisal",
            description="Auction related items")
class AuctionItemResource(APIResource):

    @json_view(permission='view_auction')
    def collection_get(self):
        """Lot Item List"""
        collection_data = [i.serialize("view") for i in self.context.items]
        return {'data': collection_data}

    @json_view(content_type="application/json", permission='edit_auction', validators=post_validators)
    def collection_post(self):
        """Lot Item Upload"""
        item = self.request.validated['item']
        self.context.items.append(item)
        if save_auction(self.request):
            self.LOGGER.info(
                'Created lot item {}'.format(item.id),
                extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_item_create'}, {'item_id': item.id})
            )
            self.request.response.status = 201
            item_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(
                                                            _route_name=item_route,
                                                            item_id=item.id,
                                                            _query={}
                                                            )
            return {'data': item.serialize("view")}

    @json_view(permission='view_auction')
    def get(self):
        """Lot Item Read"""
        item = self.request.validated['item']
        return {'data': item.serialize("view")}

    @json_view(content_type="application/json", permission='edit_auction', validators=patch_validators)
    def patch(self):
        """Lot Item Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            self.LOGGER.info(
                'Updated lot item {}'.format(self.request.context.id),
                extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_item_patch'})
            )
            return {'data': self.request.context.serialize("view")}
