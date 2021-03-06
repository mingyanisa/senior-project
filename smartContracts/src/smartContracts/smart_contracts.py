from smartContracts.buyer import Buyer
from smartContracts.seller import Seller
from smartContracts.transaction import Transaction
from smartContracts.calculate_unit_price import *
from smartContracts.evaluation_matrix import updateEvalutaionIndex
# from seller import Seller
import random
def weighted_avg(buyers,sellers):
    buyers_sorted,sellers_sorted=natural_sorting(buyers,sellers)
    price=calculateAvgPrice(buyers_sorted)
    print(price)
    return trading_iterate(price,buyers_sorted,sellers_sorted) # return buyers, sellers 

def discriminatory_kda(buyers,sellers):
    k=1
    return dis_kda(k,buyers,sellers)

def uniform_kda(buyers,sellers):
    k=1
    return uni_kda(k,buyers,sellers)

def dis_kda(k,buyers,sellers):
    # print("buyers:",buyers,'\nseller:',sellers)
    print("DisKDA\nk:",k)
    buyers_sorted,sellers_sorted=natural_sorting(buyers,sellers)
    [seller.print_seller() for seller in sellers_sorted]
    i=0
    for buyer in buyers_sorted:
        if(buyer.quantityLeft==0):continue
        for seller in sellers_sorted:
            if(seller.quantityLeft==0 or buyer.quantityLeft==0): continue
            elif(seller.quantityLeft<=buyer.quantityLeft):
                print("seller<buyer")
                boughtQuantity = seller.quantityLeft
                buyer.quantityLeft-=seller.quantityLeft
                seller.quantityLeft=0
            else:
                print("seller>buyer")
                boughtQuantity = buyer.quantityLeft
                seller.quantityLeft-=buyer.quantityLeft
                buyer.quantityLeft=0
            price=calculateDisPrice(k,buyer.bidPrice,seller.reservePrice)
            buyer.transaction.append(Transaction(boughtQuantity,price))
            buyer.totalBoughtPrice+=price*boughtQuantity
            seller.transaction.append(Transaction(boughtQuantity,price))
            seller.totalSoldPrice+=price*boughtQuantity
            i+=1
            print("=======round ",i,"=========")
            seller.print_seller()
            print("*")
            buyer.print_buyer()
    buyersComplete,sellersComplete=addingGrid(buyers_sorted,sellers_sorted)
    buyersResult,sellersResult=updateEvalutaionIndex(buyersComplete,sellersComplete)
    return buyersResult,sellersResult

def uni_kda(k,buyers,sellers):
    buyers_sorted,sellers_sorted=natural_sorting(buyers,sellers)
    price=calculateUniPrice(k,buyers_sorted,sellers_sorted)
    print("UniKDA\nk:",k,"\nprice:",price)
    return trading_iterate(price,buyers_sorted,sellers_sorted) # return buyers, sellers 

def natural_sorting(buyers,sellers):
    return sorted(buyers,key=lambda buyer: buyer.bidPrice, reverse=True),sorted(sellers,key=lambda seller: seller.reservePrice, reverse=False)

def trading_iterate(price,buyers,sellers):
    listing=[]
    i=0
    for buyer in buyers:
        if(buyer.quantityLeft==0):continue
        for seller in sellers:
            if(seller.quantityLeft==0 or buyer.quantityLeft==0): continue
            elif(seller.quantityLeft<=buyer.quantityLeft):
                print("seller<buyer")
                boughtQuantity = seller.quantityLeft
                buyer.quantityLeft-=seller.quantityLeft
                seller.quantityLeft=0
            else:
                print("seller>buyer")
                boughtQuantity = buyer.quantityLeft
                seller.quantityLeft-=buyer.quantityLeft
                buyer.quantityLeft=0
            buyer.transaction.append(Transaction(boughtQuantity,price))
            buyer.totalBoughtPrice+=price*boughtQuantity
            seller.transaction.append(Transaction(boughtQuantity,price))
            seller.totalSoldPrice+=price*boughtQuantity
            i+=1
            print("=======round ",i,"=========")
            seller.print_seller()
            print("*")
            buyer.print_buyer()
            listing.append([seller,buyer])
    buyersComplete,sellersComplete=addingGrid(buyers,sellers)
    buyersResult,sellersResult=updateEvalutaionIndex(buyersComplete,sellersComplete)
    return buyersResult,sellersResult

def addingGrid(buyers,sellers):
    totalQuantityWantLeft=sum([buyer.quantityLeft for buyer in buyers])
    totalQuantityAvailableLeft=sum([seller.quantityLeft for seller in sellers])
    if(totalQuantityWantLeft>totalQuantityAvailableLeft):
        grid=Seller(totalQuantityWantLeft-totalQuantityAvailableLeft,5,True)
        for buyer in buyers:
            if(buyer.quantityLeft>0):
                buyer.totalBoughtPrice+=buyer.quantityLeft*grid.reservePrice
                buyer.transaction.append(Transaction(buyer.quantityLeft,grid.reservePrice))
                grid.transaction.append(Transaction(buyer.quantityLeft,grid.reservePrice))
                buyer.quantityLeft=0
    if(totalQuantityAvailableLeft>totalQuantityWantLeft):
        grid=Buyer(totalQuantityAvailableLeft-totalQuantityWantLeft,1.68,True)
        for seller in sellers:
            if(seller.quantityLeft>0):
                seller.totalSoldPrice+=seller.quantityLeft*grid.bidPrice
                seller.transaction.append(Transaction(seller.quantityLeft,grid.bidPrice))
                grid.transaction.append(Transaction(seller.quantityLeft,grid.bidPrice))
                seller.quantityLeft=0
    return buyers,sellers

