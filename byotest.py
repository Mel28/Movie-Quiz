from byotest import*
import unittest
import os

def test_index(self):
        """Route Testing"""
        test1 = app.test_client(self)
        response = test1.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
def test_scoreboard(self):
        """Route Testing"""
        test3 = app.test_client(self)
        response = test3.get('/scoreboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
   unittest.main()
print("All tests pass!")