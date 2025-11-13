class Math:
    @staticmethod
    def add(*args):
        print(sum(args))
        return sum(args)
    
    @staticmethod
    def mul(*args):
        prod = 1
        for i in args:
            prod*=i
        print(prod)
        return prod
    
