from __future__ import print_function
from __future__ import division
import numpy as np
from pygame.transform import scale
import config
import espControl as led

from virtualLed import VirtualLedTable


phase = 0
amplitude = 3
reverseAmp = False
reverseRGB = False
count_frames = 1

rgb = [np.linspace(0, 128, 256),
       np.linspace(0, 128, 256),
       np.linspace(128, 0, 256)]


def map1dto2d(pixels):
    width = 8
    mapped_pixels = []
    for color in pixels:
        rgb = np.zeros(config.N_PIXELS)
        for i in range(1, len(color)+1):
            if (i % width == 0):
                rgb[i-8:i] = np.mean(color[i-8:i])
        mapped_pixels.append(rgb)

    return mapped_pixels


def invertColumnIndex(n, i):
    if (i % 2 == 0):
        return n

    if n == 7:
        return 0
    elif n == 6:
        return 1
    elif n == 5:
        return 2
    elif n == 4:
        return 3
    elif n == 3:
        return 4
    elif n == 2:
        return 5
    elif n == 1:
        return 6
    else:
        return 7


def map1dto2d_plot(pixels):
    width = 8
    mapped_pixels = []
    for color in pixels:
        rgb = np.zeros(config.N_PIXELS)
        for i in range(1, len(color)+1):
            if (i % width == 0):
                rgb[i-width:i] = np.mean(color[i-width:i])
        mapped_pixels.append(rgb)

    # get max RGB amplitude of each stripe to determine plot's bar amplitude
    maxAmplitude = np.max(mapped_pixels, 0)

    # normalize to fit width's resolution
    maxAmplitude = maxAmplitude*width/64

    # keep rgb on according to the max amplitudes
    for i in range(len(mapped_pixels[0])):
        columIndex = invertColumnIndex(i % (width), int(i/width))
        if maxAmplitude[i] <= columIndex:
            mapped_pixels[0][i] = 0
            mapped_pixels[1][i] = 0
            mapped_pixels[2][i] = 0

    return mapped_pixels


def testing():
    rgb = [np.zeros(config.N_PIXELS), np.zeros(
        config.N_PIXELS), np.zeros(config.N_PIXELS)]

    rgb[0][0] = 128
    rgb[2][-1] = 128
    rgb[1][64] = 60

    return rgb


def map2dto1d(board):
    global count_frames, reverseRGB
    if (count_frames >= (len(rgb[0])-1) or count_frames <= 0):
        reverseRGB = not reverseRGB

    output = np.zeros([3, config.N_PIXELS])
    width = 8

    for i in range(len(output[0])):
        columIndex = invertColumnIndex(i % (width), int(i/width))
        if columIndex == board[int(i/width)]:
            output[0][i] = int(rgb[0][count_frames])
            output[2][i] = int(rgb[2][count_frames])

    if not reverseRGB:
        count_frames += 1
    else:
        count_frames -= 1

    return output


def map8x32to1x256(data):
    output = np.array([])
    for j in range(len(data[0])-1, -1, -1):
        if j % 2 == 0:
            rg = range(len(data))
        else:
            rg = range(len(data)-1, -1, -1)

        for i in rg:
            #   output.append(data[i][j])
            output = np.append(output, data[i][j])

    return output


def sin_static():
    global phase, amplitude, reverseAmp
    # raw
    x = np.linspace(phase + -2*np.pi, phase + 2*np.pi, 32)
    y = np.sin(x)*amplitude + 4
    print(x, y)
    # discretize y axis
    y_disc = y.astype(int)
    # mapping to 1d
    output = map2dto1d(y_disc)
    if (phase > 2*np.pi):
        phase = 0
        reverseAmp = not reverseAmp
    else:
        phase += 0.1

    return output


def distance_2d(x_point, y_point, x, y):
    return np.hypot(x-x_point, y-y_point)


def setMode(mode: str, vlt: VirtualLedTable) -> str:
    if (mode == 'pulse'):
        useRollingCenter = False

        R = np.zeros([8, 32])
        G = np.zeros([8, 32])
        B = np.zeros([8, 32])

        center = np.arange(0, 32)

        scale_factor = np.concatenate(
            (np.linspace(1, 3, 50), np.linspace(3, 1, 50)))

        center_pos = np.append(np.arange(0, 32, 1), np.arange(32, 0, -1))
        color_base = np.append(np.arange(1, 128, 1), np.arange(128, 1, -1))

        while True:

            # ---- mode: colormap -----
            # scale_factor: sets the aperture range on pulsar effect
            scale_factor = np.roll(scale_factor, -1)
            center_pos = [16, 3]
            color_base = np.roll(color_base, 1)

            if useRollingCenter:
                center_pos = np.roll(center_pos, 1)
                center = np.roll(center, 1)

            ys, xs = np.ogrid[0:8, 0:32]
            distances = distance_2d(center_pos[0], 3, xs, ys)

            distances = np.interp(distances, [np.min(distances), np.max(distances)], [
                                  20*scale_factor[0], 160])

            # print(distances)
            # print('\n\n\n')
            R, G, B = distances, distances - 64, distances - 128

            vlt.updateVirtualLedTable(R, G, B)

            led.pixels = [map8x32to1x256(
                R), map8x32to1x256(G), map8x32to1x256(B)]
            led.update()
            time.sleep(.05)

    if (mode == 'pulsar'):
        """
        submodes:
            colors: selection of multiple midsteps by defining color at that step'
            ini-to-end-to-ini: linear path from 2 defined limits
        """
        submode = 'ini-to-end-to-ini'

        if submode == 'colors':
            # c1 = [120, 20, 10]
            # c2 = [250, 130, 50]
            # c3 = [20, 10, 130]
            c1 = [10, 60, 10]
            c2 = [50, 10, 30]
            c3 = [0, 0, 0]
            step_transition = 100  # base: 100
            r_roll_base = np.concatenate((np.linspace(c1[0], c2[0], step_transition, dtype=int),
                                          np.linspace(
                c2[0], c3[0], step_transition, dtype=int),
                np.linspace(c3[0], c1[0], step_transition, dtype=int)))
            g_roll_base = np.concatenate((np.linspace(c1[1], c2[1], step_transition, dtype=int),
                                          np.linspace(
                c2[1], c3[1], step_transition, dtype=int),
                np.linspace(c3[1], c1[1], step_transition, dtype=int)))
            b_roll_base = np.concatenate((np.linspace(c1[2], c2[2], step_transition, dtype=int),
                                          np.linspace(
                c2[2], c3[2], step_transition, dtype=int),
                np.linspace(c3[2], c1[2], step_transition, dtype=int)))
        elif submode == 'ini-to-end-to-ini':
            # r_roll_base = np.arange(0, 125, 3)
            # g_roll_base = np.arange(0, 125, 3)

            """
                modo pulsar: 50 (eq1x3)
                modo psicodelia: 5 (eq1,2,1)
            """
            repeat_vel = 150

            r_roll_base = np.concatenate((np.linspace(
                0, 10, repeat_vel, dtype=int), np.linspace(10, 0, repeat_vel, dtype=int)))
            g_roll_base = np.concatenate((np.linspace(
                0, 10, repeat_vel, dtype=int), np.linspace(10, 0, repeat_vel, dtype=int)))
            b_roll_base = np.concatenate((np.linspace(
                10, 0, repeat_vel, dtype=int), np.linspace(0, 10, repeat_vel, dtype=int)))
        else:
            raise Exception('unkonwn submode')

        R = np.zeros([8, 32])
        G = np.zeros([8, 32])
        B = np.zeros([8, 32])

        center = (16, 4)
        y, x = np.ogrid[0:8, 0:32]
        distances = distance_2d(center[0], center[1], x, y)

        while True:
            r_roll_base = np.roll(r_roll_base, -1)
            g_roll_base = np.roll(g_roll_base, -1)
            b_roll_base = np.roll(b_roll_base, -1)

            for i in range(len(distances)):
                for j in range(len(distances[0])):

                    mapping_dist_eq1 = int(distances[i, j]) * 10  # linear
                    mapping_dist_eq2 = int(
                        distances[i, j] * distances[i, j])  # exponencial

                    # R[i, j] = np.roll(
                    #     r_roll_base, mapping_dist_eq1)[0]
                    G[i, j] = np.roll(
                        g_roll_base, mapping_dist_eq1)[0]
                    B[i, j] = np.roll(
                        b_roll_base, mapping_dist_eq1)[0]

            vlt.updateVirtualLedTable(R, G, B)

            led.pixels = [map8x32to1x256(
                R), map8x32to1x256(G), map8x32to1x256(B)]
            led.update()
            time.sleep(.05)


if __name__ == '__main__':
    import time

    vlt = VirtualLedTable()
    setMode('pulsar', vlt)

    vlt.closeGame()


# if __name__ == '__main__':
#     import time
#     # Turn all pixels off
#     # led.pixels *= 0
#     # led.pixels[0, 0] = 255  # Set 1st pixel red
#     # led.pixels[1, 1] = 255  # Set 2nd pixel green
#     # led.pixels[2, 2] = 255  # Set 3rd pixel blue
#     R = np.zeros([8, 32])
#     G = np.zeros([8, 32])
#     B = np.zeros([8, 32])
#     R[:,:4] = [[128,0,0,0], [0,128,0,0], [0,0,128,0], [0,0,0,128], [0,0,0,128], [0,0,128,0], [0,128,0,0], [128,0,0,0]]
#     G[:,1:5] = [[128,0,0,0], [0,128,0,0], [0,0,128,0], [0,0,0,128], [0,0,0,128], [0,0,128,0], [0,128,0,0], [128,0,0,0]]
#     B[:,2:6] = [[128,0,0,0], [0,128,0,0], [0,0,128,0], [0,0,0,128], [0,0,0,128], [0,0,128,0], [0,128,0,0], [128,0,0,0]]

#     center = np.arange(0, 32)

#     scale_factor = np.concatenate((np.linspace(1,3,50),np.linspace(3,1,50)))
#     # scale_factor = np.concatenate((np.linspace(0,160,50),np.linspace(160,0,50)))
#     # scale_factor = np.linspace(0,255,200)
#     # print(scale_factor)

#     vlt = VirtualLedTable()

#     center_pos = np.append(np.arange(0,32,1), np.arange(32,0, -1))
#     color_base = np.append(np.arange(1,128,1), np.arange(128,1,-1))

#     while True:
#         # led.pixels = np.roll(led.pixels, 1, axis=1)
#         # sin = sin_static()
#         # print(sin)
#         # print(led.pixels)
#         # matrix = np.zeros([8, 32])
#         # matrix[2:6,10:14] = [[128,128,128,128], [128, 0, 0, 128], [128, 0, 0, 128], [128,128,128,128]]
#         # matrix[2:6, 15:19] = np.tile(128, (4,4))

#         # ---- mode: sin changuing rgb -----
#         # R = np.roll(R, 1, axis=1)
#         # G = np.roll(G, 1, axis=1)
#         # B = np.roll(B, 1, axis=1)


#         # ---- mode: colormap -----
#         # scale_factor: sets the aperture range on pulsar effect
#         scale_factor = np.roll(scale_factor, -1)
#         center_pos = [16, 3]
#         # center_pos = np.roll(center_pos, 1)
#         color_base = np.roll(color_base, 1)

#         #center = np.roll(center, 1)
#         ys, xs = np.ogrid[0:8, 0:32]
#         distances = distance_2d(center_pos[0], 3, xs, ys)
#         distances = np.interp(distances, [np.min(distances), np.max(distances)], [20*scale_factor[0], 160])
#         # distances = np.interp(distances, [np.min(distances), np.max(distances)], [scale_factor[0], 255])
#         R,G,B = distances, distances - 64, distances - 128
#         # R,G,B = distances, distances - 64, color_base[0] * np.ones((8, 32))


#         vlt.updateVirtualLedTable(R, G, B)

#         led.pixels = [map8x32to1x256(R), map8x32to1x256(G), map8x32to1x256(B)]
#         led.update()
#         time.sleep(.05)

#     vlt.closeGame()
