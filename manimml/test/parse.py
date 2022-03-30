if __name__ == '__main__':
    # print(parse_kwargs('1, 2, num=3, test=a', {'a': 114514}))
    print(parse_kwargs('geometry["sphere"], material["sun"]', {
        'geometry': { 'sphere': 1111 },
        'material': { 'sun': 2222 },
    }))
