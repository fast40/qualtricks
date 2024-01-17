from flask import Flask, Response, request, render_template, send_file, redirect, url_for, abort, send_from_directory
from flask_pymongo import PyMongo
from authenticate import create_authentication_routes, password_protected
import datasets

app = Flask(__name__)
app.config.from_pyfile('config.py')
client = PyMongo(app).cx

if client is None:
	raise Exception('There was an issue getting the database client.')


create_authentication_routes(app, 'authenticate.html')


@app.route('/')
@password_protected
def index():
	return render_template('index.html', dataset_names=datasets.get(client))


@app.route('/dataset/<dataset_id>')
@password_protected
def dataset(dataset_id):
	files = datasets.get_files(dataset_id, client)

	return render_template('dataset.html', datasets=datasets.get(client), files=files)


@app.route('/get_file')
def get_file():
	dataset = request.args.get('dataset')
	ordering = request.args.get('ordering')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if dataset is None or ordering is None or response is None or loop_number is None or loop_number[0] == '$':  # loop_number[0] will be $ when building the qualtrics survey
		return redirect(url_for('static', filename='media/test_video.webm'))

	file_path = datasets.get_file_fixed(dataset, response, int(loop_number), client)

	return redirect(f'/file/{file_path}')


@app.route('/get_url')
def get_url():
	dataset = request.args.get('dataset')
	ordering = request.args.get('ordering')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if dataset is None or ordering is None or response is None or loop_number is None or loop_number[0] == '$':  # loop_number[0] will be $ when building the qualtrics survey
		file_path = url_for('static', filename='media/test_video.webm')
	else:  # elif ordering == 'fixed':
		file_path = datasets.get_file_fixed(dataset, response, int(loop_number), client)
	
	file_url = Response(str(file_path))
	file_url.headers['Access-Control-Allow-Origin'] = '*'

	return file_url


@app.route('/upload', methods=['POST'])
def upload():
	zip_file = request.files['zip_file']
	dataset = request.form['dataset_name']

	datasets.create(dataset, zip_file, client)

	return redirect('/')


@app.route('/download')
def download():
	dataset = request.args.get('dataset')

	dataset_log = datasets.get_responses_file(dataset, client)

	return send_file(dataset_log, mimetype='application/json', as_attachment=True, download_name='data.json')


@app.route('/test')
def test():
	return '/test'


# @app.route('/reset')
# def reset():
# 	dataset = request.args.get('dataset')

# 	datasets.reset(dataset)

# 	return redirect('/')


# @app.route('/delete')
# def delete():
# 	dataset = request.args.get('dataset')

# 	datasets.delete(dataset)

# 	return redirect('/')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=3000)
