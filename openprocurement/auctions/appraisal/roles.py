# -*- coding: utf-8 -*-
from schematics.transforms import (
    blacklist,
    whitelist
)

from openprocurement.auctions.core.models.roles import (
    auction_embedded_role,
    edit_role,
    Administrator_role,
    enquiries_role,
    view_role,
    auction_view_role
)

appraisal_auction_roles = {
    'create': (
        auction_embedded_role +
        blacklist(
            '_attachments',
            'status',
            'auctionID',
            'auctionUrl',
            'awardCriteria',
            'awardPeriod',
            'awards',
            'bids',
            'cancellations',
            'complaints',
            'contracts',
            'date',
            'dateModified',
            'doc_id',
            'documents',
            'eligibilityCriteria',
            'eligibilityCriteria_en',
            'eligibilityCriteria_ru',
            'enquiryPeriod',
            'numberOfBidders',
            'owner',
            'procurementMethod',
            'questions',
            'revisions',
            'submissionMethod',
            'suspended',
            'tenderPeriod',
            'rectificationPeriod'
        )
    ),
    'edit_active.tendering_during_rectification_period': (
        edit_role +
        blacklist(
            'auctionParameters',
            'auction_guarantee',
            'auction_minimalStep',
            'auction_value',
            'awardCriteriaDetails',
            'awardCriteriaDetails_en',
            'awardCriteriaDetails_ru',
            'eligibilityCriteria',
            'eligibilityCriteria_en',
            'eligibilityCriteria_ru',
            'enquiryPeriod',
            'procurementMethodRationale',
            'procurementMethodRationale_en',
            'procurementMethodRationale_ru',
            'procuringEntity',
            'rectificationPeriod',
            'submissionMethodDetails',
            'submissionMethodDetails_en',
            'submissionMethodDetails_ru',
            'suspended',
            'tenderPeriod',
            'rectificationPeriod'
        )
    ),
    'edit_active.tendering': whitelist(),
    'Administrator': (
        Administrator_role +
        whitelist(
            'auctionParameters',
            'awards',
            'suspended',
        )
    ),
    'pending.verification': enquiries_role,
    'invalid': view_role,
    'edit_pending.verification': whitelist(),
    'edit_invalid': whitelist(),
    'convoy': whitelist(
        'documents',
        'items',
        'status',
    ),
    'auction_view': (
        auction_view_role +
        whitelist(
            'auctionParameters',
            'bankAccount',
            'minNumberOfQualifiedBids',
            'registrationFee',
        )
    ),
}
