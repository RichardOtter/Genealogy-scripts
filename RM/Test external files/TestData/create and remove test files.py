# ===================================================DIV60==
import sys
import os
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


    file_list =[]

#    file_list.append( (r'C:\Users\rotter\Test', 'sample', 'DBTest file -in database dir1.txt'))
#    file_list.append( (r'C:\Users\rotter', '', 'DBTest file -test test.txt'))

#                        Base folder                           created test folder         Test File
    file_list.append( (r'G:\My Drive',                         '',                        'DBTest-file in GoogleDrive.txt '))
    file_list.append( (r'C:\Users\rotter\Genealogy\GeneDB',   '',                        'DBTest file -in database dir1.txt'))
    file_list.append( (r'C:\Users\rotter\Genealogy\GeneDB',   'test dir to check TEF',   'DBTest file -in database dir2.txt'))
    file_list.append( (r'C:\Users\rotter',                    '',                        'DBTest file -in home dir1.txt '))
    file_list.append( (r'C:\Users\rotter',                    'test dir to check TEF',   'DBTest file -in home dir2.txt '))
    file_list.append( (r'F:' + '\\',                          '',                        'DBTest file -in abs dir1.txt'))
    file_list.append( (r'F:'+'\\',                            'test dir to check TEF',   'DBTest file -in abs dir2.txt '))


    for file in file_list:
        print (file)
        folder_path = Path(file[0]) / file[1]
        print(folder_path)
        file_path = folder_path / file[2]
        print(file_path)

        if sys.argv[1] == 'remove':
            try:
                os.remove(file_path)
            except:
                pass
            if (file[1] !=''             # created a test folder)
                        and is_folder_empty_os(folder_path)):
                os.rmdir(folder_path)    # safe- won't remove unless empty

        elif sys.argv[1] == 'create':
            try:
                os.mkdir(folder_path)
            except:
                pass
            touch_file(file_path)
        else:
            print( f'argument {sys.argv[1]} unknown')
    return






def touch_file(filename):
    try:
        os.utime(filename, None)  # Update access and modification times
    except OSError:
        # If the file doesn't exist, create it in append mode and close immediately
        with open(filename, mode='w'):
            pass

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

