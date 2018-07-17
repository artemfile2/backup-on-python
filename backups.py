import os
import datetime
import shutil
import time
import hashlib
import re

    # Название каталогов, которые получаю из файла list.st:
    # Читаю все строки (пути) и получаю список который необходимо делать копии

def md5hash(filePath):
    # проверка хеша файла
    file = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = file.read(8000)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def my_copytree(src, dst, symlinks=False, ignore=None):
    tit1 = time.time()
    # print ("Составление списка файлов исходного каталога")
    # Root - полный путь к каталогу
    # Files - список файлов в каталоге по указанному пути
    # dirs - список папок в каталоге по указанному пути
    for root, dirs, files in os.walk(src):
        for name in files:
            # print ("Получение полного пути к файлам")
            src_file = os.path.join(root, name)
            print("Копирование " + name)
            # print ("Состаление списка путей для копий")
            # Замена начала адресса, указанного как источник, конечным
            src = re.sub("^\s+|\n|\r|\s+$", '', src)
            dst_file = src_file.replace(src, os.path.join(dst, src.split('\\')[-2]+'\\'))

            s = md5hash(src_file)
            d = ''
            try:
                d = md5hash(dst_file)
            except:
                pass

            if s == d:
                pass

            if not os.path.exists(dst_file):
                # На этом этапе, в dst_file записаны адресса всех файлов
                # Исправление ошибок в симвалах пути
                path = os.path.realpath(dst_file)
                # Получение пути к каталогу, в котором находится файл
                dir = os.path.split(path)[0]
                # Проверка наличия папок на диске
                if not os.path.exists(dir):
                    # Создание папок
                    os.mkdir(dir)
            shutil.copy2(src_file, dst_file)

    tit2 = time.time()
    print ('скорость обработки: %.2f' % (tit2 - tit1))

def prepare():

    path_from = []
    FilelistFile = open('list.ls')
    for line in FilelistFile:
        path_from.append(line.replace('\n', ''))
    FilelistFile.close()

    RootFoldersFile = open('tobackup.ls')
    path_where = RootFoldersFile.readline()
    path_where.join(path_where.replace('\n', ''))
    RootFoldersFile.close()
    print("Копии будут сохранены в директории: {}\n".format(path_where))

    # делаю каталог для копий по текущему времени
    dt = datetime.datetime.now()
    currentdate = dt.strftime('%d_%m_%Y')
    path_where = path_where + currentdate + '\\'
    if not os.path.exists(path_where):
        os.mkdir(path_where)

    # скопируем все каталоги в созданный
    # копирование дерева  - откуда - куда
    for from_folder in path_from:
        if os.path.exists(from_folder):
            currentpath = os.path.basename(os.path.normpath(from_folder))
            print("\nИз " + from_folder + " копирование в " + path_where + currentpath + "...")
            my_copytree(from_folder, path_where)

    print("\nСоздание резервных копий законченно!")
    print("Для закрытия программы нажмите Enter")
    input()


if __name__ == "__main__":
    prepare()