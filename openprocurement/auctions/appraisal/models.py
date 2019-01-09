# -*- coding: utf-8 -*-
from functools import partial

from datetime import timedelta

from pyramid.security import Allow
from schematics.exceptions import ValidationError
from schematics.types import StringType, BooleanType, IntType, MD5Type
from schematics.types.compound import ModelType
from schematics.transforms import blacklist, whitelist

from schematics.types.serializable import serializable
from zope.interface import implementer

from openprocurement.api.models.schema import (
    SwiftsureProcuringEntity,
)
from openprocurement.api.models.schematics_extender import (
    DecimalType,
)
from openprocurement.auctions.core.interfaces import (
    IAuction
)

from openprocurement.auctions.core.models.roles import (
    item_roles
)
from openprocurement.auctions.core.models.schema import (
    Auction as BaseAuction,
    dgfCDB2Document,
    dgfCDB2Complaint as Complaint,
    dgfCancellation,
    AuctionParameters,
    ComplaintModelType,
    Model,
    ListType,
    Value,
    Period,
    get_auction,
    Bid as BaseBid,
    Feature,
    Lot,
    Guarantee,
    BankAccount,
    validate_features_uniq,
    validate_lots_uniq,
    validate_items_uniq,
    validate_not_available,
    validate_contract_type,
    dgfCDB2Item as Item,
    IsoDateTimeType
)
from openprocurement.auctions.core.plugins.awarding.v3_1.models import (
    Award
)
from openprocurement.auctions.core.plugins.contracting.v3_1.models import (
    Contract,
)
from openprocurement.auctions.core.utils import (
    rounding_shouldStartAfter_after_midnigth,
    AUCTIONS_COMPLAINT_STAND_STILL_TIME,
    calculate_business_date,
    SANDBOX_MODE,
    get_now,
    TZ,
)

from openprocurement.auctions.appraisal.constants import (
    DUTCH_PERIOD,
    QUICK_DUTCH_PERIOD,
    NUMBER_OF_STAGES,
    AUCTION_STATUSES,
    CONTRACT_TYPES
)

from openprocurement.auctions.appraisal.utils import generate_auction_url, calc_auction_end_time
from openprocurement.auctions.appraisal.roles import appraisal_auction_roles

validate_contract_type = partial(validate_contract_type, choices=CONTRACT_TYPES)


class RectificationPeriod(Period):
    invalidationDate = IsoDateTimeType()


class AppraisalDocument(dgfCDB2Document):
    documentOf = StringType(
        required=True,
        choices=[
            'auction',
            'item',
            'lot'],
        default='auction')
    documentType = StringType(choices=[
        'notice', 'technicalSpecifications', 'evaluationCriteria', 'clarifications',
        'bidders', 'illustration', 'x_PublicAssetCertificate', 'x_presentation',
        'x_nda', 'x_PlatformLegalDetails', 'x_dgfAssetFamiliarization', 'contractProforma'
    ])


class AppraisalBidDocument(AppraisalDocument):
    documentType = StringType(choices=[
        'commercialProposal', 'qualificationDocuments',
        'eligibilityDocuments', 'financialLicense'
    ])


class AppraisalCancellationDocument(AppraisalDocument):
    documentType = StringType(choices=['cancellationDetails'])


class AppraisalCancellation(dgfCancellation):
    documents = ListType(
        ModelType(AppraisalCancellationDocument),
        default=list(),
    )


class AppraisalAuctionParameters(AuctionParameters):
    dutchSteps = IntType(min_value=1, max_value=99, default=99)

    class Options:
        roles = {
            'create': blacklist()
        }


class AppraisalItem(Item):

    quantity = DecimalType(precision=-4, required=True)

    class Options:
        roles = item_roles


class AuctionAuctionPeriod(Period):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if auction.status not in ['active.tendering', 'active.auction']:
            return
        if self.startDate and get_now() > calc_auction_end_time(NUMBER_OF_STAGES, self.startDate):
            start_after = calc_auction_end_time(NUMBER_OF_STAGES, self.startDate)
        elif auction.enquiryPeriod and auction.enquiryPeriod.endDate:
            start_after = auction.enquiryPeriod.endDate
        else:
            return
        return rounding_shouldStartAfter_after_midnigth(start_after, auction).isoformat()

    def validate_startDate(self, data, startDate):
        auction = get_auction(data['__parent__'])
        if not auction.revisions and not startDate:
            raise ValidationError(u'This field is required.')


class Bid(BaseBid):
    class Options:
        roles = {
            'create': whitelist('tenderers', 'status', 'qualified', 'eligible'),
            'edit': whitelist('status', 'tenderers'),
        }

    status = StringType(choices=['active', 'draft', 'invalid'], default='active')
    qualified = BooleanType(required=True, choices=[True])
    documents = ListType(ModelType(AppraisalBidDocument), default=list())
    eligible = BooleanType(required=True, choices=[True])

    def validate_value(self, data, value):
        if isinstance(data['__parent__'], Model):
            auction = data['__parent__']
            if not value:
                return
            if auction.get('value').currency != value.currency:
                raise ValidationError(u"currency of bid should be identical to currency of value of auction")
            if auction.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                raise ValidationError(u"valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of auction")

    @serializable(serialized_name="participationUrl", serialize_when_none=False)
    def participation_url(self):
        if not self.participationUrl and self.status == "active":
            request = get_auction(self).__parent__.request
            url = generate_auction_url(request, bid_id=str(self.id))
            return url


class AppraisalAward(Award):
    items = ListType(ModelType(AppraisalItem))


class AppraisalContract(Contract):
    items = ListType(ModelType(AppraisalItem))


@implementer(IAuction)
class IAppraisalAuction(IAuction):
    """Marker interface for Appraisal auctions"""


@implementer(IAppraisalAuction)
class AppraisalAuction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    class Options:
        roles = appraisal_auction_roles
    _internal_type = "appraisal"
    description = StringType(required=True)
    awards = ListType(ModelType(AppraisalAward), default=list())
    cancellations = ListType(ModelType(AppraisalCancellation), default=list())
    complaints = ListType(ComplaintModelType(Complaint), default=list())
    contracts = ListType(ModelType(AppraisalContract), default=list())
    documents = ListType(ModelType(AppraisalDocument), default=list())  # All documents and attachments related to the auction.
    enquiryPeriod = ModelType(Period)  # The period during which enquiries may be made and will be answered.
    tenderPeriod = ModelType(Period)  # The period when the auction is open for submissions. The end date is the closing date for auction submissions.
    rectificationPeriod = ModelType(RectificationPeriod)
    tenderAttempts = IntType(choices=[1, 2, 3, 4, 5, 6, 7, 8])
    status = StringType(choices=AUCTION_STATUSES, default='draft')
    features = ListType(ModelType(Feature), validators=[validate_features_uniq, validate_not_available])
    lots = ListType(ModelType(Lot), default=list(), validators=[validate_lots_uniq, validate_not_available])
    items = ListType(ModelType(AppraisalItem), required=True, min_size=1, validators=[validate_items_uniq])
    suspended = BooleanType()
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.
    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})
    auctionParameters = ModelType(AppraisalAuctionParameters)
    minimalStep = ModelType(Value)
    registrationFee = ModelType(Guarantee, required=True)
    guarantee = ModelType(Guarantee, required=True)
    bankAccount = ModelType(BankAccount)
    procuringEntity = ModelType(SwiftsureProcuringEntity, required=True)
    lotIdentifier = StringType(required=True)

    def __acl__(self):
        return [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction_award'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_auction_documents'),
        ]

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'chronograph':
            role = 'chronograph'
        elif request.authenticated_role == 'auction':
            role = 'auction_{}'.format(request.method.lower())
        elif request.authenticated_role == 'convoy':
            role = 'convoy'
        elif request.authenticated_role == 'concierge':
            role = 'concierge'
        else:
            role = 'edit_{}'.format(request.context.status)
            if request.context.status == 'active.tendering' and get_now() < self.rectification_period.endDate:
                role += '_during_rectification_period'
        return role

    def initialize(self):
        pass

    def validate_value(self, data, value):
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    def validate_tenderPeriod(self, data, value):
        if not value:
            return

        new_startDate = value.get('startDate')
        new_endDate = value.get('endDate')

        # validate startDate
        if new_startDate and data.get('endDate') and data.get('endDate') < new_startDate:
            raise ValidationError(u"period should begin before its end")

        # validate endDate
        if new_endDate and data.get('startDate') and new_endDate > data['startDate']:
            min_end_date_limit = calculate_business_date(
                data['startDate'],
                timedelta(days=7),
                self,
                working_days=True
            )

            if new_endDate < min_end_date_limit:
                raise ValidationError(u"tenderPeriod should be at least 7 working days")


    @serializable(serialized_name="minimalStep", type=ModelType(Value))
    def auction_minimalStep(self):
        return Value(dict(amount=0))

    @serializable(serialized_name="rectificationPeriod", type=ModelType(RectificationPeriod), serialize_when_none=False)
    def rectification_period(self):
        if self.tenderPeriod:
            self.rectificationPeriod = RectificationPeriod() if not self.rectificationPeriod else self.rectificationPeriod
            self.rectificationPeriod.startDate = self.tenderPeriod.startDate
            self.rectificationPeriod.endDate = calculate_business_date(self.tenderPeriod.endDate, -timedelta(days=5), self, working_days=True)

            if self.rectificationPeriod.startDate > self.rectificationPeriod.endDate:
                self.rectificationPeriod.startDate = self.rectificationPeriod.endDate = None

        return self.rectificationPeriod

    @serializable(serialized_name="tenderPeriod", type=ModelType(Period))
    def tender_period(self):
        if self.tenderPeriod and self.auctionPeriod.startDate:
            end_date = calculate_business_date(self.auctionPeriod.startDate, DUTCH_PERIOD, self)
            if SANDBOX_MODE and self.submissionMethodDetails and 'quick' in self.submissionMethodDetails:
                end_date = self.auctionPeriod.startDate + QUICK_DUTCH_PERIOD
            if self.auctionPeriod.endDate and self.auctionPeriod.endDate <= self.tenderPeriod.endDate:
                end_date = self.auctionPeriod.endDate.astimezone(TZ)
            self.tenderPeriod.endDate = end_date
        return self.tenderPeriod

    @serializable(serialize_when_none=False)
    def next_check(self):
        if self.suspended:
            return None
        now = get_now()
        checks = []
        if self.status == 'active.tendering' and self.enquiryPeriod and self.enquiryPeriod.endDate:
            checks.append(self.enquiryPeriod.endDate.astimezone(TZ))
        elif not self.lots and self.status == 'active.auction' and self.auctionPeriod and self.auctionPeriod.startDate and not self.auctionPeriod.endDate:
            if now < self.auctionPeriod.startDate:
                checks.append(self.auctionPeriod.startDate.astimezone(TZ))
            elif now < calc_auction_end_time(NUMBER_OF_STAGES, self.auctionPeriod.startDate).astimezone(TZ):
                checks.append(calc_auction_end_time(NUMBER_OF_STAGES, self.auctionPeriod.startDate).astimezone(TZ))
        elif not self.lots and self.status == 'active.qualification':
            for award in self.awards:
                if award.status == 'pending':
                    checks.append(award.verificationPeriod.endDate.astimezone(TZ))
        elif not self.lots and self.status == 'active.awarded' and not any([
                i.status in self.block_complaint_status
                for i in self.complaints
            ]) and not any([
                i.status in self.block_complaint_status
                for a in self.awards
                for i in a.complaints
            ]):
            standStillEnds = [
                a.complaintPeriod.endDate.astimezone(TZ)
                for a in self.awards
                if a.complaintPeriod.endDate
            ]
            for award in self.awards:
                if award.status == 'active':
                    checks.append(award.signingPeriod.endDate.astimezone(TZ))

            last_award_status = self.awards[-1].status if self.awards else ''
            if standStillEnds and last_award_status == 'unsuccessful':
                checks.append(max(standStillEnds))
        if self.status.startswith('active'):
            from openprocurement.auctions.core.utils import calculate_business_date
            for complaint in self.complaints:
                if complaint.status == 'claim' and complaint.dateSubmitted:
                    checks.append(calculate_business_date(complaint.dateSubmitted, AUCTIONS_COMPLAINT_STAND_STILL_TIME, self))
                elif complaint.status == 'answered' and complaint.dateAnswered:
                    checks.append(calculate_business_date(complaint.dateAnswered, AUCTIONS_COMPLAINT_STAND_STILL_TIME, self))
            for award in self.awards:
                for complaint in award.complaints:
                    if complaint.status == 'claim' and complaint.dateSubmitted:
                        checks.append(calculate_business_date(complaint.dateSubmitted, AUCTIONS_COMPLAINT_STAND_STILL_TIME, self))
                    elif complaint.status == 'answered' and complaint.dateAnswered:
                        checks.append(calculate_business_date(complaint.dateAnswered, AUCTIONS_COMPLAINT_STAND_STILL_TIME, self))
        return min(checks).isoformat() if checks else None

