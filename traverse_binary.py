import bap


if __name__ == "__main__":
   
    test_binary = "/bin/ls"
    proj = bap.run(test_binary)
    for sub in proj.program.subs:
        print sub.name
        for p in sub.blks:
            print p
