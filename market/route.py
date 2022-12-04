from flask import Blueprint, render_template, request, session, current_app, url_for
from werkzeug.utils import redirect
from database.sql_provider import SQLProvider
import os
from access import external_required
from database.operations import select, select_dict, insert

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
@external_required
def order_index():
    db_config = current_app.config['db_config']

    if request.method == 'GET':
        sql = provider.get('product_list.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        print(items)
        return render_template('product_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('product_list.sql')
        items = select_dict(db_config, sql)

        add_to_basket(prod_id, items)

        return redirect(url_for('bp_market.order_index'))

def add_to_basket(prod_id: str, items:dict):
    item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
    print("Item_description before = ", item_description)
    item_description = item_description[0]
    curr_basket = session.get('basket', {})

    if prod_id in curr_basket:
        curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + 1
    else:
        curr_basket[prod_id] = {
            'prod_name': item_description['prod_name'],
            'prod_price': item_description['prod_price'],
            'amount': 1
        }
        session['basket'] = curr_basket
        session.permanent = True
    return True

@blueprint_market.route('/speciality', methods=['GET', 'POST'])
@external_required
def cart_speciality():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('speciality_list.sql')
        items = select_dict(db_config, sql)
        print(items)
        return render_template('cart_speciality.html', items=items)
    else:
        speciality = request.form['Speciality']
        session['speciality'] = speciality
        if not session['speciality']:
            return 'No valid speciality'
        else:
            print(session['speciality'])
            return redirect(url_for('market.cart_doctor'))


@blueprint_market.route('/doctor', methods=['GET', 'POST'])
@external_required
def cart_doctor():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('doctor_list.sql', speciality=session['speciality'])
        items = select_dict(db_config, sql)
        print(items)
        return render_template('cart_doctor.html', items=items)
    else:
        doctor_id = request.form['doctor_id']
        session['doctor_id'] = doctor_id
        if not session['doctor_id']:
            return 'No valid doctor ID'
        print(session['doctor_id'])
        return redirect(url_for('market.cart_timetable'))


@blueprint_market.route('/timetable', methods=['GET', 'POST'])
@external_required
def cart_timetable():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('timetable_list.sql', id_d=session['doctor_id'])
        items = select_dict(db_config, sql)
        print(items)
        return render_template('cart_timetable.html', items=items)
    else:
        date_zap = request.form['date_zap']
        time_zap = request.form['time_zap']
        session['date_zap'] = date_zap
        session['time_zap'] = time_zap
        print(session['date_zap'])
        print(session['time_zap'])
        return redirect(url_for('market.cart_confirm'))


@blueprint_market.route('/confirm', methods=['GET', 'POST'])
@external_required
def cart_confirm():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('confirm_data.sql', id_p=session['patient_id'], id_d=session['doctor_id'])
        items = select_dict(db_config, sql)
        return render_template('cart_confirm.html', items=items)
    else:
        sql_insert = provider.get('data_insert.sql', date_zap=session['date_zap'],
                                  time_zap=session['time_zap'],
                                  patient_id=session['patient_id'],
                                  doctor_id=session['doctor_id'])
        insert(db_config, sql_insert)
        print('SQL: ' + str(sql_insert))
        sql_update = provider.get('data_update.sql', date_zap=session['date_zap'],
                                  time_zap=session['time_zap'],
                                  doctor_id=session['doctor_id'])
        insert(db_config, sql_update)
        print('SQL: ' + str(sql_update))
        return render_template('cart_confirm_end.html')
