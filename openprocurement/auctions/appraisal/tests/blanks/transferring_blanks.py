from iso8601 import parse_date
from datetime import timedelta
from copy import deepcopy


def check_pending_activation(self):
    auth = ('Basic', (self.first_owner, ''))
    data = deepcopy(self.initial_data)
    data['status'] = 'pending.activation'

    auction = self.create_auction_unit(auth=auth, data=data)

    self.app.authorization = ('Basic', (self.second_owner, ''))
    transfer = self.create_transfer()
    self.use_transfer(transfer,
                      auction['data']['id'],
                      auction['access']['transfer'])

    new_access_token = transfer['access']['token']

    # second_owner can change the auction

    req_data = {"data": {"status": "active.tendering"}}
    req_url = '/auctions/{}?acc_token={}'.format(auction['data']['id'], new_access_token)
    response = self.app.patch_json(req_url, req_data)

    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('transfer', response.json['data'])
    self.assertNotIn('transfer_token', response.json['data'])
    self.assertIn('owner', response.json['data'])
    self.assertEqual(response.json['data']['status'], "active.tendering")
    self.assertEqual(response.json['data']['owner'], self.second_owner)
