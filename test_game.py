import unittest,random,collections
import game
modules={'pong':game}
class Tests(unittest.TestCase):
 def test_pong_score(self):
  g=modules['pong'].Pong(80,24);g.x=-10;g.y=12;g.vx=-14;g.left=3;g.step(.05);self.assertEqual(g.score,[0,1])
 def test_pong_wall(self):
  g=modules['pong'].Pong(80,24);g.y=1;g.vy=-6;g.step(.05);self.assertGreater(g.vy,0)
 def test_pong_bounds(self):
  g=modules['pong'].Pong(80,24)
  for _ in range(1000):g.step(.04,random.choice((-1,0,1)))
  self.assertTrue(3<=g.left<=20)
if __name__=="__main__":unittest.main()
