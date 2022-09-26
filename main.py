from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave
import copy

image = copy.deepcopy(imread('image.bmp'))  # начальная картинка
with open('message.txt') as file:
    message = file.read()  # сообщение для шифрования
colors = [1]  # цвета rgb
bits = [8]  # номера битов для замены

test = [[[1, 2, 3], [4, 2, 3]],
        [[7, 2, 3], [10, 2, 3]],
        [[1, 2, 3], [4, 2, 3]],
        [[7, 2, 3], [10, 2, 3]]]


def get_sequence():
    symbols = ['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')]
    return ''.join(symbols)


def set_pixel_bit(pixel, rgb, value):
    color = '{:08b}'.format(pixel[rgb])
    color = color[:7] + value
    pixel[rgb] = int(color, 2)


def embed_text_to_image(rgbs):
    number = 0
    sequence = get_sequence()
    sequence_length = len(sequence)

    for row in image:
        for pixel in row:
            for rgb in rgbs:
                set_pixel_bit(pixel, rgb, sequence[number])

                number += 1

                if number == sequence_length:
                    return

    a = 1


if __name__ == '__main__':
    embed_text_to_image(colors)
    imsave('image2.bmp', image)
