from __future__ import annotations

from typing import TYPE_CHECKING
import pathlib
from zipfile import ZipFile
import json
import io
import random

import pymongo

if TYPE_CHECKING:
    import os

DATA_ROOT_DIR = pathlib.Path('/files')
DATABASE = 'qualtricks'


def get(client: pymongo.MongoClient):
    return client[DATABASE]['datasets'].distinct('dataset')


def get_files(dataset: str, client: pymongo.MongoClient):
    return list(client[DATABASE]['datasets'].find({'dataset': dataset, 'path': {'$exists': True}}))


def create(dataset: str, zip_file: str | os.PathLike, client: pymongo.MongoClient):
    dataset_path = DATA_ROOT_DIR.joinpath(dataset)

    if dataset_path.exists():
        raise FileExistsError('Dataset has already been created once.')

    with ZipFile(zip_file) as zf:
        zf.extractall(dataset_path)
    
    client[DATABASE]['datasets'].insert_many({
        'dataset': dataset,
        'path': str(path.relative_to(DATA_ROOT_DIR)),
        'views': 0,
        'loop_number': 0
    } for path in dataset_path.rglob('*') if path.is_file() and path.name[0] != '.')

    client[DATABASE]['datasets'].insert_one({
        'dataset': dataset,
        'views_in_round': 0
    })

    shuffle(dataset, client)

  
def shuffle(dataset: str, client: pymongo.MongoClient):
    files = list(client[DATABASE]['datasets'].find({'dataset': dataset, 'path': {'$exists': True}}))

    random.shuffle(files)

    for i, file in enumerate(files):
        client[DATABASE]['datasets'].update_one({'_id': file['_id']}, {'$set': {'loop_number': i + 1}})


def _reset(dataset: str, client: pymongo.MongoClient):
    print('WARNING: reset was called. This will reset view counts AND responses.')
    client[DATABASE]['datasets'].update_many(filter={'dataset': dataset, 'views': {'$exists': True}}, update={'$set': {'views': 0}})
    client[DATABASE]['datasets'].update_one(filter={'dataset': dataset, 'views_in_round': {'$exists': True}}, update={'$set': {'views_in_round': 0}})
    client[DATABASE]['responses'].delete_many({'dataset': dataset})


def get_file(dataset: str, ordering: str, response_id: str, loop_number: str, client: pymongo.MongoClient):
    response = client[DATABASE]['responses'].find_one(filter={'response_id': response_id}, projection={'_id': 0, 'response_id': 0})

    if response is not None and loop_number in response:
        return response[loop_number]

    excluded_files = list(response.values()) if response is not None else []
    
    views_in_round = _get_views_in_round(dataset, client)
    path = _get_path_and_update_file(dataset, views_in_round, excluded_files, client)

    if path is None:
        raise FileNotFoundError(f'Could not find a file in datset {dataset} for response_id {response_id}')
    
    _add_path_to_response(dataset, response_id, loop_number, path, client)

    return path


def get_file_fixed(dataset: str, response_id: str, loop_number: int, client: pymongo.MongoClient):
    response = client[DATABASE]['responses'].find_one(filter={'response_id': response_id}, projection={'_id': 0, 'response_id': 0})

    if response is not None and loop_number in response:
        return response[loop_number]

    file = client[DATABASE]['datasets'].find_one({'dataset': dataset, 'loop_number': loop_number}) 

    return file['path']


 
def get_responses_file(dataset: str, client: pymongo.MongoClient):
    files = list(client[DATABASE]['responses'].find(filter={'dataset': dataset}, projection={'_id': 0, 'dataset': 0}))

    json_string = json.dumps(files, indent=4).encode('utf-8')

    json_file = io.BytesIO()
    json_file.write(json_string)
    json_file.seek(0)

    return json_file


def _get_views_in_round(dataset: str, client: pymongo.MongoClient):  
    views_in_round = client[DATABASE]['datasets'].find_one(
        filter={'dataset': dataset, 'views_in_round': {'$exists': True}})

    if views_in_round is None:
        raise NameError(f'Could not find views_in_round for dataset {dataset}')
    
    return views_in_round['views_in_round']


def _get_path_and_update_file(dataset: str, views_in_round: int, excluded_files: list, client: pymongo.MongoClient):
    file = client[DATABASE]['datasets'].find_one_and_update(
        filter={
            'dataset': dataset,
            'views': {
                '$lte': views_in_round,
                '$nin': excluded_files
            }
        },
        update={
            '$inc': {
                'views': 1
            }
        },
    )

    if file is not None:
        return file['path']

    test_file = client[DATABASE]['datasets'].find_one(
        filter={
            'dataset': dataset,
            'views': {
                '$lte': views_in_round,
            }
        },
    )

    if test_file is not None:
        return None
    
    _set_views_in_round(dataset, views_in_round + 1, client)

    file = client[DATABASE]['datasets'].find_one_and_update(
        filter={
            'dataset': dataset,
            'views': {
                '$lte': views_in_round,
                '$nin': excluded_files
            }
        },
        update={
            '$inc': {
                'views': 1
            }
        },
    )

    if file is not None:
        return file['path']
    else:
        return None


def _set_views_in_round(dataset: str, views: int, client: pymongo.MongoClient):
    client[DATABASE]['datasets'].update_one(
        {
            'dataset': dataset,
            'views_in_round': {
                '$exists': True
            }
        },
        {
            '$set': {
                'views_in_round': views
            }
        }
    )


def _add_path_to_response(dataset: str, response_id: str, loop_number: str, path: str, client: pymongo.MongoClient):
    client[DATABASE]['responses'].update_one(
        filter={
            'response_id': response_id,
            'dataset': dataset
        },
        update={
            '$set': {
                loop_number: path
            }
        },
        upsert=True
    )


# if __name__ == '__main__':
#     client = pymongo.MongoClient(f'mongodb://127.0.0.1:27017/{DATABASE}')

#     # create('test', 'test.zip', client)
#     _reset('test', client)

#     for i in range(10):
#         get_file('test', 'test', str(i), client)