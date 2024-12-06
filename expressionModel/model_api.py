from flask import Flask, render_template

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    print('표정인식 처리')

if __name__ == '__main__':
    app.run(debug=True)