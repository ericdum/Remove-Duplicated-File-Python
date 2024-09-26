### Remove-Duplicated-File-Python

A simple script to check and move duplicate file to recycle can.

### Usage

1. Download the project.
2. Run `python main.py  -h` for help

#### Parameter Definition

```
    parser = argparse.ArgumentParser(description="A simple tool to scan duplicated files and move them to the recycle bin")
    parser.add_argument('target', type=str, help='The directory to scan')
    parser.add_argument('recycle', type=str, help='The directory to hold the duplicated files')
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--remove", action='store_true')

    args = parser.parse_args()

    scanner = Scanner()

    target = args.target if os.path.isabs(args.target) else os.path.abspath(args.target)
    recycle = args.recycle if os.path.isabs(args.recycle) else os.path.abspath(args.recycle)
    print(f"Your target directory is {target}")
    print(f"Your recycle directory is {recycle}")
    scanner.scan(args.target)

    if args.debug:
        scanner.print()

    if args.remove or input("move to trash? (Y/N)").lower() == "y":
        scanner.remove_duplicate_files(recycle)
```
