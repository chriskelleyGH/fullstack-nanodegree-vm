from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    recentItems = session.query(Item).filter().order_by('Item.id desc').limit(10)
    items = []

    for i in recentItems:
        category = session.query(Category).filter_by(id=i.category_id).one()
        item = {'item_name': i.name, 'category_name': category.name}
        items.append(item)

    return render_template('catalog.html', categories=categories, items=items)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], category_id=request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)

@app.route('/catalog/<string:category_name>/')
def showItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('items.html', items=items, category=category)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    return render_template ('item.html', item=item, category=category)

@app.route('/catalog/<string:category_name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        categories = session.query(Category).all()
        return render_template('edititem.html', category_name=category_name, item=editedItem, categories=categories)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('deleteitem.html', category_name=category_name, item_name=item_name, item=itemToDelete)

@app.route('/JSON/')
@app.route('/catalog/JSON/')
def catalogJSON():
    Catalog_Data = session.query(Category)
    return jsonify(categories=[category.serialize for category in Catalog_Data.all()])

@app.route('/catalog/<string:category_name>/JSON/')
def categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON/')
def itemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    Catalog_Item = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
