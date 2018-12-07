# -*- coding: utf-8 -*-
from uuid import uuid4
from copy import deepcopy


def check_items_listing(self):
    self.app.authorization = ('Basic', ('broker', ''))

    data = self.initial_data.copy()
    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    response = self.app.get(
        '/auctions/{}/items'.format(auction_id),
    )
    self.assertEqual(len(response.json['data']), len(data['items']))

    # Create one item and check listing
    response = self.app.post_json(
        '/auctions/{}/items'.format(auction_id),
        {'data': self.initial_item_data},
        headers=access_header
    )
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get(
        '/auctions/{}/items'.format(auction_id),
    )
    self.assertEqual(len(response.json['data']), len(data['items']) + 1)


def check_item_creation(self):
    self.app.authorization = ('Basic', ('broker', ''))

    data = self.initial_data.copy()
    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )
    # Item creation
    response = self.app.post_json(
        '/auctions/{}/items'.format(auction_id),
        {'data': self.initial_item_data},
        headers=access_header
    )
    item_id = response.json['data']['id']

    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(self.initial_item_data['id'], response.json['data']['id'])
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])

    # Get item
    response = self.app.get('/auctions/{}/items/{}'.format(auction_id, item_id))
    self.assertEqual(item_id, response.json['data']['id'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])


def check_item_patch(self):
    self.app.authorization = ('Basic', ('broker', ''))

    data = self.initial_data.copy()
    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    # Item creation
    response = self.app.post_json(
        '/auctions/{}/items'.format(auction_id),
        {'data': self.initial_item_data},
        headers=access_header
    )
    item_id = response.json['data']['id']

    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(self.initial_item_data['id'], response.json['data']['id'])
    self.assertIn(item_id, response.headers['Location'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])

    # Get item
    response = self.app.get('/auctions/{}/items/{}'.format(auction_id, item_id))
    self.assertEqual(item_id, response.json['data']['id'])
    self.assertEqual(self.initial_item_data['description'], response.json["data"]["description"])
    self.assertEqual(self.initial_item_data['quantity'], response.json["data"]["quantity"])
    self.assertEqual(self.initial_item_data['address'], response.json["data"]["address"])

    # Patch item
    patch_data = {'description': 'DESCRIPTION_' + uuid4().hex, 'id': '0*32'}
    response = self.app.patch_json(
        '/auctions/{}/items/{}'.format(auction_id, item_id),
        {'data': patch_data},
        headers=access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(patch_data['id'], response.json['data']['id'])
    self.assertEqual(patch_data['description'], response.json["data"]["description"])


def check_patch_auction_in_not_editable_statuses(self):
    self.app.authorization = ('Basic', ('broker', ''))

    # Auction creation
    data = self.initial_data.copy()
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.auction_id = auction_id
    self.set_status('active.tendering')

    # Item creation
    response = self.app.post_json(
        '/auctions/{}/items'.format(auction_id),
        {'data': self.initial_item_data},
        headers=access_header
    )
    item_id = response.json['data']['id']

    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')

    # Change status in which you can edit auction
    desired_status = 'active.auction'
    self.set_status(desired_status)

    self.app.authorization = ('Basic', ('broker', ''))

    # Trying to create new item
    response = self.app.post_json(
        '/auctions/{}/items'.format(auction_id),
        {'data': self.initial_item_data},
        headers=access_header,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(
        response.json['errors'][0]['description'],
        "You can't change items in this status ({})".format(desired_status)
    )

    # Trying to update new item
    response = self.app.patch_json(
        '/auctions/{}/items/{}'.format(auction_id, item_id),
        {'data': {'description': uuid4().hex}},
        headers=access_header,
        status=403
    )
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(
        response.json['errors'][0]['description'],
        "You can't change items in this status ({})".format(desired_status)
    )


def batch_create_items(self):
    self.app.authorization = ('Basic', ('broker', ''))

    data = self.initial_data.copy()
    data['items'] = [self.initial_item_data]
    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['items']), len(data['items']))


def batch_update_items(self):
    self.app.authorization = ('Basic', ('broker', ''))

    data = self.initial_data.copy()
    data['items'] = [self.initial_item_data]

    # Auction creation
    response = self.app.post_json('/auctions', {'data': data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['items']), len(data['items']))

    auction_id = response.json['data']['id']
    owner_token = response.json['access']['token']
    access_header = {'X-Access-Token': str(owner_token)}

    self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': {'status': 'active.tendering'}},
        headers=access_header
    )

    # Update items with batch mode
    item_2 = deepcopy(self.initial_item_data)
    del item_2['id']
    patch_items = {'items': [self.initial_item_data, item_2]}
    response = self.app.patch_json(
        '/auctions/{}'.format(auction_id),
        {'data': patch_items},
        headers=access_header
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']['items']), len(patch_items['items']))
