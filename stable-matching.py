#!/usr/bin/env python3

class Mappings:
    def __init__(self):
        self.sellers = []
        self.buyers = []
        self.free_buyers = set()

    def add_free(self, buyer):
        self.free_buyers.add(buyer)

    def remove_free(self, buyer):
        self.free_buyers.remove(buyer)

    def stablematch(self):
        while(self.free_buyers):
            #AFAICT, Python does not support a non-removal method to access something in a set, so:
            buyer = self.free_buyers.pop()
            self.free_buyers.add(buyer)
            buyer.find_someone()

    def print(self):
        for buyer in self.buyers:
            print("Buyer %03d matches with sellers %s" % (buyer.ID, str([seller.ID for seller in buyer.current_engagements])))
    
class Participant:
    def update_data_source(self, mappings, ID):
        self.mappings = mappings
        self.ID = ID
        return self
        
class Seller(Participant):
    def __init__(self, ranked_buyer_idx_list):
        self.ranked_buyer_idx_list = ranked_buyer_idx_list
        self.current_buyer = None

    def propose(self, buyer):
        if(self.current_buyer is None):
            self.current_buyer = buyer
            return True

        #Find current & potential buyer's rank
        current_rank = self.ranked_buyer_idx_list.index(self.current_buyer.ID)
        new_rank = self.ranked_buyer_idx_list.index(buyer.ID)

        #If buyer's rank > current, unpropose and conditionally accept new buyer
        if(new_rank < current_rank):
            self.current_buyer.unpropose(self)
            self.current_buyer = buyer
            return True
        return False

class Buyer(Participant):
    def __init__(self, number_of_sellers, ranked_seller_idx_list):
        self.number_of_sellers = number_of_sellers
        self.ranked_seller_idx_list = ranked_seller_idx_list
        self.already_proposed = set()
        self.current_engagements = set()

    def unpropose(self, seller):
        self.current_engagements.remove(seller)
        self.mappings.add_free(self)

    def find_someone(self):
        for sellerID in self.ranked_seller_idx_list:
            if(sellerID not in self.already_proposed):
                self.already_proposed.add(sellerID)
                seller = self.mappings.sellers[sellerID]
                if(seller.propose(self)):
                    self.current_engagements.add(seller)
                    if(len(self.current_engagements) == self.number_of_sellers):
                        self.mappings.remove_free(self)
                    return True
        error("Couldn't find a seller for buyer %d" % self.ID)


def run(buyer_data, seller_data):
    mappings = Mappings()

    #for input checking
    last_buyer_idx = -1
    seller_count = -1
    cumulative_sellers_needed = 0

    for buyer_idx, number_of_sellers, *ranked_seller_list in buyer_data:
        if(buyer_idx != last_buyer_idx + 1):
            error("Incorrectly ordered buyers at %d" % buyer_idx)
        if(seller_count == -1):
            seller_count = len(ranked_seller_list)
        else:
            if(seller_count != len(ranked_seller_list)):
                error("Differing number of ranked sellers for buyer %d" % buyer_idx)

        #The actual meat and potatoes
        new_buyer = Buyer(number_of_sellers, ranked_seller_list)
        mappings.buyers.append(new_buyer.update_data_source(mappings, buyer_idx))
        mappings.add_free(new_buyer)
        
        last_buyer_idx = buyer_idx
        cumulative_sellers_needed += number_of_sellers

    if(cumulative_sellers_needed != seller_count):
        error("Number of ranked sellers does not match cumulative number of needed sellers")
    
    #for input checking
    last_seller_idx = -1

    for seller_idx, *ranked_buyer_list in seller_data:
        if(seller_idx != last_seller_idx + 1):
            error("Incorrectly ordered sellers at %d" % seller_idx)
        if(last_buyer_idx+1 != len(ranked_buyer_list)):
            error("Incorrect number of ranked buyers for seller %d" % seller_idx)

        #The actual meat and potatoes
        new_seller = Seller(ranked_buyer_list)
        mappings.sellers.append(new_seller.update_data_source(mappings, seller_idx))
        
        last_seller_idx = seller_idx

    if(last_seller_idx+1 != cumulative_sellers_needed):
        error("Number of sellers does not match the number needed by the buyers")
        
    mappings.stablematch()

    mappings.print()
        
#First test:
run([[0, 2, 0, 1, 2, 3],
     [1, 1, 1, 2, 3, 0],
     [2, 1, 0, 3, 2, 1]],
    [[0, 2, 1, 0],
     [1, 2, 1, 0],
     [2, 1, 2, 0],
     [3, 0, 1, 2]])
         
