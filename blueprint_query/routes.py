import os.path

from flask import Blueprint, request, render_template, current_app
from database.operations import select
from database.sql_provider import SQLProvider
from access import group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/test')
def provider_test():
    p = os.path
    print(p)
    p1 = os.path.dirname(__file__)
    print(p1)
    return 'None'


@blueprint_query.route('/queries', methods=['GET', 'POST'])
@group_required
def queries():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html')
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return render_template('not_found.html')
    return render_template('queries.html')