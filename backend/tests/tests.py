import unittest
from unittest.mock import Mock

import cv2 as cv

import sys
sys.path.insert(0, "../app")

from donation_recognizer import DonationRecognizer

class TestRecognition(unittest.TestCase):
    def test_recegnition(self):
      videos = {
          'arthas_1024_newer_streams': {
            'author': 'HeroicTimes',
            'amount': 250.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_black_background': {
            'author': 'Контентина',
            'amount': 250.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_blue_background': {
            'author': 'Another day we will die, all',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_blue_background_2': {
            'author': 'elfovoz',
            'amount': 250.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_donation_on_top':  {
            'author': 'Фит фуфел',
            'amount': 500.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_full_rus':  {
            'author': 'Повар спрашивает повара',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_lokark_not_caught_donate':  {
            'author': 'lokark',
            'amount': 250.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_rus_eng_mix':  {
            'author': 'коци princess',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_russian_nick': {
            'author': 'Никитос',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_older_streams': {
            'author': 'Juse',
            'amount': 101.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_rus_and_numbers': {
            'author': 'Творожокб66',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_full_rus_two_words': {
            'author': 'Гей Виталий',
            'amount': 200.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_duplications': {
            'author': 'Работники',
            'amount': 500.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_sum_not_detected': {
            'author': 'wtrust',
            'amount': 150.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_duplications_2': {
            'author': 'Lich King',
            'amount': 100.0,
            'currency': 'RUB'
          },

          'arthas_1024_newer_streams_old_font': {
            'author': 'Net Og',
            'amount': 150.0,
            'currency': 'RUB'
          },

          'arthas_1024_older_streams_long_nick': {
            'author': 'Цаль Катя Богдановна, 8 лет',
            'amount': 150.0,
            'currency': 'RUB'
          },

          'arthas_1024_older_nick_with_numbers_at_end': {
            'author': 'Bloodes 322',
            'amount': 150.0,
            'currency': 'RUB'
          }
      }

      recognizer = DonationRecognizer()

      for video_name, expected_donation_data in videos.items():
        video = cv.VideoCapture(f"tests/data/{video_name}.mp4")
        vod = Mock(videoid='1234', published='2019-01-01 00:00:00')

        donation_data = []
        recognizer.recognize(video, vod, 0, False, lambda x: donation_data.append(x))

        donation_data = donation_data[0]

        with self.subTest(msg=f"{video_name}"):
          self.assertEqual(donation_data['author'], expected_donation_data['author'])
          self.assertEqual(donation_data['amount'], expected_donation_data['amount'])
          self.assertEqual(donation_data['currency'], expected_donation_data['currency'])

if __name__ == '__main__':
    unittest.main()
