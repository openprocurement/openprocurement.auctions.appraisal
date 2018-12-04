# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import get_now, update_logging_context
from openprocurement.auctions.core.validation import (
    validate_patch_auction_data,
    validate_data
)


def validate_auction_auction_data(request, **kwargs):
    data = validate_patch_auction_data(request)
    auction = request.validated['auction']
    if auction.status != 'active.auction':
        request.errors.add('body', 'data', 'Can\'t {} in current ({}) auction status'.format('report auction results' if request.method == 'POST' else 'update auction urls', auction.status))
        request.errors.status = 403
        return
    if data is not None:
        bids = data.get('bids', [])
        auction_bids_ids = [i.id for i in auction.bids]
        data['bids'] = [x for (y, x) in sorted(zip([auction_bids_ids.index(i['id']) for i in bids], bids))]
    else:
        data = {}
    if request.method == 'POST':
        now = get_now().isoformat()
        data['auctionPeriod'] = {'endDate': now}
    request.validated['data'] = data


# Items view validation
def validate_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model, "item")


def validate_patch_item_data(request, error_handler, **kwargs):
    update_logging_context(request, {'item_id': '__new__'})
    context = request.context if 'items' in request.context else request.context.__parent__
    model = type(context).items.model_class
    validate_data(request, model)


def validate_change_item(request, error_handler, **kwargs):

    context = request.context if 'items' in request.context else request.context.__parent__

    if context.status not in ['draft', 'active.tendering']:
        request.errors.add('body', 'mode', 'You can\'t change items in this status ({})'.format(context.status))
        request.errors.status = 403
        raise error_handler(request)
