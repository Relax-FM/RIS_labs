@blueprint_edit.route('insert_prod', methods=["POST"])
def inserted_prod():
    message = "товар добавлен в базу данных"
    insert_values = [request.form.get('prod_name'), request.form.get('prod_price')]
    _sql = provider.get('insert.sql', insert_product=insert_values)
    res = insert(current_app.config['db_config'],_sql)
    print(res)
    return render_template('update_ok.html', message=message)


@blueprint_edit.route('insert_prod', methods=["GET"])
def insert_prod():
