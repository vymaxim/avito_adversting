from flask import request, jsonify
from werkzeug.exceptions import abort
from app import app
from app.Exeptions import *


def page_not_found(err_description):
    return jsonify(error=str(err_description)), 404

def incorrect_input(err_description):
    return jsonify(error=str(err_description)), 400

app.register_error_handler(404, page_not_found)
app.register_error_handler(400, incorrect_input)


@app.route('/add_ad', methods=['POST'])
def add_ad():
    try:
        request_body = dict(request.json)
        if 'name' in request_body:
            name = request_body['name']
        else:
            name = None
        if 'description' in request_body:
            description = request_body['description']
        else:
            description = None
        if 'price' in request_body:
            price = request_body['price']
        else:
            price = None
        if 'main_url' in request_body:
            main_url = request_body['main_url']
        else:
            main_url = None
        if 'url2' in request_body:
            url2 = request_body['url2']
        else:
            url2 = None
        if 'url3' in request_body:
            url3 = request_body['url3']
        else:
            url3 = None
        from app import interaction
        return interaction.add_ad_info(
            name=name,
            description=description,
            price=price,
            main_url=main_url,
            url2=url2,
            url3=url3
        )
    except IncorrectInputException:
        abort(400, description='name or price values is None')


@app.route('/get_ad', methods=['POST'])
def get_ad():
    try:
        request_body = dict(request.json)
        if 'id' in request_body:
            id = int(request_body['id'])
        else:
            raise IncorrectInputException
        if 'fields' in request_body:
            fields = bool(request_body['fields'])
        else:
            fields = None
        from app import interaction
        ad = interaction.get_ad_info(id=id, fields=fields)
        return ad
    except AdNotFoundException:
        abort(404, description='Ad not found')
    except IncorrectInputException:
        abort(400, description='incorrect id values')


@app.route('/get_ads', methods=['POST'])
def get_ads():
    try:
        request_body = dict(request.json)
        if 'page' in request_body:
            page = int(request_body['page'])
        else:
            raise IncorrectInputException
        if 'sort' in request_body:
            sort = request_body['sort']
        else:
            sort = None
        from app import interaction
        if page is not None and sort is not None:
            ads_info = interaction.get_ads_info(page=int(page), sort=sort)
            return ads_info
        elif page is not None and sort is None:
            ads_info = interaction.get_ads_info(page=int(page))
            return ads_info
        else:
            raise IncorrectInputException
    except TableIsEmpty:
        abort(404, description='Table is empty')
    except IncorrectInputException:
        abort(400, description='incorrect sorting values entered or do not enter a value pagination')


@app.route('/del_ad/<id>', methods=['DELETE'])
def del_ad(id):
    from app import interaction
    return jsonify(interaction.del_ad(id))
