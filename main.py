import copy

import xlsxwriter
from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave

start_image = imread('image.bmp')
image = copy.deepcopy(imread('image.bmp'))  # начальная картинка
# with open('message.txt') as file:
#     message = file.read()  # сообщение для шифрования
RGBcolors = [0, 1, 2]  # цвета rgb: 0 - r, 1 - g, 2 - b
bits = [5, 6, 7]  # номера битов для замены; отсчёт от нуля
percent = 5

first_24_values_of_blue = [start_image[i // start_image.shape[0]][i % 24][2] for i in range(24)]


def print_header():
    width = start_image.shape[0]
    height = start_image.shape[1]
    n = len(bits)
    c = len(RGBcolors)

    print(f"Высота = {width} пикселей")
    print(f"Ширина = {height} пикселей")
    print(f"Максимальный встраиваемый объём информации:")
    print(f"Если используются последний бит и одна компонента цвета: {width} * {height} * 1 * 1 / 8 = {(width * height) // 8} символов")
    print(f"Если используются последний бит и все три компоненты цвета: {width} * {height} * 1 * 3 / 8 = {(width * height * 3) // 8} символов")
    print(f"Если используются два последних бита и одна компонента цвета: {width} * {height} * 2 * 1 / 8 = {(width * height * 2) // 8} символов")
    print(f"Если используются два последних бита и все три компоненты цвета: {width} * {height} * 2 * 3 / 8 = {(width * height * 2 * 3) // 8} символов")
    print(f"Если используются три последних младших бита и одна компонента цвета: {width} * {height} * 3 * 1 / 8 = {(width * height * 3) // 8} символов")
    print(
        f"Если используются три последних младших бита и все три компоненты цвета: {width} * {height} * 3 * 3 / 8 = {(width * height * 3 * 3) // 8} символов")


def write_row(worksheet, name, row, items):
    worksheet.write(row, 0, name)

    for i in range(len(items)):
        worksheet.write(row, i + 1, items[i])


def print_tables():
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()

    # evaluations
    column_numbers = [j + 1 for j in range(24)]
    first_24_symbols_of_message = [s for s in message[:9]]
    first_24_symbols_of_message_in_bits = ['{:08b}'.format(bytearray(symbol, 'utf-8')[0]) for symbol in
                                           first_24_symbols_of_message]
    sequence = ''.join(first_24_symbols_of_message_in_bits)

    first_24_values_in_bits = ['{:08b}'.format(number) for number in first_24_values_of_blue]

    i = 0
    change_last_bit = []
    for value in first_24_values_in_bits:
        change_last_bit.append(value[:7] + sequence[i])
        i += 1
    change_last_value = [int(b, 2) for b in change_last_bit]

    i = 0
    change_two_bits = []
    for value in first_24_values_in_bits:
        change_two_bits.append(value[:6] + sequence[i] + sequence[i + 1])
        i += 2
    change_two_value = [int(b, 2) for b in change_two_bits]

    i = 0
    change_three_bits = []
    for value in first_24_values_in_bits:
        change_three_bits.append(value[:5] + sequence[i] + sequence[i + 1] + sequence[i + 2])
        i += 3
    change_three_value = [int(b, 2) for b in change_three_bits]

    # print to excel
    write_row(worksheet, "Первые 9 символов сообщения", 0, first_24_symbols_of_message)
    write_row(worksheet, "Биты первых 9 символов сообщения", 1, first_24_symbols_of_message_in_bits)
    write_row(worksheet, "Первые 24 значения синей цветовой компоненты", 4, first_24_values_of_blue)
    write_row(worksheet, "Биты первых 24 значений синей цветовой компоненты", 5, first_24_values_in_bits)
    write_row(worksheet, "Биты первых 24 значений синей цветовой компоненты после встраивания 1 бита", 7,
              change_last_bit)
    write_row(worksheet, "Биты первых 24 значений синей цветовой компоненты после встраивания 2 бит", 8,
              change_two_bits)
    write_row(worksheet, "Биты первых 24 значений синей цветовой компоненты после встраивания 3 бит", 9,
              change_three_bits)
    write_row(worksheet, "Первые 24 значения синей цветовой компоненты после встраивания 1 бита", 11, change_last_value)
    write_row(worksheet, "Первые 24 значения синей цветовой компоненты после встраивания 2 бит", 12, change_two_value)
    write_row(worksheet, "Первые 24 значения синей цветовой компоненты после встраивания 3 бит", 13, change_three_value)

    # print to console
    print()
    print('|'.join(f"{i + 1:^8}" for i in range(24)))
    print('|'.join(f"{number:^8}" for number in first_24_values_of_blue))
    print('|'.join(first_24_values_in_bits))

    workbook.close()


def print_info():
    global count_of_embeding_symbols

    width = start_image.shape[0]
    height = start_image.shape[1]
    n = len(bits)
    c = len(RGBcolors)

    v = width * height * n * c
    count_of_embeding_symbols = (v * percent) // 100

    print()
    print(f"Для текущих настроек:")
    print(f"Максимальный встраиваемый объём информации = {v} бит")
    print(f"Число возможных символов для встраивания = {v // 8} символов")


def get_sequence():
    symbols = ['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')]
    return ''.join(symbols)


def insert_into(s, index, ch):
    return s[:index] + ch + s[index + 1:]


def set_pixel_bit(pixel, rgb, bit, value):
    color = '{:08b}'.format(pixel[rgb])
    color = color[:bit] + value + color[bit + 1:]
    pixel[rgb] = int(color, 2)


def insert_text_to_image():
    with open('message.txt') as file:
        message = file.read()
    number = 0
    text_for_embed = ''.join(['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')])
    text_length = len(text_for_embed)

    for row in image:
        for pixel in row:
            for RGBcolor in RGBcolors:
                for bit in bits:
                    set_pixel_bit(pixel, RGBcolor, bit, text_for_embed[number % text_length])
                    clr = '{:08b}'.format(pixel[RGBcolor])
                    clr = clr[:bit] + text_for_embed[number % text_length] + clr[bit + 1:]
                    pixel[RGBcolor] = int(clr, 2)

                    number += 1

                    if number == count_of_embeding_symbols:
                        return


if __name__ == '__main__':
    print_header()
    print_tables()
    print_info()
    insert_text_to_image()
    imsave('image2.bmp', image)
