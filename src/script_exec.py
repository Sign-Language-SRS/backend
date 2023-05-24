import argparse
from scripts.init_db import init_db

command_line_scripts = [
  'init_db'
]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run command line shell scripts')
  
  for cmd_line_script in command_line_scripts:
    parser.add_argument(f'--{cmd_line_script}', action='store_true', dest=cmd_line_script)

  args = parser.parse_args()

  if args.init_db:
    init_db()
