import logging

from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import IContentConfigurator
from openprocurement.auctions.core.interfaces import IAuctionManager

from openprocurement.auctions.appraisal.models import AppraisalAuction, IAppraisalAuction
from openprocurement.auctions.appraisal.adapters import (
    AuctionAppraisalConfigurator,
    AuctionAppraisalManagerAdapter
)
from openprocurement.auctions.appraisal.constants import (
    VIEW_LOCATIONS,
    DEFAULT_PROCUREMENT_METHOD_TYPE,
    DEFAULT_LEVEL_OF_ACCREDITATION
)

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    procurement_method_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        procurement_method_types.append(DEFAULT_PROCUREMENT_METHOD_TYPE)
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(AppraisalAuction,
                                                 procurementMethodType)

    for view_module in VIEW_LOCATIONS:
        config.scan(view_module)

    config.registry.registerAdapter(
        AuctionAppraisalConfigurator,
        (IAppraisalAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AuctionAppraisalManagerAdapter,
        (IAppraisalAuction, ),
        IAuctionManager
    )

    LOGGER.info("Included openprocurement.auctions.appraisal plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_config.get('accreditation'):
        config.registry.accreditation['auction'][AppraisalAuction._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][AppraisalAuction._internal_type] = plugin_config['accreditation']
