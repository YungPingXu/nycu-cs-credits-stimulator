from flask import Flask, render_template, request, redirect, url_for
import stimulate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/stimulate', methods=['POST','GET'])
def calculate():
	print(request.method)
	if request.method == "POST":
		result = ""
		content = request.values['content']
		student_class = request.values['student_class']
		if student_class in ("AB", "C", "D"):
			result = stimulate.calculate(content, student_class)
		else:
			redirect(url_for("index"))
		return render_template('result.html', result=result)
	return redirect(url_for("index"))

if __name__ == '__main__':
	app.debug = True
	app.run()