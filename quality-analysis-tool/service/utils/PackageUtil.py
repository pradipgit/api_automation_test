import zipfile
import os


class PackageUtil:

    def __init__(self):
        pass

    @staticmethod
    def zip_folder(src_directory, dst_directory, output_file_name):
        zip_file = zipfile.ZipFile(output_file_name, "w")

        for directory, sub_directories, files in os.walk(src_directory):
            for file in files:
                zip_file.write(dst_directory + '/' + file)

        zip_file.close()