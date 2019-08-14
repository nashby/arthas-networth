import pafy

import cv2 as cv
import datetime as dt

from donation_recognizer import DonationRecognizer
from app.models import Donation

# First time recognition
def recognize_donations():
    date_format = '%Y-%m-%d %H:%M:%S'

    recognizer = DonationRecognizer()
    last_donation = Donation.last_donation()

    vods = recognizer.vods_with_donations()

    for vod in vods:
        try:
            if last_donation and dt.datetime.strptime(vod.published, date_format) < last_donation.vod_published_at:
                continue

            stream = vod.allstreams[-1]
            video = cv.VideoCapture(stream.url)

            if last_donation:
                frame_start = last_donation.donated_at
            else:
                frame_start = 0

            recognizer.recognize(video=video, vod=vod, frame_start=frame_start, break_after_recognition=False, callback=lambda x: recognizer.save(x))
        except OSError:
            pass

# Iterate through saved donations and try to recognize it again
# It's used when recognition algorithm is improved and we need to use it again but we don't want to parse whole video again
# since we have donation timing saved in DB
def re_recognize_donations():
    donations = Donation.query.order_by(Donation.vod_published_at.asc(), Donation.donated_at.asc()).all()
    recognizer = DonationRecognizer()
    vod_id = None

    for donation in donations:
        last_vod_id = vod_id
        vod_id = donation.vod_youtube_id

        if last_vod_id != vod_id:
            vod = pafy.new("https://www.youtube.com/watch?v={}".format(vod_id))
            stream = vod.allstreams[-1]
            video = cv.VideoCapture(stream.url)

        video.set(cv.CAP_PROP_POS_MSEC, donation.donated_at * 1000)

        recognizer.recognize(video=video, vod=vod, frame_start=0, break_after_recognition=True, callback=lambda x: recognizer.update(donation, x))

if __name__ == '__main__':
    re_recognize_donations()
