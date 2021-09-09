def main():
    from random import randint
    print_count = randint(1, 25)
    while print_count > 0:
        print_count -= 1
        print('good bye cruel world')

if __name__ == '__main__':
    main()
