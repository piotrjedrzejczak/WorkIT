from datetime import datetime, timedelta
from flask import render_template
from workit.model.Newsletter import Newsletter
from workit.const import WEBSITES
from .email import send_mail
from . import mongo, app


def send_newsletters():
    with app.app_context():
        print('sending newsletters', flush=True)
        collection = mongo.newsletters.find({})
        for document in collection:
            newsletter = Newsletter(**document)
            user = mongo.users.find_one({'_id': newsletter.user_id})
            if newsletter.last_sent:
                delta = datetime.utcnow() - datetime.fromisoformat(newsletter.last_sent)
                frequency = timedelta(days=newsletter.frequency).total_seconds()
                if abs(delta.total_seconds() - frequency) < 3600:
                    body = render_template(
                        'newslettermail.html',
                        offers=newsletter.get_offers(),
                        username=user['name']
                    )
                    send_mail(body, 'WorkIT - Newsletter', user['email'])
                    newsletter.timestamp()
                    newsletter.update_lastsent()
            else:
                body = render_template(
                    'newslettermail.html',
                    offers=newsletter.get_offers(),
                    username=user['name']
                )
                send_mail(body, 'WorkIT - Newsletter', [user['email']])
                newsletter.timestamp()
                newsletter.update_lastsent()


def refresh_offers():
    print('downloading offers', flush=True)
    fresh_offers = []
    for website in WEBSITES:
        website.create_offers()
        fresh_offers.extend(website.serialize_offers())
    mongo.refresh_offers(fresh_offers)
