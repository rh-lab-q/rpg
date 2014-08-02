from subprocess import call

def move_file(self, location, target):
    call(["mv", location, target])
