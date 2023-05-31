from reporter.reader import main, parse

if __name__ == '__main__':
    args = parse()
    print(main(args))
