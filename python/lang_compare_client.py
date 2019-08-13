import subprocess
import time

from lib import read_config, Runner

if __name__ == '__main__':
    config = read_config('config.yaml')

    runners = {}
    for elem in config['runners']:
        k, v = list(elem.items())[0]
        runner = Runner(v)
        runners[k] = runner

    for r in config['runs']:
        runner = runners[r]
        if runner.type == 'py':
            print('run cmd: {}'.format(runner.cmd))
            cmds = runner.cmd.split(' ')
            subprocess.run(cmds)
            time.sleep(1)
        else:
            err_str = "Invalid runner type in config.yaml: {}".format(runner.type)
            raise RuntimeError(err_str)


