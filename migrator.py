import configuration as c
import sys
import subprocess

commands = ('apply', 'rollback', 'reapply', 'break-lock')

if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print('Prvy argument musi byt', '/'.join(commands), file=sys.stderr)
        sys.exit(1)

    print("Selected database:", c.DB)
    inp = input('Continue? [Yn]: ')

    if inp == '' or inp.startswith('Y'):
        db = f"mysql://{c.USER}:{c.PASSWD}@{c.HOST}:{c.PORT}/{c.DB}"
        subprocess.run(["yoyo", sys.argv[1], '--database', db])
