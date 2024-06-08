#!python
import argparse
import os
import shutil
import uuid

from tqdm import tqdm

folder_path = "./test_assets"

# map structure:
# file name:
#   file size: file path
map = {}

# compare
def compare_files(fp1, fp2):
    with open(fp1, 'rb') as f1, open(fp2, 'rb') as f2:
        while True:
            chunk1 = f1.read(1024*1024)
            chunk2 = f2.read(1024*1024)
            if chunk1 != chunk2:
                return False
            if not chunk1:
                return True


class Scanner:
    def __init__(self):
        self.files_info = {}
        self.duplicates = {}
        self.ignore_list = ['.git', '__pycache__', '*.bak', '#recycle']

    def should_ignore(self, path):
        """判断路径是否应该被忽略"""
        for ignore_pattern in self.ignore_list:
            if '*' in ignore_pattern:
                # 使用简单的通配符匹配
                if ignore_pattern.replace('*', '') in path:
                    return True
            elif ignore_pattern in path:
                return True
        return False

    def scan(self, folder_path):
        pbar = tqdm(desc="Scanning Directories", unit="dir")
        pbarf = tqdm(desc="Comparing Files", unit="file")
        for root, subs, files in os.walk(folder_path):
            if not self.should_ignore(root):
                pbar.total = pbar.n + len(subs) + 1
                pbarf.total = pbarf.n + len(files) + 1
                pbar.update(1)
                for filename in files:
                    filepath = os.path.join(root, filename)
                    filesize = os.path.getsize(filepath)
                    key = (filename, filesize)
                    pbarf.update(1)
                    if key in self.files_info:
                        dup = False
                        for fileo in self.files_info[key]:
                            if compare_files(fileo, filepath):
                                dup = True
                                self.add_dup(fileo, filepath)
                        if not dup:
                            self.files_info[key].append(filepath)
                    else:
                        self.files_info[key] = [filepath]
        pbar.close()


    def add_dup(self, f1, f2):
        if f2 in self.duplicates:
            self.duplicates[f2].append(f1)
        elif f1 in self.duplicates:
            self.duplicates[f1].append(f2)
        else:
            self.duplicates[f1] = [f2]

    def remove_duplicate_files(self, recycle_bin='recycle'):
        if not os.path.exists(recycle_bin):
            os.makedirs(recycle_bin)

        pbar = tqdm(desc="Removing Files", unit="dir")
        pbar.total = sum([len(self.duplicates[f]) for f in self.duplicates])
        for file in self.duplicates:
            try:
                for file_dup in self.duplicates[file]:
                    uni_name = f"{uuid.uuid4()}_{os.path.basename(file_dup)}"
                    shutil.move(file_dup, os.path.join(recycle_bin, uni_name))
                    pbar.update(1)
            except OSError as e:
                print(f"Error deleting file {file_dup}: {e}")
        pbar.close()

    def print(self):
        for file in self.duplicates:
            print(file, "duplicate:")
            for file_dup in self.duplicates[file]:
                print(file_dup)
            print()


if __name__ == '__main__':
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
