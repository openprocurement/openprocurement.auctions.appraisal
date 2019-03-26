# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def switch_to_auction(self):
    self.set_status('active.auction')
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active.auction")


def switch_suspended_auction_to_auction(self):
    self.app.authorization = ('Basic', ('administrator', ''))
    self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': True}})
    self.set_status(
        'active.tendering',
        {'enquiryPeriod': {
                 'startDate': (datetime.now() - timedelta(days=2)).isoformat(),
                 'endDate': (datetime.now() - timedelta(days=1)).isoformat()
             }
         }
    )

    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']["status"], "active.auction")

    self.app.authorization = ('Basic', ('administrator', ''))
    self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': False}})

    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active.auction")
