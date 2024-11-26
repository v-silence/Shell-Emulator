import os
import tarfile
import argparse

import xml.etree.ElementTree as ET
import logging
import tempfile
current_dir = "/"


def get_current_dir():
    return current_dir
class ShellEmulator:
    def __init__(self,computer_name ="default",path_to_arxiv="arch.tar",path_to_log="log.xml",path_to_script = ""):
        self.computer_name = computer_name
        self.path_to_tar = path_to_arxiv
        self.log_file = path_to_log
        self.startup_script = path_to_script
        self.cwd = '/'
        self.commands_logged = []
        # Setup logging
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

        # Load the tar file as a virtual filesystem
        self.virtual_fs = tarfile.open(self.path_to_tar, 'r')

    def log_action(self, action):
        self.commands_logged.append(action)
        logging.info(action)

    def close_log(self):
        # Save actions to XML at the end of the session
        root = ET.Element("session")
        for cmd in self.commands_logged:
            ET.SubElement(root, "command").text = cmd
        tree = ET.ElementTree(root)
        tree.write(self.log_file, encoding='utf-8', xml_declaration=True)

    def run_script(self, script_path):
        with open(script_path, 'r') as script:
            for line in script:
                self.execute_command(line.strip())

    def execute_command(self, command):
        if not command:
            return

        commands = command.split()
        cmd = commands[0]
        args = commands[1:]

        if cmd == 'cd':
            self.cd(args)
        elif cmd == 'ls':
            self.ls(args)
        elif cmd == 'exit':
            self.exit()
        elif cmd == 'pwd':
            self.pwd(args)
        elif cmd == 'tail':
            self.tail(args)
        elif cmd == 'du':
            self.du(args)
        elif cmd == 'mkdir':
            self.mkdir(args)
        else:
            print(f"{cmd}: unknown command")

        # Log the command execution
        self.log_action(command)


    def cd(self, args):
        if not args:
            return

        target = args[0]

        # Обработка перехода в корневую директорию
        if target == '/':
            self.cwd = '/'
            return

        # Обработка перехода на уровень выше
        if target == '..':
            if self.cwd == '/':
                return
            self.cwd = os.path.dirname(self.cwd.rstrip('/'))
            if not self.cwd:
                self.cwd = '/'
            return

        # Обработка перехода в текущую директорию
        if target == '.':
            return

        # Обработка перехода по абсолютному пути
        if self.is_path_exist(self.cwd + target + '/'):
            self.cwd = os.path.join(self.cwd, target) + '/'
            return

        # Обработка перехода по относительному пути
        if self.is_path_exist(target + '/'):
            self.cwd = target + '/'
            return

        # Если директория не найдена
        print(f"cd: {target}: No such file or directory")

    def ls(self, args):
        if len(args) == 1:
            prev_cwd = self.cwd
            self.cd(args)
            self.ls([])
            self.cd(prev_cwd)
        elif len(args) == 0:
            list_of_paths = self.virtual_fs.getnames()
            for path in list_of_paths:
                if (self.cwd == '/' + path[0:len(self.cwd) - 1]):
                    print(path)
        else:
            print("Error: wrong option/s")

    def exit(self):
        print("Bye!")
        self.virtual_fs.close()
        self.close_log()
        exit(0)

    def pwd(self,args):
        print(self.cwd)

    def tail(self, args):
        if not args:
            print("Usage: tail <filename> [<lines>]")
            return

        filename = args[0]
        num_lines = int(args[1]) if len(args) > 1 else 10

        # Ищем файл по имени в текущей директории
        for path in self.virtual_fs.getnames():
            if path.endswith('/' + filename):
                file_content = self.virtual_fs.extractfile(path).read().decode('utf-8')
                lines = file_content.splitlines()
                print("\n".join(lines[-num_lines:]))
                return

        # Если не нашли, ищем по полному пути
        if self.is_file_exist(filename):
            file_content = self.virtual_fs.extractfile(filename).read().decode('utf-8')
            lines = file_content.splitlines()
            print("\n".join(lines[-num_lines:]))
        else:
            print(f"{filename}: No such file")

    def du(self, args):
        if not args:
            print("Usage: du <directory>")
            return

        directory = args[0]

        # Обработка перехода в корневую директорию
        if directory == '/':
            total_size = sum(tinfo.size for tinfo in self.virtual_fs.getmembers() if tinfo.name != '/')
            print(f"/ {total_size} bytes")
            return

        # Проверяем, существует ли указанная директория
        if not self.is_path_exist(directory):
            print(f"{directory}: No such directory")
            return

        # Вычисляем размер директории
        total_size = 0
        for path in self.virtual_fs.getnames():
            if path.startswith(directory + '/'):
                total_size += self.virtual_fs.getmember(path).size

        print(f"{directory} {total_size} bytes")


    def run(self):
        if self.startup_script:
            self.run_script(self.startup_script)
        try:
            while True:
                command = input(f"{self.computer_name}:{self.cwd}> ")
                self.execute_command(command)
        except KeyboardInterrupt:
            self.exit()

    def is_path_exist(self, path):
        if path == '/':
            return True

            # Удаляем ведущий и trailing слэш, если есть
        path = path.strip('/')

        # Получаем список всех файлов и директорий в архиве
        file_list = self.virtual_fs.getnames()

        # Проверяем, есть ли указанный путь в списке
        for item in file_list:
            if item.startswith(path + '/') or item == path:
                return True

        return False

    def is_file_exist(self, filename):
        with tarfile.open(self.path_to_tar, 'r') as tar:
            file_list = tar.getnames()
            return filename in file_list


def args_parser():
    parser = argparse.ArgumentParser(description="Эмулятор Shell")
    parser.add_argument("computer_name", nargs="?", help="Имя пользователя", default="username")
    parser.add_argument("path_to_arxiv", nargs="?", help="Путь до виртуальной файловой системы",
                        default="arch.tar")
    parser.add_argument("path_to_log", nargs="?", help="Путь до лог файла",
                        default="log.xml")
    parser.add_argument("path_to_script", nargs="?", default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = args_parser()
    emulator = ShellEmulator(args.computer_name, args.path_to_arxiv, args.path_to_log, args.path_to_script)
    emulator.run()
