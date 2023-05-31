# ++ выдача ошибки если повторяются номера страниц - взять более свежий файл https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
#        -- файлы с 4.1 выдаются как ошибка, хотя не должны
# -- добавить водяной знак
# -- сделать автора в метаданных
# https://stackoverflow.com/questions/46849733/change-metadata-of-pdf-file-with-pypdf2

import PyPDF2 as PDF
import os, re
import datetime
import ctypes
from shutil import copy2

def writeComments(changeFile, message):
	print(changeFile)
	print(message)
	with open(changeFile, 'a', encoding = "utf8") as chOut:
		chOut.writelines(outFileName+"\n")
		chOut.writelines(message)
		
def doComment(changeFile):
	add_suffix = None
	try:	
		with open(changeFile, 'r', encoding = "utf8") as chIn:
			lines = []
			for line in chIn.readlines():
				line = line.strip('\n').lstrip()
				if line: lines.append(line)

			print('<==================>\n' +
				  '\n'.join(lines) +
				  '<==================>'
				  )

			add_suffix = lines[-1].lstrip()
			if len(add_suffix) > 1 and add_suffix[0] == '!':
				add_suffix = add_suffix[1:]
			else:
				add_suffix = None

	except FileNotFoundError:
		print('Файл {changeFile} не найден.')
		
	print("Комментарий (пустая строка - завершить; !суффикс - в первой строке, добавит к имени файла):")
	if add_suffix:
		print('Предложение суффикса: ', add_suffix)
		
	txt ="."
	message = ""
	lines = 0	
	while 1:
		txt = input()
		if txt == '': break
		if lines == 0 and txt[0]=='!' and len(txt)>1:
			add_suffix = txt[1:]
		message+=f"\t\t{txt}\n"
		lines+=1

	if lines < 2: 
		message = "\t\t<-- Сборка без коментариев -->\n"
		if add_suffix:
			message += f'!{add_suffix}\n'

	return message, add_suffix


def makeDirDialog(dirName):
	if not os.path.isdir(work_dir):
		print("Папка не существует")
		answer = askDialog("Создать папку?")
		print(answer)
		if answer != "" and answer in "yд":
			print(f"Создаю папку '{dirName}'")
			os.makedirs(dirName)
		else:
			print(f"Выходим")
			exit(0)

	else:
		print("Папка найдена!")

def askDialog(msg, answers = ("ynдн"), tries = 3):
	answer = "."
	n = 0
	while (answer not in answers or answer == "") and n < tries:
		answer = input(f"{msg} [{tries-n}] ({answers}): ").lower()
		n+=1
	return answer

# try: 
# 	from pdfwatermark import pdfwatermark
# 	watermaktConnected = True
# except:
# 	watermaktConnected = False
# 	print("!!! Модуль с водяным знаком не подключен !!!")

template_file = 'PDF_merge.py'
base_name = os.path.basename(__file__)

if base_name == template_file:
	slug = input('Короткое название проекта ( PDF_project_name ): ')
	copy2(template_file, f'PDF_{slug}.py')
	if not (os.path.exists('README.md') and
	        os.path.exists('.gitignore')): # если мы кодим, то не удалять!
		os.remove(template_file)
	exit(0)

try:
	print("Поиск папки")
	work_dir = re.findall("PDF_.*\.py", base_name)[0][0:-3]
	print(f"Пробую \\{work_dir}")
except IndexError:
	print("Путь не задан. Использую поумолчанию.")
	work_dir = u"PDF"
# Пробуем создать папку из имени файла
makeDirDialog(work_dir)
work_dir+="\\"
proj_name = u"NoName"
# work_dir = u"pdf\\"
needWatermark = True
watermark_path = "watermark.pdf"
print (os.getcwd()+"\\"+work_dir)

pdfs = []
pdfs2 = [] #для тех что без номеров
# взять имя проекта из файла
projFile = work_dir + u"project.txt"
changeFile = work_dir + u"changelog.txt"
try:
	with open (projFile, "r", encoding = "utf-8") as pr_file:
		proj_name = pr_file.readline()#.decode("windows-1251")
except FileNotFoundError:
	proj_name = input("Название проекта:")
	if proj_name == "":
		proj_name = "noname"
	try:
		with open (projFile, "w", encoding = "utf8") as pr_file:
			pr_file.writelines(proj_name)
	except:
		print(f"Ошибка при сохранении названия проекта '{proj_name}' в файл '{projFile}'")
	
print ("Проект: ",str(proj_name))

proj_name = str(proj_name)
# имя результирующего файла
# .strftime("%Y-%m-%d %H:%M:%S:%f")
# datePrefix = 
prefix = datetime.datetime.now().strftime("%Y-%m-%d")
suffix = datetime.datetime.now().strftime("%H%M")
# outFileName = datetime.datetime.now().strftime(f"%Y-%m-%d {proj_name} (%H%M).pdf")
addSuffix = ""
message = ""

message, suff = doComment(changeFile)
if suff: addSuffix=f" - {suff}"

outFileName = f"{prefix} {proj_name}{addSuffix}({suffix}).pdf"
writeComments(changeFile, message)

n = 1
counter = 0
try:
	for file in os.listdir(work_dir):
		counter +=1
		if file[-4:].lower() == ".pdf":
			x = 0
			while file[x] in ("0123456789."): # определение количества цифр в начале файла
				x = x + 1
			if x:
				n = float(file[0:x])
				pdfs.append((n, file))
			else:
				patt = re.search("^((\D){,3}\d{1,4}(\.\d{,2})?)", file) #
				try:
					print("pattern >>>", patt.group(0))
					number = re.search("\d{1,4}(\.\d{,2})?", patt.group(0))
					n = float(number.group(0))
					print("n=",n)
				except:
					n = counter
				
				pdfs2.append((n, file))
	pdfs = sorted(pdfs)
	pdfs.extend(sorted(pdfs2))
	# print (pdfs)

	
				
except FileNotFoundError:
	input("Ошибка при поиске файлов для обработки...")
	exit()
	
if counter == 0:
	input("Нет файлов .pdf для обработки...")
	exit()
	
# проверка на повторные номера
for i in range(len(pdfs)):
	if i>0:
		if pdfs[i-1][0] == pdfs [i][0]:
			# print () #pdfs[i-1][1].decode("windows-1251"), pdfs[i][1].decode("windows-1251")
			input(f"ОШИБКА - повтор номера страницы {pdfs[i][0]}\nНажми enter чтобы продолжить")

merger = PDF.PdfMerger(strict = False)

for pdf in pdfs:
	fname = work_dir + pdf[1]
	print (fname)
	# x = open(fname, "rb")
	# print x.readlines()
	merger.append(PDF.PdfReader(work_dir + pdf[1], 'rb'))
outFileName=outFileName.replace("\n","")
print ("Всего " + str(len(pdfs)) + " .pdf файлов")
print (u"Записываем в '" + outFileName)
        
with open(outFileName, 'wb') as fout:        
	merger.write(fout)
	print ("готово")
	# https://stackoverflow.com/questions/7343388/open-pdf-with-default-program-in-windows-7
	# https://stackoverflow.com/questions/434597/open-document-with-default-application-in-python
	# почему-то не работает с z:\ с пробелами
	# f = f'cmd /c start "" "{fullName}"'
	# print (f)
	# subprocess.call(f)
	# print("Открываю ", fullName )
	# os.system(fullName)


path = os.getcwd()
shell32 = ctypes.windll.shell32
fullName = "\"" + path + "\\" + outFileName + "\""
# subprocess.run([sys.executable, fullName])
shell32.ShellExecuteA(0,"open",repr(fullName),0,0,5)
print(fullName)

# exit(0)
	
# if watermaktConnected:	
	# try:
		# if needWatermark:
			# print (u"Делаем водяной знак...")
			# pdfwatermark(watermark_path, outFileName, "_" + outFileName)
			# print (u"... готово")
		# input("Нажми ENTER что бы выйти...")
	# except:
		# input("произошла ошибка")
