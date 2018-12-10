# -*- coding: utf-8 -*-


def new_owner_can_change(self):
    auth = ('Basic', (self.first_owner, ''))
    auction = self.create_auction_unit(auth=auth)

    self.app.authorization = ('Basic', (self.second_owner, ''))
    transfer = self.create_transfer()
    self.use_transfer(transfer,
                      auction['data']['id'],
                      auction['access']['transfer'])

    new_access_token = transfer['access']['token']

    # second_owner can change the auction
    desc = "second_owner now can change the tender"
    req_data = {"data": {"description": desc}}
    req_url = '/auctions/{}?acc_token={}'.format(auction['data']['id'], new_access_token)
    self.app.patch_json(req_url, {'data': {'status': 'active.tendering'}})
    response = self.app.patch_json(req_url, req_data)

    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('transfer', response.json['data'])
    self.assertNotIn('transfer_token', response.json['data'])
    self.assertIn('owner', response.json['data'])
    self.assertEqual(response.json['data']['description'], desc)
    self.assertEqual(response.json['data']['owner'], self.second_owner)
