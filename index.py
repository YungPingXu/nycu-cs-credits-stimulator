from flask import Flask, render_template, request, redirect, url_for
import stimulate

app = Flask(__name__) # 初始化 Flask 類別成為 instance

@app.route('/', methods=['GET']) # 路由和處理函式配對
def index():
	return render_template('index.html')

@app.route('/stimulate', methods=['POST','GET']) # 路由和處理函式配對
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

if __name__ == '__main__': # 判斷自己執行非被當做引入的模組，因為 __name__ 這變數若被當做模組引入使用就不會是 __main__
	app.debug = True
	app.run()