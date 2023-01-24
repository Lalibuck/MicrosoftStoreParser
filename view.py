from flask import request, redirect, render_template, session
from app import app, db
from models import Application
from parser import driver_preprocess, category_parser, page_parser


def pag_number_valid(pag_number):
    if not pag_number or pag_number == '10':
        pag_number = 10
    else:
        pag_number = 20
    return pag_number


def page_valid(page):
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    return page


def searching(search):
    if search:
        query = Application.query.filter(Application.company.contains(search))
    else:
        query = Application.query
    return query


def order(sort, query):
    if sort == 'asc':
        query = query.order_by(Application.release.asc())
    elif sort == 'desc':
        query = query.order_by(Application.release.desc())
    return query


@app.route('/', methods=['POST', 'GET'])
def table():
    """The parsed app information displays as a table"""
    # get sorting, search and pagination information from a session
    search = session.get('search', '')
    pag_number = session.get('pag_number', '')
    sort = session.get('sort', '')
    # get the current page
    page = request.args.get('page')
    if request.method == 'POST':
        # handle search, pagination, sorting request
        if 'search' in request.form:
            session['search'] = request.form['search']
            search = session['search']
        if 'pag_number' in request.form:
            session['pag_number'] = request.form['pag_number']
            pag_number = session['pag_number']
        if 'release_sort' in request.form:
            session['sort'] = request.form['release_sort']
            sort = session['sort']
    # check correctness of input data about pagination
    pag_number = pag_number_valid(pag_number)
    # validation input page number
    page = page_valid(page)
    # filter data by search result
    query = searching(search)
    # sorting data by sort request(if necessary)
    query = order(sort, query)
    # query pagination
    pages = query.paginate(page=page, per_page=pag_number)
    return render_template('table.html', pages=pages, sort=sort, search=search)


@app.route('/parser', methods=['POST', 'GET'])
def parser():
    """Choosing parsing params, parsing Microsoft Store and add to the database"""
    # error message
    message = ''
    # parsing Microsoft store
    if request.method == 'POST':
        # check if amount param is digit
        if not request.form['amount'].isdigit():
            message = 'Please, input a number'
        # check the parsing limit
        elif int(request.form['amount']) > 200:
            message = 'Please, input a number less than 200'
        else:
            amount = int(request.form['amount'])
            # drop the previous parsing query
            Application.query.delete()
            # run selenium webdriver
            browser = driver_preprocess()
            # forming list of parsing app links
            for link in category_parser(browser, amount, request.form['category']):
                # parse app page
                app_inform = page_parser(browser, link)
                try:
                    # add application information to database
                    application = Application(name=app_inform[0], company=app_inform[1], release=app_inform[2], email=app_inform[3])
                    db.session.add(application)
                    db.session.commit()
                except:
                    message = 'Cannot record the data'
                    browser.quit()
                    return render_template('parser.html', message=message)
            browser.quit()
            return redirect('/')
    # display parsing params
    return render_template('parser.html', message=message)
