# -*- coding: utf-8 -*-
from datetime import timedelta

from openprocurement.auctions.appraisal.models import AppraisalAuction
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.core.plugins.awarding.v3_2.adapters import (
    AwardingV3_2ConfiguratorMixin
)
from openprocurement.auctions.core.utils import (
    calculate_business_date,
    SANDBOX_MODE,
    get_now,
    TZ,
)
from openprocurement.auctions.appraisal.constants import (
    DUTCH_PERIOD,
    QUICK_DUTCH_PERIOD
)


class AuctionAppraisalConfigurator(AuctionConfigurator,
                                   AwardingV3_2ConfiguratorMixin):
    name = 'Auction Appraisal Configurator'
    model = AppraisalAuction
    pending_admission_for_one_bid = False


class AuctionAppraisalManagerAdapter(AuctionManagerAdapter):
    create_validation = []

    def create_auction(self, request):
        self._validate(request, self.create_validation)

        auction = request.validated['auction']

        if not auction.enquiryPeriod:
            auction.enquiryPeriod = type(auction).enquiryPeriod.model_class()
        if not auction.tenderPeriod:
            auction.tenderPeriod = type(auction).tenderPeriod.model_class()

        now = get_now()
        start_date = TZ.localize(auction.auctionPeriod.startDate.replace(tzinfo=None))
        auction.auctionPeriod.startDate = None
        auction.auctionPeriod.endDate = None

        auction.tenderPeriod.startDate = auction.enquiryPeriod.startDate = now

        # Specific logic to make enquiryPeriod.endDate be one day before auctionPeriod.startDate and be set 20 hour
        pause_between_periods = start_date - (start_date.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1))
        auction.enquiryPeriod.endDate = calculate_business_date(start_date, -pause_between_periods, auction).astimezone(TZ)

        # Specific logic to make tenderPeriod.endDate be from enquiryPeriod.endDate until end of auction
        time_before_tendering_end = (start_date.replace(hour=9, minute=30, second=0, microsecond=0) + DUTCH_PERIOD) - auction.enquiryPeriod.endDate
        auction.tenderPeriod.endDate = calculate_business_date(auction.enquiryPeriod.endDate, time_before_tendering_end, auction)

        if SANDBOX_MODE and auction.submissionMethodDetails and 'quick' in auction.submissionMethodDetails:
            auction.tenderPeriod.endDate = (auction.enquiryPeriod.endDate + QUICK_DUTCH_PERIOD).astimezone(TZ)

        auction.auctionPeriod.startDate = None
        auction.auctionPeriod.endDate = None
        auction.date = now
        if not auction.auctionParameters:
            auction.auctionParameters = type(auction).auctionParameters.model_class()

    def change_auction(self, request):
        pass
