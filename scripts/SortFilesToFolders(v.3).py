import shutil, os, re, datetime, plyer, logging

# Создание log-файла, путь которого указан в скобках
logfile = os.path.join('D:\\', 'VIDEO', 'TRASSA', 'EXPORT', 'log.txt')
logging.basicConfig(level=logging.DEBUG, filemode='a', filename=logfile)

# Создание переменной, содержащей путь к рабочему каталогу
workingDirectory = os.path.join('D:\\', 'VIDEO', 'TRASSA', 'EXPORT')

# Создание регулярного выражения, которому соответствуют имена каталогов
# с существующими заданиями
taskFoldersRegex = re.compile(r'\w*-\d*-\d{2}-\d{2}')

# Создание регулярного выражения, которому соответствуют имена файлов,
# необходимых для перемещения в папку с соответствующей датой
dateFindRegex = re.compile(r"""(.*\.?_) # весь текст перед датой
	(20\d{2})-							# 4 цифры года	
	(\d{2})-							# 2 цифры месяца
	(\d{2})_							# 2 цифры числа
	(.*)								# весь текст после даты
	""", re.VERBOSE)

# Создание регулярного выражения, которому соответствуют имена каталогов
# с датами в каталогах с заданиями
archiveFoldersRegex = re.compile(r"""(20\d{2})-		# 4 цифры года
	(\d{2})-										# 2 цифры месяца
	(\d{2})											# 2 цифры числа
	""", re.VERBOSE)

# Организация цикла по папкам в рабочем каталоге
for videoFolders in os.listdir(workingDirectory):
    mo1 = taskFoldersRegex.search(videoFolders)
    # Пропуск каталогов с именами, не подходящих регулярному выражению
    if mo1 == None:
        continue

    # Создание переменной, содержащей путь к рабочему каталогу задания
    taskWorkingDirectory = os.path.join(workingDirectory, videoFolders)

    # Организация цикла по файлам в рабочем каталоге задания
    for videoFile in os.listdir(taskWorkingDirectory):
        mo2 = dateFindRegex.search(videoFile)
        # Пропуск файлов с именами, не подходящих регулярному выражению
        if mo2 == None:
            continue

        # Получение отдельных частей имен файлов
        yearPart = mo2.group(2)
        monthPart = mo2.group(3)
        dayPart = mo2.group(4)

        # Создание переменной, содержащей имя каталога для перебираемых файлов
        videoArchive = yearPart + '-' + monthPart + '-' + dayPart
        # Создание переменной, содержащей путь каталога для перебираемых файлов
        videoArchiveMove = os.path.join(taskWorkingDirectory, videoArchive)
        # Создание переменной, содержащей путь к перебираемому файлу
        videoFileMove = os.path.join(taskWorkingDirectory, videoFile)

        # Проверяем существует ли каталог для перебираемых файлов
        if os.path.exists(videoArchiveMove) == True:
            pass
        elif os.path.exists(videoArchiveMove) == False:
            # Создаем каталог для перебираемых файлов
            os.mkdir(videoArchiveMove)
        # print('Создан каталог: ', videoArchiveMove)
        else:
            plyer.notification.notify(
                message='Произошла ошибка при сортировке видеофайлов в рабочий каталог',
                app_name='SortFilesToFolders',
                title='Error script')
            print("Произошла ошибка при сортировке видеофайлов в рабочий каталог: ", videoArchiveMove)

        # Перемещаем файл в соответствующий его дате каталог с проверкой на ошибки(ошибки фиксируем в log-файле)
        try:
            shutil.move(videoFileMove, videoArchiveMove)
            print('Перемещен файл: ', videoFile)
        except:
            logging.debug("Move exception")
            logging.exception(str(os.path.abspath(videoFileMove)))
            logging.debug(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            logging.debug('\n')

    # Организация цикла по каталогам с датами в рабочем каталоге задания
    for dateFolders in os.listdir(taskWorkingDirectory):
        mo3 = archiveFoldersRegex.search(dateFolders)
        # Пропуск файлов и катологов с именами, не подходящих регулярному выражению
        if mo3 == None:
            continue

        # Получение отдельных частей имен катологов
        yearPart = int(mo3.group(1))
        monthPart = int(mo3.group(2))
        dayPart = int(mo3.group(3))

        # Создание переменной, имеющей значение текущей даты(Тип:timedelta)
        dt = datetime.datetime.now()
        # Срок хранения файлов(кол-во дней)
        archiveDays = datetime.timedelta(days=30)
        # Минимальная дата для хранимых файлов(Тип:timedelta)
        dt = dt - archiveDays
        # Перевод имён каталогов(YYYY-MM-DD) типа: str в тип: timedelta
        dateFilesBox = datetime.datetime(yearPart, monthPart, dayPart)

        # Сравнения минимальной даты с датой каждого католога
        if dt >= dateFilesBox:
            # Создание переменной, содержащей путь к катологу, который необходимо удалить
            deleteFolders = os.path.join(taskWorkingDirectory, dateFolders)
            try:
                shutil.rmtree(deleteFolders)
                print('Удален каталог: ', deleteFolders)
            except:
                logging.debug("Remove exception")
                logging.exception(str(os.path.abspath(deleteFolders)))
                logging.debug(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                logging.debug('\n')
        else:
            # print('Каталоги, требующие удаления, отсутствуют!')
            pass