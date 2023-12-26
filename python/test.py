from flask import Flask, render_template
import flask
import random
import subprocess
import time
app = Flask(__name__)


#export FLASK_APP=python/test.py
#flask run




def get_random_ticket():
	lotto = []
	for x in range(5):
		x = random.randint(0,70)
		pp = False
		while pp == False:
			if x in lotto:
				x = random.randint(0,70)
			else:
				pp = True
		lotto.append(x)
	y = random.randint(0,26)
	lotto.append(y)
	return lotto


@app.route('/lottery/<int:number1>/<int:number2>/<int:number3>/<int:number4>/<int:number5>')
def lottery(number1,number2,number3,number4,number5):

	def inner():
		count = 0
		x = False
		r = [number1,number2,number3,number4,number5]
		while(x == False):
			t = get_random_ticket()
			for i in r:
				if i not in t:
					x = False
					break
				else:
					x = True
			if x == False:
				count += 1
				print(str(count) + "\n")
				yield str(count) + '<br/>\n'
			else:
				print("Congrats it took you " + str(count) + " tries")
				yield "congratulations" + str(count) + '<br/>\n'

	return flask.Response(inner(), mimetype='text/html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
