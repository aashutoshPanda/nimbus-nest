import pathlib
import shutil

def remove_folder(zip_dir):
    my_dir_to_delete = pathlib.Path(zip_dir)
    shutil.rmtree(my_dir_to_delete)
