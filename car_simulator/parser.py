import sys, getopt

def parser(argv):
    gamemode = 2
    MAX_ITERATION = 100

    # try and catch
    try:
        opts, args = getopt.getopt(argv,"m:i:")
    except getopt.GetoptError:
        print 'usage: main.py [-m gamemode][-i max_iteration]'
        sys.exit(2)

    # parameter parsing
    for opt, arg in opts:

        # gamemode
        if opt == '-m':
            if arg=='train':
                gamemode = 100
            elif arg=='free_drive':
                gamemode = 2
            elif arg=='drive':
                gamemode = 2
            elif arg=='auto':
                gamemode = 3
            else:
                print 'usage: -m [train|drive|auto]'
                sys.exit(2)

        # max_iteration
        elif opt == '-i':
            try: 
                arg = int(arg)
                MAX_ITERATION = arg
            except ValueError:
                print 'usage: -i max_iteration(integer)'
                sys.exit(2)

        # exception
        else: 
            print 'usage: main.py [-m gamemode][-i max_iteration]'
            sys.exit(2)

    # system log
    print 'gamemode: %d' %gamemode
    print 'max iteration: %d' %MAX_ITERATION

    return gamemode,MAX_ITERATION
