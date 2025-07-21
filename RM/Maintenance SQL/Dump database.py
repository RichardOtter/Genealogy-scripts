import os
from datetime import datetime
from pathlib import Path
import subprocess

#  File paths must use either doubled back slash or
#     forward slash (posix) due to Sqlite3.exe limitation
# may be sensitive to spaces in paths

# requires SQLite3.exe from
# https://sqlite.org/download.html
# see download labeled: sqlite-tools-win-x64-3440200.zip
#   A bundle of command-line tools for managing SQLite database files ...

#   https://www.sqlite.org/cli.html#using_sqlite3_in_a_shell_script
#   https://www.sqlite.org/cli.html

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    # file locations
   # database_path = Path(r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree")
   # database_path = Path(r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\Test Data\TestData-RMpython.rmtree")
    database_path = Path(r"E:\Users Overflow\ROtter external\Genealogy\Generated Output\DB Dump files\oldOtter-Saito.rmtree")

    dump_fldr_path = Path(r"E:\Users Overflow\ROtter external\Genealogy\Generated Output\DB Dump files")
    dump_file = F'Otter-Saito-sql-dump-{timestamp}.sql'
    patch_file = F'diff_patch-{timestamp}.txt'
    dump_file_path = dump_fldr_path / dump_file
    patch_file_path = dump_fldr_path / patch_file


    prev_latest_dump_file = get_latest_file(dump_fldr_path, "Otter-Saito-sql-dump*")

    app_path=r"\bin\sqlite3.exe"
    database_path_posix = database_path.as_posix()
    dump_file_path_posix = dump_file_path.as_posix()

    temp_folder = os.environ['TEMP']
    temp_cmd_file=Path(temp_folder) / F'cmd_file_{timestamp}'

    open_cmd = F".open '{database_path_posix}'\n"
    output_cmd = F".output '{dump_file_path_posix}'\n"

    with open(temp_cmd_file, 'w') as dump_cmd_file:
        dump_cmd_file.write(open_cmd)
        dump_cmd_file.write(output_cmd)
        dump_cmd_file.write('.dump\n')
        dump_cmd_file.write('.quit\n')

    # with open(temp_cmd_file, 'r') as dump_cmd_file:
    #     for line in dump_cmd_file:
    #         print(line)

    with open(temp_cmd_file, 'r') as stdin_file:
        subprocess.run( app_path,
            stdin=stdin_file,
            shell=True
                        )

    os.remove(temp_cmd_file)

    print( F"""Generate the git diff between 
    {prev_latest_dump_file}
    and 
    {dump_file_path}
          """)

    #   git diff unified=0 --no-index file1 file2

    git_path = r'C:\Users\rotter\AppData\Local\Programs\Git\bin\git.exe'

    with open( patch_file_path, 'w') as output_file:
        subprocess.run(
        [
        git_path,
        'diff',
        '--unified=0',
        '--no-index',
        '--',
        prev_latest_dump_file,
        dump_file_path
        ],
        stdout=output_file,
        shell=True
                        )

    # to restore
    # .open the DB (create it)
    # sqlite> .read C:\\somesubdir\\some.sql

# ===================================================DIV60==
def get_latest_file(folder, pattern):
    files = list(Path(folder).glob(pattern))
    return max(files, key=os.path.getmtime) if files else None

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
