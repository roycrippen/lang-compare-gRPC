from subprocess import *
import time

from lib import read_config

if __name__ == '__main__':
    config = read_config('config.yaml')

    runners = {}
    for k, v in config['runners'].items():
        runners[k] = v['cmd']

    for r in config['runs']:
        if r in runners:
            cmd = runners[r]
            print('\n\n[RUN COMMAND]: {}'.format(cmd))
            cmds = cmd.split(' ')
            run(cmds)
            time.sleep(0.25)
        else:
            err_str = "Invalid runner found in runs section of config.yaml: {}".format(r)
            raise RuntimeError(err_str)

