from subprocess import Popen, PIPE


def run_command(command):
    process = Popen(command, stdout=PIPE)
    alive = True
    while alive:
        output = process.stdout.readline()
        
        print(output.strip().decode("utf-8")) if output else None

        alive = process.poll() is None

    rc = process.poll()
    return rc

run_command(["bash", "./test.sh"])
