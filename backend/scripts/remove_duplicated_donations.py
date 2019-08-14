import sys
sys.path.insert(0, "/app")

from app import app
from app.models import Donation
from app import db

def remove_duplicated_donations():
  donations = Donation.query \
                      .order_by(Donation.vod_published_at.asc(), Donation.donated_at.asc()) \
                      .all()

  prev_donation = None
  duplicates = []
  removed = 0

  for donation in donations:
    if prev_donation:
      if donation.donated_at - prev_donation.donated_at <= 5 and donation.vod_youtube_id == prev_donation.vod_youtube_id and donation.author == donation.author:
        duplicates.append([prev_donation, donation])

        db.session.delete(donation)

        removed = removed + 1

    prev_donation = donation

  db.session.commit()

  print("Duplicates count: {}".format(len(duplicates)))
  print("Removed count: {}".format(removed))

if __name__ == '__main__':
    remove_duplicated_donations()
