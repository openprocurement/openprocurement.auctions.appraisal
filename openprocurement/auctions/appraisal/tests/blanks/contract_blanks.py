# -*- coding: utf-8 -*-
from datetime import timedelta

from openprocurement.auctions.core.utils import get_now


def patch_auction_contract_to_active(self):
    response = self.app.get('/auctions/{}/contracts'.format(self.auction_id))
    contract = response.json['data'][0]

    # Trying to patch contract to active status
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': u"Can't sign contract without contractSigned document",
         u'location': u'body',
         u'name': u'data'}
    ])

    # Truying to set dateSigned without `contractSigned` document
    custom_signature_date = get_now().isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"dateSigned": custom_signature_date}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': u"Can't sign contract without contractSigned document",
         u'location': u'body',
         u'name': u'data'}
    ])

    self.upload_contract_document(contract, 'contract')

    # Trying to patch contract to active status again
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"status": "active"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': u"Can't sign contract without "
                         u"specified dateSigned field",
         u'location': u'body',
         u'name': u'data'}])

    # Trying to patch contract's dateSigned field with invalid value
    one_hour_in_future = (get_now() + timedelta(hours=1)).isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"dateSigned": one_hour_in_future}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.json['errors'], [
        {u'description': [u"Contract signature date can't be in the future"],
         u'location': u'body',
         u'name': u'dateSigned'}
    ])

    # Trying to patch contract's dateSigned field with valid value
    custom_signature_date = get_now().isoformat()
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"dateSigned": custom_signature_date}})
    self.assertEqual(response.status, '200 OK')

    # Trying to patch contract to active status again
    response = self.app.patch_json('/auctions/{}/contracts/{}?acc_token={}'.format(
        self.auction_id, contract['id'], self.auction_token
    ), {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")

    response = self.app.get('/auctions/{}/contracts/{}'.format(
        self.auction_id, contract['id'])
    )
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active")
    self.assertEqual(response.json['data']["value"]['amount'], 479)
    self.assertEqual(
        response.json['data']['contractID'], contract['contractID']
    )
    self.assertEqual(response.json['data']['items'], contract['items'])
    self.assertEqual(response.json['data']['suppliers'], contract['suppliers'])
    self.assertEqual(response.json['data']['dateSigned'], custom_signature_date)
