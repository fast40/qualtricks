from flask import Flask, Response, request, render_template, send_file, redirect, url_for
from flask_pymongo import PyMongo
from authenticate import create_authentication_routes, password_protected
import datasets

app = Flask(__name__)
app.config.from_pyfile('config.py')
client = PyMongo(app).cx

create_authentication_routes(app, 'authenticate.html')


@app.route('/')
@password_protected
def index():
	dataset_names = datasets.get(client)

	return render_template('upload.html', dataset_names=dataset_names)


@app.route('/get_file')
def get_file():
	dataset = request.args.get('dataset')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if dataset is None or response is None or loop_number is None or loop_number[0] == '$':  # loop_number[0] will be $ when building the qualtrics survey
		return redirect(url_for('static', filename='media/test_video.webm'))

	file_path = datasets.get_file(dataset, response, loop_number, client)

	return redirect(f'/static/data/{file_path}')


@app.route('/get_url')
def get_url():
	dataset = request.args.get('dataset')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if dataset is None or response is None or loop_number is None or loop_number[0] == '$':  # loop_number[0] will be $ when building the qualtrics survey
		file_path = url_for('static', filename='media/test_video.webm')
	else:
		file_path = datasets.get_file(dataset, response, loop_number, client)
	
	file_url = Response(str(file_path))
	file_url.headers['Access-Control-Allow-Origin'] = '*'

	return file_url


@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['data']
	dataset = request.form['dataset']

	datasets.create(dataset, file, client)

	return redirect('/')


@app.route('/download')
def download():
	dataset = request.args.get('dataset')

	dataset_log = datasets.get_responses_file(dataset, client)

	return send_file(dataset_log, mimetype='application/json', as_attachment=True, download_name='data.json')


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
