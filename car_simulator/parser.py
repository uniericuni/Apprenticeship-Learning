import sys, getopt

def parser(argv):
    gamemode = 2
    MAX_ITERATION = 100

    # try and catch
    try:
        opts, args = getopt.getopt(argv,"m:i:")
    except getopt.GetoptError:
        sys.stdout.write('usage: main.py [-m gamemode][-i max_iteration]'+'\n')
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
                sys.stdout.write('usage: -m [train|drive|auto]'+'\n')
                sys.exit(2)

        # max_iteration
        elif opt == '-i':
            try: 
                arg = int(arg)
                MAX_ITERATION = arg
            except ValueError:
                sys.stdout.write('usage: -i max_iteration(integer)'+'\n')
                sys.exit(2)

        # exception
        else: 
            sys.stdout.write('usage: main.py [-m gamemode][-i max_iteration]'+'\n')
            sys.exit(2)

    # system log
    sys.stdout.write('gamemode: %d'%gamemode+'\n')
    sys.stdout.write('max iteration: %d'%MAX_ITERATION+'\n')

    return gamemode,MAX_ITERATION
