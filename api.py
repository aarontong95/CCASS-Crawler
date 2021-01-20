import flask
from flask import request, request, render_template, url_for
from crawler import trend_plot, transaction_finder 
from config import shareholding_columns, transaction_columns, image_save_path
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
 
@app.route('/')
def index():
    return render_template("layout.html")

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/trend_plot', methods=['GET', 'POST'])
def api_trend_plot():
    if request.method == 'POST': 
        error = None
        result = []
        stock_code = request.form['stock_code']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        if stock_code == '' or start_date_str == '' or end_date_str == '':
            error = "All fileds must be filled out"
        else:
            result = trend_plot(stock_code, start_date_str, end_date_str)
        return render_template("trend_plot.html", 
                               data=result, 
                               columns=shareholding_columns,
                               title='Shareholding Table', 
                               code=stock_code, 
                               start_date=start_date_str, 
                               end_date=end_date_str, 
                               error=error)
    else:
        if os.path.isfile(image_save_path):
            os.remove(image_save_path)
            
        return render_template("trend_plot.html", 
                               data=[], 
                               columns=shareholding_columns, 
                               title="To Search")

 
@app.route('/transaction_finder', methods=['GET', 'POST'])
def api_transaction_finder():
    if request.method =='POST':
        error = None
        result = []
        stock_code = request.form['stock_code']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        threshold = float(request.form['threshold'])
        if stock_code == '' or start_date_str == '' or end_date_str == '' or threshold > 100 or threshold <= 0:
            error = "All fileds must be filled out and threshold should be in range 0 to 100"
        else:
            result = transaction_finder(stock_code, start_date_str, end_date_str, threshold)
        return render_template("transaction.html", 
                                   data=result,
                                   columns=transaction_columns, 
                                   title="Transaction Finder Table",
                                   code=stock_code,
                                   start_date=start_date_str,
                                   end_date=end_date_str,
                                   threshold=threshold,
                                   error=error)
    else:
        return render_template("transaction.html", 
                               data=[],
                               columns=transaction_columns, 
                               title="To Search")

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port = 5000)