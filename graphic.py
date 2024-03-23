import os
import logic
import tkinter as tk
import subprocess
from PIL import ImageTk, Image
import tkinter.messagebox as mb


def open_text():
    try:
        current_directory = os.getcwd()
        # Формируем путь к файлу "TestFile.txt" в текущей директории
        source_path = os.path.join(current_directory, "source.txt")

        subprocess.Popen(["start", "notepad", source_path], shell=True)
    except Exception as e:
        mb.showerror("Ошибка", f"Невозможно открыть файл: {e}")


def open_hash():
    try:
        current_directory = os.getcwd()
        # Формируем путь к файлу "TestFile.txt" в текущей директории
        source_path = os.path.join(current_directory, "ResultStr.txt")

        subprocess.Popen(["start", "notepad", source_path], shell=True)
    except Exception as e:
        mb.showerror("Ошибка", f"Невозможно открыть файл: {e}")


def open_test():
    try:
        current_directory = os.getcwd()
        # Формируем путь к файлу "TestFile.txt" в текущей директории
        source_path = os.path.join(current_directory, "TestFile.txt")

        subprocess.Popen(["start", "notepad", source_path], shell=True)
    except Exception as e:
        mb.showerror("Ошибка", f"Невозможно открыть файл: {e}")


def print_result_in_file(bit_str):
    output = open("ResultStr.txt", "w+")
    for bit in bit_str:
        output.write(str(bit))
    output.close()


def define_file_button():
    file = open("source.txt", "rb")
    m = file.read()
    file.close()

    result = logic.create_rand_num(int(m))
    print_result_in_file(result)


def define_ui_button(get_num):
    value = [int(x) for x in get_num.split(",")]

    result = logic.create_rand_num(value[0])
    print_result_in_file(result)


def define_test_button():
    input_file = open("ResultStr.txt", "r")
    m = input_file.read()
    input_file.close()
    clean = open("TestFile.txt", "w")
    clean.close()
    mass = []
    for elem in m:
        if elem == "0":
            mass.append(0)
        elif elem == "1":
            mass.append(1)

    test_1 = logic.frequency_test(mass)
    test_2 = logic.same_bits_test(mass)
    test_3 = logic.deviations_test(mass)
    mb.showinfo("Результаты тестов", "Частотный тест: {0}\nПоследовательность бит: {1}\nПроизвольные отклонения:"
                                     " {2}".format(test_1, test_2, test_3))


def initialization():
    root = tk.Tk()
    root.title("ИБ Лабораторная работа 3")
    img = Image.open("bg9try.jpg")
    width = 500
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.LANCZOS)
    image = ImageTk.PhotoImage(imag)
    tk.Label(root, image=image).pack(side="top", fill="both", expand="no")

    p_entry = tk.Entry(root, bd=5)
    p_entry.pack()

    tk.Button(root, text="Взять число\nиз интерфейса", command=lambda: define_ui_button(p_entry.get()), 
              activebackground="black").place(x=75, y=40)
    tk.Button(root, text="Взять число\nиз файла", command=lambda: define_file_button(), 
              activebackground="black").place(x=75, y=110)
    tk.Button(root, text="Провести\nтестирование", command=lambda: define_test_button(), 
              activebackground="black").place(x=75, y=180)
    tk.Button(root, text="Изменить входной\nфайл", command=open_text,
              activebackground="black").place(x=255, y=40)
    tk.Button(root, text="Посмотреть/Изменить\nрезультат", command=open_hash,
              activebackground="black").place(x=255, y=110)
    tk.Button(root, text="Посмотреть\nрезультат тестирования", command=open_test,
              activebackground="black").place(x=255, y=180)
    root.mainloop()


def begin():
    initialization()
