import re
import time
import collections
import datetime as dt
import csv
import base64

from io import StringIO
from PIL import Image

import cv2 as cv
import numpy as np

from app.models import Donation
from app import db

from tesserocr import PyTessBaseAPI

import pafy

from collections import Counter

class DonationRecognizer:
    TESSERACT_THRESHOLD = 75

    def __init__(self):
        self.tesseract_client = PyTessBaseAPI(lang='rus+eng')

    def mask_donator_name_and_amount(self, frame):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Blue color range donator name and donate amount
        lower_val = np.array([90, 155, 155])
        upper_val = np.array([103, 255, 255])
        mask = cv.inRange(hsv_frame, lower_val, upper_val)

        masked_frame = cv.bitwise_not(mask)

        masked_frame = cv.morphologyEx(masked_frame, cv.MORPH_CLOSE, (3,3))
        masked_frame = cv.GaussianBlur(masked_frame, (3,3), 0)

        return masked_frame

    def bottom_part_of_frame_with_donator_name_and_amount(self, frame):
        return frame[540:720, 180:1100]

    def top_part_of_frame_with_donator_name_and_amount(self, frame):
        return frame[0:80, 180:1100]

    def is_frame_empty(self, frame):
        return np.sum(frame == 0) < 200

    def find_donator_name_and_amount(self, frame, lang, results):
        # Frame doesn't have donation text
        if self.is_frame_empty():
            return [results, False]

        self.tesseract_client.Init(lang=lang)
        self.tesseract_client.SetImage(Image.fromarray(frame))

        tsv_data = self.tesseract_client.GetTSVText(0)
        parsed_tsv_data = csv.reader(StringIO(tsv_data), delimiter='\t')

        recognized = False

        for row in parsed_tsv_data:
            text = row[-1]
            conf = int(row[-2])
            left = int(row[-6])
            height = int(row[-3])
            width = int(row[-4])

            if conf >= TESSERACT_THRESHOLD:
                recognized = True
                index = None

                for i in range(-10, 10):
                    if left + i in results:
                        index = left + i

                index = index or left

                if not index in results:
                    results[index] = []

                results[index].append([conf, height, width, text])

        # Frame has something similar to donation text colorwise but it's not donation
        if len(results) <= 2:
            return [{}, False]

        return [results, recognized]

    def find_most_accurate(self, results):
        words = []

        for key, result in collections.OrderedDict(sorted(results.items())).items():
            common_height = Counter(list(map(lambda x: x[1], result))).most_common(1)[0][0]
            common_width = Counter(list(map(lambda x: x[2], result))).most_common(1)[0][0]

            filtered_result = list(filter(lambda x: x[1] == common_height and x[2] == common_width, result))

            words.append(max(filtered_result, key=lambda x: x[0])[3])

        return words

    def format_donation_data(self, donation):
        raw_donation = ' '.join(donation).strip()
        raw_donation = re.sub(r"((?<=RUB|USD|EUR)(?:.(?!(RUB|USD|EUR)))+)$", "", raw_donation)
        raw_donation = re.sub(r"^\W+", "", raw_donation)
        raw_donation = re.sub(r"\W+$", "", raw_donation)

        regexped = re.search("(.+?) (([\d\s]+\,?\d*) (RUB|USD|EUR)(?:!?)\Z)", raw_donation)

        if not regexped:
            return {
                'raw_donation': raw_donation
            }

        groups = regexped.groups()

        return {
            'raw_donation': raw_donation,
            'author': groups[0].rstrip(' -'),
            'amount': float(groups[2].replace(',', '.').replace(' ', '')),
            'currency': groups[3],
        }

    def vods_with_donations(self):
        date_format = '%Y-%m-%d %H:%M:%S'

        # Donations were enabled since Sep 30, 2015
        # First stream is https://www.youtube.com/watch?v=snkEcLcIPew
        first_donation_date = dt.datetime.strptime('2015-09-30 00:00:00', date_format)

        channel = pafy.get_channel("https://www.youtube.com/user/SpitefulDick")
        uploads = list(filter(lambda vod: dt.datetime.strptime(vod.published, date_format) >= first_donation_date, channel.uploads))

        return sorted(uploads, key=lambda vod: vod.published)

    def save(self, data):
        donation = Donation(
            raw_donation=data.get('raw_donation'),
            author=data.get('author'),
            amount=data.get('amount'),
            currency=data.get('currency'),
            donated_at=data.get('donated_at'),
            donation_image=memoryview(data.get('donation_image')),
            vod_youtube_id=self.vod.videoid,
            vod_published_at=self.vod.published
        )

        db.session.add(donation)
        db.session.commit()

    def update(self, donation, data):
        donation.updated_at = dt.datetime.now()
        donation.raw_donation = data.get('raw_donation')
        donation.donation_image = data.get('donation_image')
        donation.author = data.get('author')
        donation.amount = data.get('amount')
        donation.currency = data.get('currency')

        db.session.commit()

    def recognize(self, video, vod, frame_start, break_after_recognition, callback):
        self.video = video
        self.vod = vod

        frame_number = 1

        first_extracted_at = None
        first_recognized_frame = None
        results = {}
        recognized = False

        not_recognized_times = 0

        ret, frame = self.video.read()
        lang = "rus"

        while(ret):
            # Get every 30th frame since youtube has 30 frames per second
            if frame_number % 30 == 0 and frame_number / 30 > frame_start:
                frame_part = self.bottom_part_of_frame_with_donator_name_and_amount(frame)
                masked_frame = self.mask_donator_name_and_amount(frame_part)

                # Try to find donation at the bottom of frame
                results, recognized = self.find_donator_name_and_amount(masked_frame, lang, results)

                # Try to find donation at the top of frame
                if not recognized:
                    frame_part = self.top_part_of_frame_with_donator_name_and_amount(frame)
                    masked_frame = self.mask_donator_name_and_amount(frame_part)

                    results, recognized = self.find_donator_name_and_amount(masked_frame, lang, results)

                # Switch languages for Tesseract since donation author can have name in russian, english or mixed
                if lang == "rus":
                    lang = "eng"
                else:
                    lang = "rus"

                if recognized:
                    first_extracted_at = first_extracted_at or frame_number

                    # Store frame when donation was detected at first. We save this data later
                    if first_recognized_frame is None:
                        first_recognized_frame = frame_part
                elif results and not_recognized_times >= 3:
                    words = self.find_most_accurate(results)
                    formatted_donation_data = self.format_donation_data(words)

                    if formatted_donation_data:
                        formatted_donation_data['donated_at'] = int(first_extracted_at / 30)
                        _, formatted_donation_data['donation_image'] = cv.imencode('.webp', first_recognized_frame, [cv.IMWRITE_WEBP_QUALITY, 20])
                        callback(formatted_donation_data)

                    results = {}
                    first_extracted_at = None
                    first_recognized_frame = None
                    not_recognized_times = 0

                    if break_after_recognition:
                        break
                else:
                    not_recognized_times = not_recognized_times + 1

                    if not_recognized_times >= 4 and break_after_recognition:
                        break

            frame_number = frame_number + 1
            ret, frame = self.video.read()
