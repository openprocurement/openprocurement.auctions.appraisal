# -*- coding: utf-8 -*-
from uuid import uuid4
from openprocurement.auctions.core.utils import get_now

def award_fixture(auction, status, bid_index):
    now = get_now()
    return {
        "id": uuid4().hex,
        "date": now.isoformat(),
        "bid_id": auction["bids"][bid_index]["id"],
        "status": status,
        "suppliers": auction["bids"][bid_index]["tenderers"],
        'value': auction['value'],
        "complaintPeriod": {
            "startDate": now.isoformat(),
        },
        "signingPeriod": {
            "startDate": now.isoformat(),
            "endDate": now.isoformat(),
        },
        "verificationPeriod": {
            "startDate": now.isoformat()
        }
    }


def migrate_pendingVerification_pending_one_bid(self):
    auction = self.db.get(self.auction_id)

    pending_verification_award = award_fixture(auction, 'pending.verification', 0)
    auction['awards'] = [pending_verification_award]
    auction.update(auction)
    self.db.save(auction)
    self.migrate_data(self.app.app.registry)

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    auction = response.json['data']
    self.assertEqual(auction['status'], u'active.qualification')
    self.assertEqual(auction['awards'][0]['status'], u'pending')


def migrate_pendingPayment_active_one_bid(self):
    auction = self.db.get(self.auction_id)

    pending_payment_award = award_fixture(auction, 'pending.payment', 0)

    auction['awards'] = [pending_payment_award]
    auction.update(auction)
    self.db.save(auction)
    self.migrate_data(self.app.app.registry)

    response = self.app.get('/auctions/{}'.format(self.auction_id))
    auction = response.json['data']
    self.assertEqual(auction['awards'][0]['status'], u'active')

    response = self.app.get('/auctions/{}/contracts'.format(self.auction_id))
    contracts = response.json['data']
    self.assertEqual(len(contracts), 1)
    self.assertEqual(contracts[0]['status'], 'pending')
    self.assertEqual(contracts[0]['signingPeriod'], pending_payment_award['signingPeriod'])
