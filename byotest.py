from byotest import*
import os

def test_index(get, self):
        """Route Testing"""
        response = get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
def test_scoreboard(self, get, response):
        """Route Testing"""
        response = get('/scoreboard', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
print("All tests pass!")