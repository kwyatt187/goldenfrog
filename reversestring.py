import argparse


def reversestring(string):
    result = []
    vowels = {'a':'', 'e':'', 'i':'', 'o':'', 'u':''}
    for i in range(len(string)-1,-1,-1):
        if string[i] in vowels:
            result.append(string[i].upper())
        else:
            result.append(string[i].lower())

    return ''.join(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str, help='String to operate on')
    args = parser.parse_args()
    
    print reversestring(args.string)
