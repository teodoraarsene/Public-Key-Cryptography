import time


def gcd_division(a, b):
    if (b == 0):
         return a
    return gcd(b, a%b)

def gcd_subtraction(a, b):
    while (a != b):
        if (a > b):
            a -= b
        else:
            b -= a
    return a

def gcd(a, b):
  result = min(a, b)
   
  while result:
    if a % result == 0 and b % result == 0:
      break

    result -= 1
   
  return result

def measure_running_time(algo, a, b):
    start_time = time.process_time_ns()
    #print('start: ' + str(start_time))

    result = algo(a, b)

    end_time = time.process_time_ns()
    #print('end: ' + str(end_time))

    return result, end_time - start_time

if __name__ == '__main__':
    inputs = [(10, 15), (270, 192), (72, 12), (3, 5), (98, 56), (36, 60), (2740, 1760), (30, 50), (24, 18), (15, 75)]

    for (a, b) in inputs:
        result1, elapsed_time1 = measure_running_time(gcd_division, a, b)
        print ('gcd_division(' + str(a) + ', ' + str(b) + ') = ' + str(result1) + '\telapsed time: ' + str(elapsed_time1))

        result2, elapsed_time2 = measure_running_time(gcd_subtraction, a, b)
        print ('gcd_subtraction(' + str(a) + ', ' + str(b) + ') = ' + str(result2) + '\telapsed time: ' + str(elapsed_time2))

        result3, elapsed_time3 = measure_running_time(gcd, a, b)
        print ('gcd3(' + str(a) + ', ' + str(b) + ') = ' + str(result3) + '\t\ttelapsed time: ' + str(elapsed_time3))
