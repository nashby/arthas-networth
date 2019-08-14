from app import db

from base64 import b64encode

class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    raw_donation = db.Column('raw_donation', db.String)
    author = db.Column('author', db.String)
    amount = db.Column('amount', db.Float)
    currency = db.Column('currency', db.String)
    donated_at = db.Column('donated_at', db.Integer)
    vod_youtube_id = db.Column('vod_youtube_id', db.String)
    vod_published_at = db.Column('vod_published_at', db.DateTime)
    donation_image = db.Column('donation_image', db.LargeBinary)
    approved = db.Column('approved', db.Boolean)
    created_at = db.Column('created_at', db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column('updated_at', db.DateTime)

    def dump_datetime(self, value):
        if value is None:
            return None
        return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

    @staticmethod
    def last_donation(self):
        donation = db.session.query(Donation).order_by(Donation.vod_published_at.desc(), Donation.donated_at.desc()).first()
        return donation

    @property
    def serialize(self):
       return {
           'id' : self.id,
           'raw_donation': self.raw_donation,
           'author': self.author,
           'amount': self.amount,
           'currency': self.currency,
           'donation_image': b64encode(self.donation_image).decode('ascii'),
           'vod_youtube_id': self.vod_youtube_id,
           'donated_at': self.donated_at,
           'vod_published_at': self.dump_datetime(self.vod_published_at)
       }
