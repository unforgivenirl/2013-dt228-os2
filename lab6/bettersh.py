# Very basic Posix shell with support for executing a single command
import os
import sys
import readline
import shlex

prompt = "bettersh> "

# Naive splitting of input into constituent arguments
def parse(cmd):
  return shlex.split(cmd)

# Execute an external command (i.e. run a  program on disk)
# If this succeeds it never returns
def execute(cmd, argv):
  try:
    os.execv(cmd, argv)
  except OSError: pass

def call(argv):
  if os.fork() == 0:
    cmd = argv[0]
    if '/' in cmd:
      # Relative or absolute path specified
      execute(cmd, argv)
    else:
      for dir in os.getenv('PATH').split(':'):
        # Keep trying each directory in PATH until we find it
        execute(dir + '/' + cmd, argv)

    # If we get here then execution has failed
    sys.stderr.write('Unrecognised command: ' + cmd + '\n')
    os._exit(1)
  else:
    os.wait()

# Read, print, eval, loop (REPL)
while True:
  try:
    cmd = input(prompt).strip()
    if cmd == "":
      # Empty command so just prompt again
      continue
    elif cmd == "exit":
      # Exit the shell
      break
    else:
      argv = parse(cmd)
      call(argv)
  except EOFError:
      # User has pressed Ctrl-D
    break
