import bap


if __name__ == "__main__":
   
    test_binary = "/bin/true"
    print "parsing..."
    proj = bap.run(test_binary, ['--ssa'])
    
    print "run complete."
    for sub in proj.program.subs:
        print sub.name
        for p in sub.blks:
            print p


