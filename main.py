import copy

from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave

start_image = imread('image.bmp')
image = copy.deepcopy(imread('image.bmp'))  # начальная картинка
with open('message.txt') as file:
    message = file.read()  # сообщение для шифрования
colors = [0, 1, 2]  # цвета rgb: 0 - r, 1 - g, 2 - b
bits = [5, 6, 7]  # номера битов для замены; отсчёт от нуля
percent = 30


def print_info():
    global count_of_embeding_symbols

    width = start_image.shape[0]
    height = start_image.shape[1]
    n = len(bits)
    c = len(colors)

    v = width * height * n * c
    count_of_embeding_symbols = (v * percent) // 100

    print(f"Максимальный встраиваемый объём информации = {v}")
    print(f"Число возможных символов для встраивания = {v // 8}")


def get_sequence():
    symbols = ['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')]
    return ''.join(symbols)


def insert_into(s, index, ch):
    return s[:index] + ch + s[index + 1:]


def set_pixel_bit(pixel, rgb, bit, value):
    color = '{:08b}'.format(pixel[rgb])
    color = color[:bit] + value + color[bit + 1:]
    pixel[rgb] = int(color, 2)


def embed_text_to_image(rgbs):
    number = 0
    sequence = get_sequence()
    sequence_length = len(sequence)

    for row in image:
        for pixel in row:
            for rgb in rgbs:
                for bit in bits:
                    set_pixel_bit(pixel, rgb, bit, sequence[number % sequence_length])

                    number += 1

                    if number == count_of_embeding_symbols:
                        return


if __name__ == '__main__':
    print_info()
    embed_text_to_image(colors)
    imsave('image2.bmp', image)
