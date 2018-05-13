from linq import Range


def fibonacci():
    f_1, f_2 = 0, 1
    count = 0
    while True:
        f_1, f_2 = f_2, f_1 + f_2
        if f_1 % 3 == 0:
            count += 1
        if count < 5:
            yield f_1
        else:
            yield f_1
            break


if __name__ == '__main__':
    print(Range(fibonacci())
          .where(lambda x: x % 3 == 0)
          .select(lambda x: (x ** 2) * (1 - x % 2) + x * (x % 2))
          .take(5)
          .to_list())
