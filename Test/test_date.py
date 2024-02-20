import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from datetime import datetime,timedelta
from app import competitions

class TestCompetitions(unittest.TestCase):

    def setUp(self) :
        self.competition = [
        {"name": "Spring Festival","date": "2024-03-27 10:00:00","numberOfPlaces": "25"},
        {"name": "Fall Classic","date": "2024-10-22 13:30:00","numberOfPlaces": "13"},
        ]
    def test_with_old_date(self):
        today = datetime.now()
        comps = [competition for competition in self.competition if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") < today]
        expected_comp=[]
        self.assertEqual(comps,expected_comp)

    def test_competition(self):
        today = datetime.now()
        comps = [competition for competition in self.competition if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
        expected_comps = [
        {"name": "Spring Festival","date": "2024-03-27 10:00:00","numberOfPlaces": "25"},
        {"name": "Fall Classic","date": "2024-10-22 13:30:00","numberOfPlaces": "13"},
        ]
        self.assertEqual(comps,expected_comps)