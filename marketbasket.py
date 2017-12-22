# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 00:16:45 2017

@author: Amogh Gupta

Support count = Number of times an itemset is present in dataset (transactions)

Confidence c(X->Y)=sup(XUY)/sup(X)

"""
import csv
import pandas as pd

frequency_dict=dict()


def get_support_value(percentage,num_of_transactions):
#  Ex:For 4 items, if sup_per=50%,
#      support=(50/100)*4=2   
    support_val = ((percentage/100)*num_of_transactions)
    return support_val

def aprioriFirst(dataset, support):
#1 generating 1_itemset by considering support value

    frequencyset= set()
    for a in dataset:
        #Build frequencyset to store all unique items({'Milk', 'Beer', 'Cola', 'Bread', 'Diapers', 'Eggs'})
        frequencyset=frequencyset.union(a)

    #oneitemset is to calculate first frequency set
    oneitemset=set()
    for ab in frequencyset:
        temp=0
        for b in dataset:
            if ab in b:
                temp+=1
        if temp >= support: 
            oneitemset.add(ab)
    return(frequencyset, oneitemset)
            

 

def removedup(l):
    """
        To remove the duplicate items in the given list, by creating a new list
        without duplicates
    """
    nl=list()
    for i in l:
        if i not in nl:
            nl.append(i)
    return nl

def generateSets(itemset, k, frequencyset,dataset):
     #List of (k-1) itemsets
     #frequencyset has all the items
    kitemset=list()
    fset=frequencyset.copy()
    for a in itemset:
        fset=fset-a
        #fset now has items which are not there in itemset
        for b in fset:
            kitemset.append((a|{b}))
            #sets has k itemset with duplicates
    kitemset=removedup(kitemset)
    return kitemset
    

def simplifyset(dataset,kitemset,support):
    #Anti monotone property (support count)
    #dataset is list of transactions
    min_set = list()
    for s in kitemset:
        #For each set in kitemset
        temp = 0
        for d in dataset:
            #Number of subsets returns the frequency of kitemset
            if s.issubset(d):
                temp += 1
        if temp >= support:
            min_set.append(s)
    min_set = removedup(min_set)        
    return min_set



def aprioriGen(dataset,support,oneitemset,frequencyset):
    #List of sets for oneitemset
    oneitem_list = list()
    for a in oneitemset:
        temp = set()
        temp.add(a)
        oneitem_list.append(temp)
    #apriori
    k=2    
    kitemset = oneitem_list.copy()
    if kitemset == []:
        return kitemset
    while(True):
        #k_1itemset is k-1 itemset
        k_1itemset = kitemset.copy()
        kitemset = generateSets(kitemset,k,frequencyset,dataset)
        kitemset = simplifyset(dataset,kitemset,support)
        if kitemset==[]:
            return k_1itemset
        k+=1    
        
    return kitemset

def sup(sett,dataset):
    count=0
    for i in dataset:
       if sett.issubset(i):
           count+=1
    return count        


def powerset(s):
    
    #To create powerset of s
    result=[[]]
    for elem in s:
        result.extend([x+[elem] for x in result])
        
    power=list()
    #To convert it into list of sets
    for i in result:
        temp=set()
        for t in i:
            temp.add(t)
        power.append(temp)

    return power




def ruleGen(kitemset,dataset,conp):
   # ruleflag=1
    
    print('Rules-')
    ruleno=0
    
    for i in kitemset:
        items=list()  
        
        
        reset=powerset(i)
  
        for t in reset:
            if(len(t)!=0 and len(t)!=len(i)):
                #ruleflag=0
                items.append(t)

        for s in items:
            #s->i-s
            num=sup(i,dataset)
            den=sup(s,dataset)
            fset=i-s
            
    
             #Confidence c(X->Y)=sup(XUY)/sup(X)
            if(den!=0):
                conf=num/den
                
            if(conf>=conp):
                ruleno+=1
                print(ruleno,s,'->',fset,' with confidence = ',conf)
        
    if(ruleno==0):
        print('Sorry, No rules could be deduced with given support and confidence values')
    return    

def market_basket_run(dataset,sup_per,con_percentage):
    (all_set,first_set) = aprioriFirst(dataset,support)
    kitemset= aprioriGen(dataset,support,first_set,all_set)
    if len(kitemset)==0:
        print ("Sorry No item could be bought with this support threshold")
    else:    
        print("The items that are frequently bought together(using the specified support threshold):")
        df2=pd.DataFrame(kitemset)
        print(df2)
        print('----------------------------------------------------------------------------')    
        ruleGen(kitemset,dataset,con_percentage)

    




#dataset=[['bread','milk'],['bread','diapers','beer','eggs'],['milk','diapers','beer','cola'],['bread','milk','diapers','beer'],['bread','milk','diapers','cola']]
dataset=list()

#Dataset of transactions
fp=open('dataset.txt','r')
reader = csv.reader(fp, delimiter=',')
for row in reader:
    rset=set(row)
    dataset.append(rset)

#Displaying the transactions
print('Transactions are as follows:')
df=pd.DataFrame(dataset)
print(df)



#Enter the support percentage and get its value
sup_per=int(input('Enter the support value in percentage:'))
#Threshold support value
support=get_support_value(sup_per,len(dataset))
support=int(support)

if(support<1):
    print("Support is less than 1")
    

confidence=int(input('Enter the confidence value in percentage'))
confidence=confidence/100

print('------------------------------------------------------------')

kitemset= market_basket_run(dataset,support,confidence)






