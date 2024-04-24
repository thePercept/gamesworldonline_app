from flask import Flask, render_template      

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/about',methods=['GET'])
def about():
    return "About US Page"




if (__name__ == '__main__'):
    app.run()

           
