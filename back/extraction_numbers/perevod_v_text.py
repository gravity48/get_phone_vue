'''
Обработчик перевода doc, docx материала в текст
'''
from DocHeandler import DocHeandler


if __name__ == '__main__':
    path_in = '/mnt/in/'
    path_out = '/mnt/out/'
    ip_base = "localhost"
    heandler = DocHeandler(input_dir=path_in, output_dir=path_out, ip_base=ip_base)
    Status, FilesListIn = heandler.headler_file_in()
    if Status:
        print("Process ok")
    pass
