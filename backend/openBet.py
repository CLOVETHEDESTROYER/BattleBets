from flask import Flask




app=Flask(__name__)


#members API route
@app.route('/winner')
def winner():
    return {'Winner': ["Member1", "Member2", "Member3", "CacaBallZ", "nalga"]}

if __name__ == "__main__":
    app.run(port= 8000, debug=True)
