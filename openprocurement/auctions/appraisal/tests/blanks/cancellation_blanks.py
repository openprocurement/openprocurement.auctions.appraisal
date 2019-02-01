# -*- coding: utf-8 -*-
import mock

from datetime import timedelta

from openprocurement.api.utils import get_now


def check_cancellation_document_type_required(self):
    doc_data = {
        'title': u'ук111р.doc',
        'url': self.generate_docservice_url(),
        'hash': 'md5:' + '0' * 32,
        'format': 'application/msword',
    }

    with mock.patch('openprocurement.auctions.appraisal.models.DOCUMENT_TYPE_REQUIRED_FROM', get_now() - timedelta(days=10)):
        response = self.app.post_json(
            '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(
                self.auction_id, self.cancellation_id, self.auction_token
            ),
            {'data': doc_data},
            status=422
        )
        self.assertEqual(response.json['errors'][0]['description'][0], 'documentType is required')

        doc_data['documentType'] = 'cancellationDetails'

        self.app.post_json(
            '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(
                self.auction_id, self.cancellation_id, self.auction_token
            ),
            {'data': doc_data},
            status=201
        )

    with mock.patch('openprocurement.auctions.appraisal.models.DOCUMENT_TYPE_REQUIRED_FROM', get_now() + timedelta(days=10)):
        del doc_data['documentType']

        self.app.post_json(
            '/auctions/{}/cancellations/{}/documents?acc_token={}'.format(
                self.auction_id, self.cancellation_id, self.auction_token
            ),
            {'data': doc_data},
            status=201
        )

