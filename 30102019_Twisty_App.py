import pandas as pd
import numpy as np
import glob

empty_list = [] #creates empty list

for file in glob.glob("*.chanjo_txt"): #creates a list of filenames to use in the loop, finds all files within the folder the .py file is located with the .chanjo_txt file type
    df = pd.read_csv(file, header = None, names= ['EntrezGeneIDmapped','above20x','Average'], usecols =  [
        'EntrezGeneIDmapped','above20x'], delimiter='\t') #reads each file found by the loop above, adds headers, removes columns that aren't needed 
    df = df.astype('str') #converts the dataframe to a string so it can be put into a list
    df ["Sample"] = file.split("_")[2] #splits filename by _ and adds second item from split which is the individual patient ID, then adds it to the dataframe as a new column
    empty_list.append(df) #appends each dataframe to the empty list

data = pd.concat(empty_list, axis=0, ignore_index=True) #concatenates all dataframes in list to create one file containing all information needed from all .chanjo_txt files
   
gene_names_sheet = pd.read_csv("EntrezID.csv")  #Pulling in the EntrezID sheet into a dataframe to change gene numbers to Entrez IDs

merged_data = pd.merge(data, #Merging data from both sheets to match Entrez ID and gene name
         gene_names_sheet,
         on='EntrezGeneIDmapped',
         how= 'inner')

merged_data = merged_data.drop(['EntrezGeneIDmapped'], axis = 1) #Deleting redundant EntrezID column

final_data = merged_data.reindex(columns=['Sample', 'ApprovedSymbol','above20x']) #Moving approved symbol column to specified location


final_data.rename(columns={'ApprovedSymbol':'Gene'}, inplace = True) #Changing headers to match specified


np.savetxt('Shiny_app_data_final.txt', final_data, fmt='%s', comments= '', header="Sample Gene Above20x") #Creating an output .txt file for final data set

