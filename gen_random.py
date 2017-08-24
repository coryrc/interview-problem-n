import random
num_sellers = 13
num_buyers = 6

fb = open('buyers.csv','w')
remaining_sellers = num_sellers
for i in range(num_buyers):
    print("On buyer %d, remaining sellers %d, how many sellers?" % (i,remaining_sellers))
    sellers = int(input())
    remaining_sellers -= sellers
    seller_priority = list(range(num_sellers))
    random.shuffle(seller_priority)
    fb.write(",".join(map(str,[i,sellers]+seller_priority)) + "\n")


print("sellers:")
for i in range(num_sellers):
    buyer_priority = list(range(num_buyers))
    random.shuffle(buyer_priority)
    print(",".join(map(str,[i]+buyer_priority)))
    
