import argparse
from scripts.db import reset_db
from scripts.japanese_prototype_setup import populate_prototypes, process_csv

command_line_scripts = [
  'reset_db',
  'japanese_init',
  'csv_process'
]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run command line shell scripts')
  
  for cmd_line_script in command_line_scripts:
    parser.add_argument(f'--{cmd_line_script}', action='store_true', dest=cmd_line_script)

  args = parser.parse_args()
  print(args)

  if args.reset_db:
    reset_db()

  if args.japanese_init:
    populate_prototypes()

  if args.csv_process:
    process_csv()
