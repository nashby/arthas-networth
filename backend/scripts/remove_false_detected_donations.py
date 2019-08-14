import sys
sys.path.insert(0, "/app")

from app import app
from app.models import Donation
from app import db

def remove_false_detected_donations():
  donations = Donation.query \
                      .order_by(Donation.vod_published_at.asc(), Donation.donated_at.asc()) \
                      .all()

  blanks = []
  removed = 0

  for donation in donations:
    if len(donation.raw_donation) <= 2:
      blanks.append(donation)

      db.session.delete(donation)

      removed = removed + 1

  db.session.commit()

  print("Blanks count: {}".format(len(blanks)))
  print("Removed count: {}".format(removed))

if __name__ == '__main__':
    remove_false_detected_donations()
