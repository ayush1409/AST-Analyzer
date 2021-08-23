# Python program to check if difference between sum of
# odd digits and sum of even digits is 0 or not

def isDiff(n):
	return (n % 11 == 0)

# Driver code
n = 1243;
if (isDiff(n)):
	print("Yes")
else:
	print("No")