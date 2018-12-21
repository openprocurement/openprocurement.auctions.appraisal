# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import update_logging_context, get_now
from openprocurement.auctions.core.validation import (
    validate_data,
    validate_json_data,
)


def validate_patch_auction_data(request, **kwargs):
    data = validate_json_data(request)

    if request.context.status == 'draft' and data.get('status') not in [None, 'active.tendering', 'draft']:
        request.errors.add('body', 'data', 'Can\'t switch auction in such status ({})'.format(data['status']))
        request.errors.status = 422
        return

    validate_data(request, type(request.auction), data=data)


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

    if get_now() > context.rectificationPeriod.endDate:
        request.errors.add('body', 'mode', 'You can\'t change items after rectification period')
        request.errors.status = 403
        raise error_handler(request)
