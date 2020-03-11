strokesDictReverse = {
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
    'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20,
    'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30,
    'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, '0': 0
}

soundWeight = 0.5
shapeWeight = 1 - soundWeight


def compute_sound_code_similarity(sound_code1, sound_code2):  # soundCode = ['2', '8', '5', '2']

    feature_size = len(sound_code1)
    wights = [0.4, 0.4, 0.1, 0.1]
    multiplier = []
    for i in range(feature_size):
        if sound_code1[i] == sound_code2[i]:
            multiplier.append(1)
        else:
            multiplier.append(0)
    sound_similarity = 0
    for i in range(feature_size):
        sound_similarity += wights[i]*multiplier[i]
    return sound_similarity


def compute_shape_code_similarity(shape_code1, shape_code2):  # shapeCode = ['5', '6', '0', '1', '0', '3', '8']

    feature_size = len(shape_code1)
    wights = [0.25, 0.1, 0.1, 0.1, 0.1, 0.1, 0.25]
    multiplier = []
    for i in range(feature_size-1):
        if shape_code1[i] == shape_code2[i]:
            multiplier.append(1)
        else:
            multiplier.append(0)
    multiplier.append(
        1 - abs(strokesDictReverse[shape_code1[-1]]-strokesDictReverse[shape_code2[-1]]) * 1.0
        / max(strokesDictReverse[shape_code1[-1]], strokesDictReverse[shape_code2[-1]])
    )
    shape_similarity = 0
    for i in range(feature_size):
        shape_similarity += wights[i]*multiplier[i]
    return shape_similarity


def compute_ssc_similaruty(ssc1, ssc2, ssc_encode_way):
    # return 0.5 * compute_sound_code_similarity(ssc1[:4], ssc2[:4])
    # + 0.5 * compute_shape_code_similarity(ssc1[4:], ssc2[4:])

    if ssc_encode_way == "SOUND":
        return compute_sound_code_similarity(ssc1, ssc2)
    elif ssc_encode_way == "SHAPE":
        return compute_shape_code_similarity(ssc1, ssc2)
    else:
        sound_simi = compute_sound_code_similarity(ssc1[:4], ssc2[:4])
        shape_simi = compute_shape_code_similarity(ssc1[4:], ssc2[4:])
        return soundWeight * sound_simi + shapeWeight * shape_simi
