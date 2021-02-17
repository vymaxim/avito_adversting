
from flask import jsonify
from app import Ads, session
from app.Exeptions import *


def get_ad_info(id=None, name=None, fields=False):
    if name is not None:
        ad = session.query(Ads).filter_by(name=name).first()
        if ad:
            session.expire_all()
            ad = {'id': ad.id}
            return jsonify(ad), 200
        else:
            raise AdNotFoundException
    else:
        ad = session.query(Ads).filter_by(id=id).first()
        if ad:
            session.expire_all()
            if fields:
                ad = {'id': ad.id, 'name': ad.name, 'price': ad.price, 'description': ad.description, 'main_url': ad.main_url, 'url2': ad.url2, 'url3': ad.url3}
            else:
                ad = {'id': ad.id, 'name': ad.name, 'price': ad.price, 'description': ad.description}
            return jsonify(ad), 200
        else:
            raise AdNotFoundException


def add_ad_info(name, price, description=None, main_url=None, url2=None, url3=None):
    if name is not None and price is not None:
        ad = Ads(
            name=name,
            price=price,
            description=description,
            main_url=main_url,
            url2=url2,
            url3=url3
        )
        session.add(ad)
        session.flush()
        return get_ad_info(name=name)
    else:
        raise IncorrectInputException


def get_ads_info(page=None, sort=None):
    sort_list = {
        "price_asc": Ads.price.asc(),
        "price_desc": Ads.price.desc(),
        "date_asc": Ads.data_create.asc(),
        "date_desc": Ads.data_create.desc(),
    }
    if sort is None:
        ads = session.query(Ads).all()
    elif sort in sort_list:
        ads = session.query(Ads).order_by(sort_list[sort]).all()
    if ads:
        ads_list = []
        if page is not None:
            for ad in ads[(page-1)*10:(page)*10]:
                ad = {'name': ad.name, 'price': ad.price, 'url': ad.main_url}
                ads_list.append(ad)
            session.expire_all()
            return jsonify(f'page {page}. Ads from {(page-1)*10+1} to {(page)*10}', ads_list), 200
        else:
            for ad in ads:
                ad = {'name': ad.name, 'price': ad.price, 'url': ad.main_url}
                ads_list.append(ad)
            session.expire_all()
            return ads_list, 200
    else:
        raise TableIsEmpty


def del_ad(id):
    ad = session.query(Ads).filter_by(id=id).one()
    session.delete(ad)
    session.flush()
    return f'ok', 200