import os
import logging
from datetime import datetime

from flask import request, current_app
from flask_security import current_user

from udata.api import apiv2

@apiv2.route('/datasets', methods=['GET'])
def get_datasets_list():
    '''List or search all datasets'''


@ns.route('/', endpoint='datasets')
class DatasetListAPI(API):
    '''Datasets collection endpoint'''
    @api.doc('list_datasets')
    @api.expect(search_parser)
    @api.marshal_with(dataset_page_fields)
    def get(self):
        '''List or search all datasets'''
        search_parser.parse_args()
        return search.query(Dataset, **multi_to_dict(request.args))

    @api.secure
    @api.doc('create_dataset', responses={400: 'Validation error'})
    @api.expect(dataset_fields)
    @api.marshal_with(dataset_fields)
    def post(self):
        '''Create a new dataset'''
        form = api.validate(DatasetForm)
        dataset = form.save()
        return dataset, 201
