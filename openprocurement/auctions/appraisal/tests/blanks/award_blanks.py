# -*- coding: utf-8 -*-
from iso8601 import parse_date

from openprocurement.auctions.core.utils import (
    get_now, calculate_business_date, TZ
)
from openprocurement.auctions.appraisal.constants import (
    SIGNING_PERIOD_PARAMS
)


def check_signing_period(self):
    response = self.app.get(
        '/auctions/{}'.format(self.auction_id),
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertEqual('active.qualification', auction["status"])
    first_award = auction['awards'][0]

    signing_period_start = parse_date(first_award['signingPeriod']['startDate']).astimezone(TZ)
    signing_period_end = parse_date(first_award['signingPeriod']['endDate']).astimezone(TZ)
    expected_end = calculate_business_date(
        start=signing_period_start,
        context=auction,
        **SIGNING_PERIOD_PARAMS
    )

    self.assertEqual(signing_period_end, expected_end)
