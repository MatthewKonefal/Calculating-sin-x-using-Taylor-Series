''' This program calculates the sine of a float using a Taylor series expansion.
    This process is implemented as follows:

    Step 1 - Adjust the float (by adding or subtracting multiples of 2pi) so that it lies in the range [-pi,pi].
    Step 2 - Form a Taylor series expansion about -pi, -pi/2, 0, pi/2 or pi, whichever is closest.
    Step 3 - Add up some number of terms of this expansion.
'''

#Use the Bailey–Borwein–Plouffe formula to yield pi.
#Alternately, pi could be imported from the math module.
PI = 0
for term in range(500):
    PI += 1/16**term*(4/(8*term+1) - 2/(8*term+4) - 1/(8*term+5) - 1/(8*term+6))

def factorial(val,soFar=1):
    '''Caculate the factorial of val.'''
    #This is calculated recursively; the soFar parameter holds the interim results of the calculation.
    #Each succesive call reduces val by one, and multplies the soFar value by val.
    #Therefore, by the time val gets to 0, soFar will hold the factorial of the original val.
    assert isinstance(val,int)     #val must be an integer otherwise this function will not terminate.
    if val == 0:
        return soFar
    else:
        return factorial(val-1,soFar*val)

def getInRange(val):
    '''Adjust val (by adding or subtracting multiples of 2pi) so that it lies in the range [-pi,pi].'''
    return (val+PI)%(2*PI)-PI

def getTerm(termNumber,sinAndCosVals,dif):
    '''Get the 'termNumber'th term of the Taylor Series expansion. '''
    #The nth term of the Taylor Series expansion of sin(x) about a looks like:
    #   nth_derivate_of_sin(x)_at_a * (dif**n)
    #   -------------------------------------
    #                      n!
    #Since the nth derivate of sin(x) is periodic with order 4, we can use modulo to determine what that should look like.
    #The 4k+0th derivative at a is sin(a) which is the first number in the sinAndCosVals tuple.
    #The 4k+1th derivative at a is cos(a) which is the second number in the sinAndCosVals tuple.
    #The 4k+2th derivative at a is -sin(a) which is the negative of the first number in the sinAndCosVals tuple.
    #The 4k+3th derivative at a is -cos(a) which is the negative of the second number in the sinAndCosVals tuple.
    #Using this information, calculate the value of the term and return it.
    if termNumber%4 == 0:
        return (sinAndCosVals[0] * dif**termNumber) / factorial(termNumber)
    elif termNumber%4 == 1:
        return (sinAndCosVals[1] * dif**termNumber) / factorial(termNumber)
    elif termNumber%4 == 2:
        return (-sinAndCosVals[0] * dif**termNumber) / factorial(termNumber)
    else:
        return (-sinAndCosVals[1] * dif**termNumber) / factorial(termNumber)

def sin(val,howManyTerms=50):
    '''Calculate the sine of val, using the first howManyTerms of the Taylor series expansion.'''
    #Adjust val (by adding or subtracting multiples of 2pi) so that it lies in the range [-pi,pi].
    val = getInRange(val)
    #Decide where to do the Taylor series about, based on which of -pi,-pi/2,0,pi/2 and pi is closest to val.
    #The sinAndCosVals tuple represents the (sine,cosine) of the aboutWhere value.
    #These values will be used in the Taylor series as the derivatives of sine are all ±sine or ±cosine.
    if val < PI*-0.75:
        aboutWhere = -PI
        sinAndCosVals = (0,-1)
    elif val < PI*-0.25:
        aboutWhere = -PI/2
        sinAndCosVals = (-1,0)
    elif val < PI*0.25:
        aboutWhere = 0
        sinAndCosVals = (0,1)
    elif val < PI*0.75:
        aboutWhere = PI/2
        sinAndCosVals = (1,0)
    else:
        aboutWhere = PI
        sinAndCosVals = (0,-1)
    #Calculate the difference between val and aboutWhere, which will be used in the Taylor expansion.
    dif = val - aboutWhere
    result = 0
    #Add each term to the result.
    for termNumber in range(howManyTerms):
        result += getTerm(termNumber,sinAndCosVals,dif)
    #Return the result.
    return result

##Example:
##>>> sin(1)
##0.8414709848078965
##>>> sin(2)
##0.9092974268256817
##>>> sin(3)
##0.1411200080598671
##>>> sin(4)
##-0.7568024953079284
##>>> sin(5)
##-0.9589242746631383
