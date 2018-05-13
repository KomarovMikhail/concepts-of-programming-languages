from linq import Range

if __name__ == '__main__':
    print(Range(range(10))
          .group_by(lambda x: x % 3)
          .to_list())

    print(Range(range(10))
          .select(lambda x: x ** 2)
          .where(lambda x: x % 2 == 0)
          .take(4)
          .to_list())

    print(Range(range(10))
          .order_by(lambda x: x % 3)
          .to_list())
