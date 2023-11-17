from flask import Flask, request, render_template, send_file, redirect, url_for
from authenticate import create_authentication_routes, password_protected
import datasets

app = Flask(__name__)
app.config.from_pyfile('config.py')

create_authentication_routes(app, 'authenticate.html')


@app.route('/')
@password_protected
def index():
	datsets = datasets.get()

	return render_template('upload.html', datasets=datsets)


@app.route('/get_file')
def get_file():
	dataset = request.args.get('dataset')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if loop_number[0] == '$':
		return redirect(url_for('static', filename='media/test_video.webm'))

	file_path = datasets.get_random_file_path(dataset, response, loop_number)

	return redirect(file_path)


@app.route('/get_url')
def get_url():
	dataset = request.args.get('dataset')
	response = request.args.get('response')
	loop_number = request.args.get('loop_number')

	if loop_number[0] == '$':
		return url_for('static', filename='media/test_video.webm')

	file_path = datasets.get_random_file_path(dataset, response, loop_number)

	return file_path


@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['data']
	dataset = request.form['dataset']

	datasets.create(dataset, file)

	return redirect('/')


@app.route('/download')
def download():
	dataset = request.args.get('dataset')

	dataset_log = datasets.get_log_path(dataset)

	return send_file(dataset_log, as_attachment=True)


@app.route('/reset')
def reset():
	dataset = request.args.get('dataset')

	datasets.reset(dataset)

	return redirect('/')


@app.route('/delete')
def delete():
	dataset = request.args.get('dataset')

	datasets.delete(dataset)

	return redirect('/')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=3000)
