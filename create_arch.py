import tarfile
from io import BytesIO


def create_test_archive(archive_path):
    with tarfile.open(archive_path, 'w') as tar:
        # Создаем директории
        for dir_name in ['dir1/', 'dir1/subdir/', 'dir2/']:
            info = tarfile.TarInfo(dir_name)
            info.type = tarfile.DIRTYPE
            tar.addfile(info)

        # Создаем тестовый файл
        test_content = b"test content\n"
        info = tarfile.TarInfo('dir1/test.txt')
        info.size = len(test_content)
        tar.addfile(info, BytesIO(test_content))

if __name__ == '__main__':
    create_test_archive("arch.tar")