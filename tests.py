import unittest
import time
from emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.emulator = ShellEmulator(computer_name="user_name", path_to_arxiv="arch.tar", path_to_script=None)

    def test_ls_root(self):
        """Тест команды ls в корневой директории"""
        result = self._capture_output(self.emulator.ls, [])
        self.assertIn('dir1', result)  # Проверяем, что 'new_folder' присутствует в выводе

    def test_cd_and_ls(self):
        """Тест команды cd и ls внутри папки"""
        self.emulator.cd(["dir1"])  # Переходим в папку 'new_folder'
        result = self._capture_output(self.emulator.ls, [])
        self.assertIn('dir1/subdir', result)  # Проверяем, что 'content' находится в 'new_folder'

    def test_cd_back_to_root(self):
        """Тест команды cd для возвращения в корневую директорию"""
        self.emulator.cd(["dir1"])  # Переходим в папку 'new_folder'
        self.emulator.cd([".."])  # Возвращаемся в корневую директорию
        self.assertEqual(self.emulator.cwd, "/")  # Проверяем, что текущая директория - это корень

    def test_cd_absolute_path(self):
        """Тест команды  cd для перемещения по абсолютному пути"""
        self.emulator.cd(["dir1/subdir"])
        self.assertEqual(self.emulator.cwd, "/dir1/subdir/")  # Проверка, что текущий путь это введенный путь

    def test_cd_nonexistent_directory(self):
        """Тест ошибки при переходе в несуществующую директорию"""
        result = self._capture_output(self.emulator.cd, ["none_dir"])
        self.assertIn("No such file or directory", result)  # Проверяем, что выводится сообщение об ошибке

    def test_exit(self):
        """Тест команды exit"""
        with self.assertRaises(SystemExit):  # Ожидаем завершения программы
            self.emulator.exit()

    def test_pwd(self):
        """Тест команды pwd"""
        self.emulator.cd(["dir1"])
        result = self._capture_output(self.emulator.pwd, [])
        self.assertEqual(result.strip(), "/dir1/")

    def test_tail(self):
        """Тест команды tail"""
        self.emulator.cd(["dir1"])
        result = self._capture_output(self.emulator.tail, ["test.txt"])
        self.assertIn("test content", result)



    def test_du(self):
        """Тест команды du"""
        self.emulator.cd(["dir1"])
        result = self._capture_output(self.emulator.du, ["dir1"])
        self.assertIn("dir1 13 bytes", result)


    def _capture_output(self, func, args):
        from io import StringIO
        import sys
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            func(args)
            return out.getvalue()
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    unittest.main()