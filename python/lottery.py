import random


def get_theticket():
	lotto2 = [54, 12, 7, 23, 3, 13]
	# for x in range(5):
	# 	x = random.randint(0,70)
	# 	lotto2.append(x)
	# y = random.randint(0,26)
	# lotto2.append(y)
	return lotto2




def get_random_ticket():
	lotto = []
	for x in range(5):
		x = random.randint(0,70)
		pp = False
		while pp == False:
			if x in lotto:
				x = random.randint(0,70)
			else:
				pp = True
		lotto.append(x)
	y = random.randint(0,26)
	lotto.append(y)
	return lotto



def see_if_equal():
	x = False
	count = 0
	r = get_theticket()
	while(x == False):
		t = get_random_ticket()
		for i in r:
			if i not in t:
				x = False
				break
			else:
				x = True

		if x == False:
			count += 1
			print(str(count) + "\n")
		else:
			print("Congrats it took you " + str(count) + " tries")

	
	


see_if_equal()


def main():


	if __name__ == "__main__":
		main()

