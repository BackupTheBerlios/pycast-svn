import weakref
from globalfunc import *

def main():
  class usage:
    vim=100
    inuse=True
  joe=usage()

  say(joe)

  print joe.vim
if __name__ == "__main__":
  main()
