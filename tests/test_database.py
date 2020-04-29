import unittest

import time
from unittest.mock import MagicMock
from timerecorder.database import Database

class TestDatabase(unittest.TestCase):


    def setUp(self):
        self.thing = Database('test')
        
    def tearDown(self):
        pass

    def testResetStage(self):
        statements = self.thing.getCarUpdateStatements(123456, [1])

        self.assertEqual(statements, ['UPDATE laptimes SET Car=1 WHERE Timestamp="123456";'])

    def testGetMultipleCarUpdateStatements(self):
        statements = self.thing.getCarUpdateStatements(123456, [1, 5])

        self.assertEqual(statements, ['UPDATE laptimes SET Car=1 WHERE Timestamp="123456";', 'UPDATE laptimes SET Car=5 WHERE Timestamp="123456";'])

    def testGetMultipleTrackUpdateStatements(self):
        statements = self.thing.getTrackUpdateStatements(123456, [1, 5])

        self.assertEqual(statements, ['UPDATE laptimes SET Track=1 WHERE Timestamp="123456";', 'UPDATE laptimes SET Track=5 WHERE Timestamp="123456";'])

    def testUnidentifiedTrackUpdateStatements(self):
        statements = self.thing.getTrackUpdateStatements(123456, [])

        self.assertEqual(statements, [])

    def testGetCarInsertStatement(self):
        statement = self.thing.getCarInsertStatement(700, 200)

        self.assertEqual(statement, 'INSERT INTO cars (id, name, maxrpm, idlerpm) VALUES (ID, \'CAR_NAME\', 700, 200);')

    def testGetTrackInsertStatement(self):
        statement = self.thing.getTrackInsertStatement(10000, -1220)

        self.assertEqual(statement, 'INSERT INTO Tracks (id, name, length, startz) VALUES (ID, \'TRACK_NAME\', 10000, -1220);')

    def testGetUserId(self):
        userId = self.thing.createUserId();
        self.assertIsNotNone(userId, "userId must exist")

    def testUserIdDiffersOverTime(self):
        userId1 = self.thing.createUserId();
        time.sleep(1)
        userId2 = self.thing.createUserId();
        self.assertNotEqual(userId1, userId2, "userId must differ over time")
    
    def testRecordResults(self):
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor = MagicMock(return_value = cursor)
        cursor.execute = MagicMock()
        self.thing.getLapDbConnection = MagicMock(return_value = conn)
        
        self.thing.recordResults(100, 200, 1586278198.59, 220.4, 144)
        
        cursor.execute.assert_called_once_with('INSERT INTO laptimes (Track, Car, Timestamp, Time, Topspeed) VALUES (?, ?, ?, ?, ?)', (100, 200, 1586278198.59, 220.4, 144));
        conn.commit.assert_called_once()
        conn.close.assert_called_once()
        
if __name__ == "__main__":
    unittest.main()