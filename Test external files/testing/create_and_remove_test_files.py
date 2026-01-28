# ===================================================DIV60==
import sys
import os
import shutil
from pathlib import Path

# Script to create and remove test files used by TestExternalFiles.py

# ================================================================
def main():

    # test mode override =True


    if False:  #TestMode:
        action = 'remove'
        #action = 'create'
    else:
        if len(sys.argv) >2: 
            print( "\n\nERROR: Only one parameter allowed.\n")
            input("press enter to continue and exit")
            return
        if len(sys.argv) ==1: 
            print( "\n\nERROR: one parameter required - create or remove.\n")
            input("press enter to continue and exit")
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

    # Source files
    test_db_home_fldr = Path(r'C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Test Data')
    tef_app_home= Path(r'C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Test external files')
    test_files_home_fldr = tef_app_home / 'testing'

    test_db_file = 'TestData-RMpython.rmtree'
    test_ignore_file = 'TestExternalFiles_ignore.txt'
    test_ini_file ='test.ini'
    test_run_TEF_shortcut_1 = '__Run TestExternalFiles with test.ini.lnk'
    test_run_TEF_shortcut_2 = '__Run TestExternalFiles with test.ini RELATIVE bad.lnk'
    cmd_1 = 'Run RM with Home=Test.cmd'
    cmd_2 = 'Run TEF with Home=Test.cmd'
    tef_app = "TestExternalFiles.py"

    # Destination files & folders            Assumes existence of \Users\Test
    base_user_dir = Path(R'C:\Users\Test')

    if not Path(base_user_dir).is_dir():
        print('Base dir does not exist')
        input("press enter to continue and exit")
        return 1

    main_user_dir = Path(R'C:\Users\rotter')
    google_drive_dir = Path(R'G:\My Drive')
    alt_drive_dir = Path('F:\\')

    # RM_test_data_root is like GeneDB folder which will have database
    RM_test_root = base_user_dir / 'RM_test_root'
    # RM_test_data_root\media   will be the test media folder
    RM_test_media = RM_test_root / 'media'

     # Files to be created
    file_fldr_list =[
        #  Base folder          created test folder         Test File
        (google_drive_dir,    r'',                       'DBTest-file in GoogleDrive.txt'),

        (alt_drive_dir,       r'',                       'DBTest file -in abs dir1.txt'),
        (alt_drive_dir,       r'test dir to check TEF',  ''),
        (alt_drive_dir,       r'test dir to check TEF',  'DBTest file -in abs dir2.txt'),

        (main_user_dir,       r'',                       'DBTest file -in home dir1.txt'),

        (main_user_dir,       r'test dir to check TEF',  ''),
        (main_user_dir,       r'test dir to check TEF',  'DBTest file -in home dir2.txt'),

        (base_user_dir,       r'',                       'DBTest file -in home dir1.txt'),
        (base_user_dir,       r'test dir to check TEF',  ''),
        (base_user_dir,       r'test dir to check TEF',  'DBTest file -in home dir2.txt'),

        (base_user_dir,       r'RM_test_root',  ''),
        (base_user_dir,      r'RM_test_root',  'DBTest file -in database dir1.txt'),

        (base_user_dir,      r'RM_test_root\test dir',  ''),
        (base_user_dir,       r'RM_test_root\test dir',  'DBTest file -in database dir2.txt'),

        (base_user_dir,       r'RM_test_root\media',  ''),
        (base_user_dir,       r'RM_test_root\media',  'DBTest file 01.jpg'),
        (base_user_dir,       r'RM_test_root\media',  'DBTest file 02.jpg'),
        (base_user_dir,       r'RM_test_root\media',  'DBTest file 03.jpg'),
        (base_user_dir,       r'RM_test_root\media',  'DBTest file 04.jpg'),
        (base_user_dir,       r'RM_test_root\media',  'DBTest file 05.jpg'),

        (base_user_dir,       r'RM_test_root\media\sub1',  ''),
        (base_user_dir,       r'RM_test_root\media\sub1',  'DBTest file s1 01.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1',  'DBTest file s1 02.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1',  'DBTest file s1 03.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1',  'DBTest file ss1 dupFileName.jpg'),

        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  ''),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 01.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 02.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 03.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 dupFileName.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 dup_In_DB.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 trp_In_DB.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1',  'DBTest file ss1 Unref.jpg'),

        (base_user_dir,       r'RM_test_root\media\sub1\ssub1-unref',  ''),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1-unref',  'DBTest file ss1 unref01.jpg'),
        (base_user_dir,       r'RM_test_root\media\sub1\ssub1-unref',  'DBTest file ss1 unref02.jpg')

    ]

    # destination names
    db_file_dest = RM_test_root / test_db_file
    ignore_file_dest = RM_test_media / test_ignore_file
    ini_file_dest = RM_test_root / '..' / test_ini_file
    test_run_TEF_shortcut_1_dest = base_user_dir / test_run_TEF_shortcut_1
    test_run_TEF_shortcut_2_dest = base_user_dir / test_run_TEF_shortcut_2
    cmd_1_in_dest = base_user_dir / cmd_1
    cmd_2_in_dest = base_user_dir / cmd_2
    tef_app_in_dest = base_user_dir / tef_app

    if action == 'remove':
        if db_file_dest.exists():
            db_file_dest.unlink()
        if ignore_file_dest.exists():
            ignore_file_dest.unlink()
        if ini_file_dest.exists():
            ini_file_dest.unlink()
        if test_run_TEF_shortcut_1_dest.exists():
            test_run_TEF_shortcut_1_dest.unlink()
        if test_run_TEF_shortcut_2_dest.exists():
            test_run_TEF_shortcut_2_dest.unlink()
        if cmd_1_in_dest.exists():
            cmd_1_in_dest.unlink()
        if cmd_2_in_dest.exists():
            cmd_2_in_dest.unlink()
        if tef_app_in_dest.exists():
            tef_app_in_dest.unlink()

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

    # SRC names
    test_db_file_src              = test_db_home_fldr / test_db_file
    test_ignore_file_src          = test_files_home_fldr / test_ignore_file
    ini_file_src                  = test_files_home_fldr / test_ini_file
    test_run_TEF_shortcut_1_src  = test_files_home_fldr / test_run_TEF_shortcut_1
    test_run_TEF_shortcut_2_src  = test_files_home_fldr / test_run_TEF_shortcut_1
    cmd_1_in_src                = test_files_home_fldr / cmd_1
    cmd_2_in_src                = test_files_home_fldr / cmd_2
    tef_app_in_src              - tef_app_home / tef_app


    if action == 'create':
            # shutil.copyfile  src, dest
        if not db_file_dest.exists():
            shutil.copyfile( test_db_file_src, db_file_dest)
        if not ignore_file_dest.exists():
            shutil.copyfile(test_ignore_file_src, ignore_file_dest)
        if not ini_file_dest.exists():
            shutil.copyfile( ini_file_src, ini_file_dest)

        if not test_run_TEF_shortcut_1_dest.exists():
            shutil.copyfile( test_run_TEF_shortcut_1_src, test_run_TEF_shortcut_1_dest)
        if not test_run_TEF_shortcut_2_dest.exists():
            shutil.copyfile(  test_run_TEF_shortcut_2_src, test_run_TEF_shortcut_2_dest)

        if not cmd_1_in_dest.exists():
            shutil.copyfile( cmd_1_in_src, cmd_1_in_dest)
        if not cmd_2_in_dest.exists():
            shutil.copyfile( cmd_2_in_src, cmd_2_in_dest)
        if not tef_app_in_dest.exists():
            shutil.copyfile( tef_app_in_src, tef_app_in_dest)
    input("press enter to continue and exit")


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

