from linq import Range

if __name__ == '__main__':
    print(Range([line for line in open('test')])
          .select(lambda x: x.split(' '))
          .flatten()
          .select(lambda x: (x, 1))
          .group_by(lambda x: x[0])
          .select(lambda x: (x[0], len(x[1])))
          .order_by(lambda x: -x[1])
          .to_list())
