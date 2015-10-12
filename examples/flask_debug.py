from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    raise

#bad
app.run(debug=True)


app.run(debug='True')
app.run(debug=False)

#okay
app.run()

#unrelated
run()
run(debug=True)
run(debug)
