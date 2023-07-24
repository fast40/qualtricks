import pathlib
import json
from zipfile import ZipFile
import shutil
import random


LOGS_FOLDER = pathlib.Path('static/data/logs')
FILES_FOLDER = pathlib.Path('static/data/files')

if not LOGS_FOLDER.exists():
	LOGS_FOLDER.mkdir(parents=True)

if not FILES_FOLDER.exists():
	FILES_FOLDER.mkdir(parents=True)


def get_log_path(dataset):
	return LOGS_FOLDER.joinpath(f'{dataset}.json')


def get_data_path(dataset):
	return FILES_FOLDER.joinpath(dataset)


def get_log_data(dataset):
	log_path = get_log_path(dataset)

	with open(log_path, 'r') as log_file:
		return json.load(log_file)


def set_log_data(dataset, data):
	log_path = get_log_path(dataset)

	with open(log_path, 'w') as file:
		json.dump(data, file, indent=4)


def get():
	return [path.stem for path in FILES_FOLDER.iterdir()]

	
def create(dataset, file):
	data_path = get_data_path(dataset)

	log_data = {
		'responses': {},
		'files': {}
	}

	with ZipFile(file) as zip_file:
		zip_file.extractall(data_path)
	
	paths = [path for path in data_path.rglob('*') if path.is_file() and path.name[0] != '.']
	
	for i, path in enumerate(paths):
		log_data['files'][i] = {
			'path': str(path.relative_to(FILES_FOLDER)),
			'views': 0
		}
	
	set_log_data(dataset, log_data)


def reset(dataset):
	log_data = get_log_data(dataset)
	log_data['responses'] = {}

	for file in log_data['files']:
		log_data['files'][file]['views'] = 0

	set_log_data(dataset, log_data)


def delete(dataset):
	log_path = get_log_path(dataset)
	data_path = get_data_path(dataset)

	log_path.unlink(missing_ok=True)
	shutil.rmtree(data_path, ignore_errors=True)


def get_random_file_path(dataset, response, loop_number):
	log_data = get_log_data(dataset)

	responses = log_data['responses']
	videos = log_data['files']

	if response not in responses:  # add the response_id to the log if it isn't already there
		responses[response] = {}
	elif loop_number in responses[response]:  # return the saved video if the user has already seen this loop_number
		return responses[response][loop_number]
	
	already_viewed_videos = list(responses[response].values())
	candidate_video_ids = []

	for video_id in videos.keys():
		if videos[video_id]['path'] not in already_viewed_videos:
			candidate_video_ids.append(video_id)

	random.shuffle(candidate_video_ids)
	candidate_video_ids = sorted(candidate_video_ids, key=lambda video_id: videos[video_id]['views'])

	try:
		selected_video_id = candidate_video_ids[0]
	except IndexError:
		return f'Could not find any new videos for response {response}'

	selected_video_path = videos[selected_video_id]['path']

	responses[response][loop_number] = selected_video_path
	videos[selected_video_id]['views'] += 1

	set_log_data(dataset, log_data)

	return FILES_FOLDER / selected_video_path