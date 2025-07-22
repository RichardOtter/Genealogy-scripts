# ===================================================DIV60==
import sys
import os
import shutil
from pathlib import Path

# Script to create and remove test files used by TestExternalFiles.py

# ================================================================
def main():


    if len(sys.argv) >2: 
        print( "\n\nERROR: Only one parameter allowed.\n")
        return
    if len(sys.argv) ==1: 
        print( "\n\nERROR: one parameter required - create or remove.\n")
        return

    action = None

    if sys.argv[1] == 'remove':
        action = 'remove'
    elif sys.argv[1] == 'create':
        action = 'create'
    else:
        print( f'argument {sys.argv[1]} unknown')
        return

#    action = 'create'

    # Assumes existence of \Users\Test
    if not Path(r'C:\Users\Test').is_dir():
        print('Base dir does not exist')
        return 1

    RM_test_root = Path(r'C:\Users\Test\RM_test_root')
    RM_test_media = RM_test_root / 'media'

    # RM_test_data_root is like GeneDB folder which will have database
    # RM_test_data_root\media   will be the test media folder

    test_db_home_fldr = Path(r'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\Test Data')
    test_files_home_fldr = Path(r'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Test external files\testing')

    test_db_file = 'TestData-RMpython.rmtree'
    test_ignore_file = 'TestExternalFiles_ignore.txt'
    test_ini_file ='test.ini'


                           
    file_fldr_list =[
        #      Base folder            created test folder         Test File
#        (r'G:\My Drive',              r'',                        'DBTest-file in GoogleDrive.txt '),
#        (r'F:' + '\\',                r'',                        'DBTest file -in abs dir1.txt'),
#        (r'F:'+'\\',                  r'test dir to check TEF',   'DBTest file -in abs dir2.txt '),
#        (r'C:\Users\rotter',         r'',                              'DBTest file -in home dir1.txt '),
#        (r'C:\Users\rotter',         r'test dir to check TEF',         'DBTest file -in home dir2.txt ')

        (r'C:\Users\Test',            r'',                            'DBTest file -above database dir1.txt'),
        (r'C:\Users\Test',            r'test dir',                    ''),
        (r'C:\Users\Test',            r'test dir',                    'DBTest file -above database dir2.txt'),

        (r'C:\Users\Test',            r'RM_test_root',           ''),
        (r'C:\Users\Test',            r'RM_test_root',           'DBTest file -in database dir1.txt'),

        (r'C:\Users\Test',            r'RM_test_root\test dir',  ''),
        (r'C:\Users\Test',            r'RM_test_root\test dir',  'DBTest file -in database dir2.txt'),

        (r'C:\Users\Test',            r'RM_test_root\media',  ''),
        (r'C:\Users\Test',            r'RM_test_root\media',  'DBTest file 01.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media',  'DBTest file 02.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media',  'DBTest file 03.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media',  'DBTest file 04.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media',  'DBTest file 05.jpg'),

        (r'C:\Users\Test',            r'RM_test_root\media\sub1',  ''),
        (r'C:\Users\Test',            r'RM_test_root\media\sub1',  'DBTest file s1 01.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media\sub1',  'DBTest file s1 02.jpg'),
        (r'C:\Users\Test',            r'RM_test_root\media\sub1',  'DBTest file s1 03.jpg'),

    ]

    db_file_in_test_root = RM_test_root / test_db_file
    ignore_file_in_test_media = RM_test_media / test_ignore_file
    ini_file_RM_test_root = RM_test_root / '..' / test_ini_file

    if action == 'remove':
        if db_file_in_test_root.exists():
            db_file_in_test_root.unlink()
        if ignore_file_in_test_media.exists():
            ignore_file_in_test_media.unlink()
        if ini_file_RM_test_root.exists():
            ini_file_RM_test_root.unlink()


    iterable = file_fldr_list
    if action == 'remove':
        iterable = reversed(file_fldr_list)

    for file in iterable:
        print (file)
        base_fldr = Path(file[0])
        intermed_fldrs = Path(file[1])
        file_name = Path(file[2])
        folder_path = base_fldr / intermed_fldrs
        print(folder_path)
        file_path = folder_path / file_name
        print(file_path)

        if action == 'remove':
            if file_path != Path(''):
                try:
                    os.remove(file_path)
                except:
                    pass
            if (intermed_fldrs !=Path('')
                        and is_folder_empty_os(folder_path)):
                os.rmdir(folder_path)

        elif action == 'create':
            if intermed_fldrs != Path('') and not folder_path.is_dir() :
                    os.mkdir(folder_path)
            if file_name != Path(''):
                file_path.touch()


    test_db_file = 'TestData-RMpython.rmtree'
    test_ignore_file = 'TestExternalFiles_ignore.txt'
    test_ini_file ='test.ini'
    test_files_home_fldr

    if action == 'create':
        if not db_file_in_test_root.exists():
            shutil.copyfile( test_db_home_fldr / test_db_file, db_file_in_test_root)
        if not ignore_file_in_test_media.exists():
            shutil.copyfile( test_files_home_fldr / test_ignore_file, ignore_file_in_test_media)
        if not ini_file_RM_test_root.exists():
            shutil.copyfile( test_files_home_fldr / test_ini_file, ini_file_RM_test_root)


# using \Users|test is safer in that can't delete files in rotter
# but RM xml file still points to actual media folder
# and home folder is still rotter
# could create a temp xml file with new media folder loc
# but actually- rm ini file says the root to look in. Does not have to be media folder
# add testing option to TEF to specify a testing rm xml file
# and try overriding HOME env variable for test runs ???


# =======================================================================DIV80==
def is_folder_empty_os(folder_path):
    """Checks if a folder is empty using os.listdir()."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return False
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory.")
        return False
    return not os.listdir(folder_path)


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

