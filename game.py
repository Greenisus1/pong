#!/usr/bin/env python3
"""Fullscreen paddle-and-ball vs computer, offline original implementation."""
import curses,random,time
from ui import put,run
class Pong:
 def __init__(self,w,h,rng=None):
  self.w=w;self.h=h;self.rng=rng or random.Random();self.score=[0,0];self.left=self.right=h/2;self.reset()
 def reset(self):self.x=self.w/2;self.y=self.h/2;self.vx=self.rng.choice((-14,14));self.vy=self.rng.choice((-6,6))
 def step(self,dt,move=0):
  dt=min(.06,max(0,dt));self.left=max(3,min(self.h-4,self.left+move*25*dt));self.right=max(3,min(self.h-4,self.right+max(-1,min(1,self.y-self.right))*15*dt));self.x+=self.vx*dt;self.y+=self.vy*dt
  if self.y<2:self.y=2;self.vy=abs(self.vy)
  if self.y>self.h-3:self.y=self.h-3;self.vy=-abs(self.vy)
  if self.vx<0 and self.x<=3 and abs(self.y-self.left)<=2:self.x=3;self.vx=abs(self.vx);self.vy+=(self.y-self.left)*2
  if self.vx>0 and self.x>=self.w-4 and abs(self.y-self.right)<=2:self.x=self.w-4;self.vx=-abs(self.vx);self.vy+=(self.y-self.right)*2
  if self.x<0:self.score[1]+=1;self.reset()
  elif self.x>self.w-1:self.score[0]+=1;self.reset()

def loop(s):
 s.timeout(35);h,w=s.getmaxyx();g=Pong(w,h);last=time.monotonic();paused=False
 while True:
  h,w=s.getmaxyx();key=s.getch();s.erase();put(s,0,1,'PONG  You '+str(g.score[0])+' : '+str(g.score[1])+' Computer',curses.A_BOLD);put(s,h-1,1,'W/S or arrows paddle | Space pause | R restart | Esc/q exit')
  if key in (27,ord('q')):return
  if key==ord(' '):paused=not paused
  if key in (ord('r'),curses.KEY_RESIZE):g=Pong(w,h);paused=False
  now=time.monotonic();dt=now-last;last=now
  if w<40 or h<15:put(s,2,1,'Resize to40x15.');s.refresh();continue
  if not paused and max(g.score)<7:g.step(dt,-1 if key in (ord('w'),curses.KEY_UP) else 1 if key in (ord('s'),curses.KEY_DOWN) else 0)
  for y in range(2,h-2,2):put(s,y,w//2,'┆')
  for n in range(-2,3):put(s,int(g.left)+n,2,'█');put(s,int(g.right)+n,w-3,'█')
  put(s,int(g.y),int(g.x),'●',curses.A_BOLD)
  if max(g.score)>=7:put(s,h//2,max(1,w//2-10),'You win!' if g.score[0]>=7 else 'Computer wins!')
  elif paused:put(s,h//2,w//2-3,'PAUSED')
  s.refresh()
if __name__=='__main__':
 import sys
 if '--version' in sys.argv:print('1.0.0')
 else:raise SystemExit(run(loop))
