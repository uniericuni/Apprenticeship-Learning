import sys, getopt

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"m:")
   except getopt.GetoptError:
      print 'ggg'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-m':
        print '-m '+arg
      else: 
        print 'ggg'

if __name__ == "__main__":
   main(sys.argv[1:])
