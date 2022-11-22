
def find_first_coprime(b,start=2):
    from math import gcd        

    def check_co_prime(num, M):
        return gcd(num, M) == 1 

    def get_smallest_co_prime(M):
        # for i in range(start, M): # for every number *i* starting from 2 up to M
        i = start
        while True:
            i += 1
            if check_co_prime(i, M): # check if *i* is coprime with M
                return i # if it is, return i as the result

    return get_smallest_co_prime(b)

def main():
    n = 8
    b = n
    a = find_first_coprime(b,start=b+1)
    a=5
    print(a,b,n)
    for i in range(n):
        print('%03i %i'%(i,i*a % b))
    
if __name__ == "__main__":
    main()