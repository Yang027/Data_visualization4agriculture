'''

@author:a108222015 a108222026 a108222027
@date:2022 06 07
@project:final Data Preprocessing

'''

import os
inPath = os.path.join("..", "input")
outPath = os.path.join("..", "output")

import pandas as pd

# 農業進出口 bar動態圖
def excel1():

    #imports
    im = pd.read_csv(inPath + "/imports.csv")
    print('import info',im.info())
    im = im.drop(columns=['Indicator Name', 'Indicator Code'])
    im = pd.melt(im, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='imports')
    im = im.dropna()
    print('import info-----------melt--------\n')
    im.info()
    print('import head(10)\n')
    print(im.head(10))

    print("-----------------------------------------------")

    #exports
    ex = pd.read_csv(inPath + "/exports.csv")
    print('export info', ex.info())
    ex = ex.drop(columns=['Indicator Name', 'Indicator Code'])
    ex = pd.melt(ex, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='exports')
    ex = ex.dropna()
    print('export info-----------melt--------\n')
    ex.info()
    print('export head(10)\n')
    print(ex.head(10))

    print("-----------------------------------------------")

    # region
    region = pd.read_csv(inPath + "/all.csv")
    print('region info', region.info())
    region = region.drop(columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'intermediate-region', 'region-code', 'sub-region-code', 'intermediate-region-code'])
    print('region head(10)\n')
    print(region.head(10))

    ex1 = pd.merge(im, ex,on=['Country Name','Country Code','year'],how='inner')
    ex1 = pd.merge(ex1, region, right_on='name', left_on='Country Name', how='inner')
    ex1 = ex1.drop(columns=['name'])
    print("ex1 info-->", ex1.info())
    print('imports exports head(10)\n')
    print(ex1.head(10))

    ex1.to_csv(inPath + "/ex1.csv")

#農業土地占比 依照年分畫GEO 動態圖
def excel2():

    # AgriculturalLand
    agriculturalLand = pd.read_csv(inPath + "/AgriculturalLand.csv")
    print('agriculturalLand info', agriculturalLand.info())
    agriculturalLand = agriculturalLand.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalLand = pd.melt(agriculturalLand, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='agriculturalLand')
    agriculturalLand = agriculturalLand.dropna()
    print('agriculturalLand info-----------melt--------\n')
    agriculturalLand.info()
    print('agriculturalLand head(10)\n')
    print(agriculturalLand.head(10))

    print("-----------------------------------------------")

    # Agriculture_GDP
    agriculturalGDP = pd.read_csv(inPath + "/Agriculture_GDP.csv")
    print('Agriculture_GDP info', agriculturalGDP.info())
    agriculturalGDP = agriculturalGDP.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalGDP = pd.melt(agriculturalGDP, id_vars=['Country Name', 'Country Code'], var_name='year',
                              value_name='agriculturalGDP')
    agriculturalGDP = agriculturalGDP.dropna()
    print('Agriculture_GDP info-----------melt--------\n')
    agriculturalGDP.info()
    print('Agriculture_GDP head(10)\n')
    print(agriculturalGDP.head(10))

    ex2 = pd.merge(agriculturalLand, agriculturalGDP,on=['Country Name','Country Code','year'],how='inner')

    ex2.to_csv(inPath + "/ex2.csv")

#Agriculture, forestry, and fishing, value added (% of GDP) vs Agricultural machinery, tractors per 100 sq. km of arable land
#(GDP vs machinery) 農業GDP與農業機械化程度是否有關
def excel3():

    # Agriculture_GDP
    agriculturalGDP = pd.read_csv(inPath + "/Agriculture_GDP.csv")
    print('Agriculture_GDP info', agriculturalGDP.info())
    agriculturalGDP = agriculturalGDP.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalGDP = pd.melt(agriculturalGDP, id_vars=['Country Name', 'Country Code'], var_name='year',value_name='agriculturalGDP')
    agriculturalGDP = agriculturalGDP.dropna()
    print('Agriculture_GDP info-----------melt--------\n')
    agriculturalGDP.info()
    print('Agriculture_GDP head(10)\n')
    print(agriculturalGDP.head(10))

    print("-----------------------------------------------")

    # AgriculturalMachinery
    agriculturalMachinery = pd.read_csv(inPath + "/AgriculturalMachinery.csv")
    print('export info', agriculturalMachinery.info())
    agriculturalMachinery = agriculturalMachinery.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalMachinery = pd.melt(agriculturalMachinery, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='agriculturalMachinery')
    agriculturalMachinery = agriculturalMachinery.dropna()
    print('AgriculturalMachinery info-----------melt--------\n')
    agriculturalMachinery.info()
    print('AgriculturalMachinery head(10)\n')
    print(agriculturalMachinery.head(10))

    print("-----------------------------------------------")

    # region
    region = pd.read_csv(inPath + "/all.csv")
    print('region info', region.info())
    region = region.drop(
        columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'intermediate-region', 'region-code',
                 'sub-region-code', 'intermediate-region-code'])
    print('region head(10)\n')
    print(region.head(10))

    print("-----------------------------------------------")

    # GDP
    GDP = pd.read_csv(inPath + "/GDP.csv")
    print('GDP info', GDP.info())
    GDP = GDP.drop(columns=['Indicator Name', 'Indicator Code'])
    GDP = pd.melt(GDP, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='GDP')
    GDP = GDP.dropna()
    print('GDP info-----------melt--------\n')
    GDP.info()
    print('GDP head(10)\n')
    print(GDP.head(10))

    ex3 = pd.merge(agriculturalGDP, agriculturalMachinery, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex3 = pd.merge(ex3, GDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex3 = pd.merge(ex3, region, right_on='name', left_on='Country Name', how='inner')

    #農業GDP美金為單位
    ex3['aGDP'] = ex3['agriculturalGDP'] * ex3['GDP']

    print("ex3 info-->", ex3.info())
    print('ex3 head(10)\n')
    print(ex3.head(10))

    ex3.to_csv(inPath + "/ex3.csv")

#AgriculturalLand vs AgriculturalMachinery 土地與機械化程度
def excel4():
    # AgriculturalLand
    agriculturalLand = pd.read_csv(inPath + "/AgriculturalLand.csv")
    print('agriculturalLand info', agriculturalLand.info())
    agriculturalLand = agriculturalLand.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalLand = pd.melt(agriculturalLand, id_vars=['Country Name', 'Country Code'], var_name='year',
                               value_name='agriculturalLand')
    agriculturalLand = agriculturalLand.dropna()
    print('agriculturalLand info-----------melt--------\n')
    agriculturalLand.info()
    print('agriculturalLand head(10)\n')
    print(agriculturalLand.head(10))

    print("-----------------------------------------------")

    # AgriculturalMachinery
    agriculturalMachinery = pd.read_csv(inPath + "/AgriculturalMachinery.csv")
    print('export info', agriculturalMachinery.info())
    agriculturalMachinery = agriculturalMachinery.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalMachinery = pd.melt(agriculturalMachinery, id_vars=['Country Name', 'Country Code'], var_name='year',
                                    value_name='agriculturalMachinery')
    agriculturalMachinery = agriculturalMachinery.dropna()
    print('AgriculturalMachinery info-----------melt--------\n')
    agriculturalMachinery.info()
    print('AgriculturalMachinery head(10)\n')
    print(agriculturalMachinery.head(10))

    ex4 = pd.merge(agriculturalLand, agriculturalMachinery, on=['Country Name', 'Country Code', 'year'], how='inner')
    print("ex4 info-->", ex4.info())
    print('ex4 head(10)\n')
    print(ex4.head(10))

    # region
    region = pd.read_csv(inPath + "/all.csv")
    print('region info', region.info())
    region = region.drop(
        columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'intermediate-region', 'region-code',
                 'sub-region-code', 'intermediate-region-code'])
    print('region head(10)\n')
    print(region.head(10))

    # ex1 = pd.merge(im,ex,on=['Country Name','Country Code','year'],how='inner')
    ex4 = pd.merge(ex4, region, right_on='name', left_on='Country Name', how='inner')
    ex4 = ex4.drop(columns=['name'])
    print("ex4 info-->", ex4.info())
    print('imports exports head(10)\n')
    print(ex4.head(10))

    ex4.to_csv(inPath + "/ex4_new .csv")

#淡水 vs 耕地 vs 食物生產指數 vs 農業GDP
#5*5
def excel5():

    # AnnualFreshwater
    annualFreshwater = pd.read_csv(inPath + "/AnnualFreshwater.csv")
    print('AnnualFreshwater info', annualFreshwater.info())
    annualFreshwater = annualFreshwater.drop(columns=['Indicator Name', 'Indicator Code'])
    annualFreshwater = pd.melt(annualFreshwater, id_vars=['Country Name', 'Country Code'], var_name='year',
                               value_name='annualFreshwater')
    annualFreshwater = annualFreshwater.dropna()
    print('AnnualFreshwater info-----------melt--------\n')
    annualFreshwater.info()
    print('AnnualFreshwater head(10)\n')
    print(annualFreshwater.head(10))

    # ArableLand
    arableLand = pd.read_csv(inPath + "/ArableLand.csv")
    print('ArableLand info', arableLand.info())
    arableLand = arableLand.drop(columns=['Indicator Name', 'Indicator Code'])
    arableLand = pd.melt(arableLand, id_vars=['Country Name', 'Country Code'], var_name='year',
                               value_name='arableLand')
    arableLand = arableLand.dropna()
    print('ArableLand info-----------melt--------\n')
    arableLand.info()
    print('ArableLand head(10)\n')
    print(arableLand.head(10))

    # FoodProductionIndex
    foodProductionIndex = pd.read_csv(inPath + "/FoodProductionIndex.csv")
    print('FoodProductionIndex info', foodProductionIndex.info())
    foodProductionIndex = foodProductionIndex.drop(columns=['Indicator Name', 'Indicator Code'])
    foodProductionIndex = pd.melt(foodProductionIndex, id_vars=['Country Name', 'Country Code'], var_name='year',
                         value_name='foodProductionIndex')
    foodProductionIndex = foodProductionIndex.dropna()
    print('FoodProductionIndex info-----------melt--------\n')
    foodProductionIndex.info()
    print('FoodProductionIndex head(10)\n')
    print(foodProductionIndex.head(10))

    # Agriculture_GDP
    agriculturalGDP = pd.read_csv(inPath + "/Agriculture_GDP.csv")
    print('Agriculture_GDP info', agriculturalGDP.info())
    agriculturalGDP = agriculturalGDP.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalGDP = pd.melt(agriculturalGDP, id_vars=['Country Name', 'Country Code'], var_name='year',
                              value_name='agriculturalLand')
    agriculturalGDP = agriculturalGDP.dropna()
    print('Agriculture_GDP info-----------melt--------\n')
    agriculturalGDP.info()
    print('Agriculture_GDP head(10)\n')
    print(agriculturalGDP.head(10))

    # GDP
    GDP = pd.read_csv(inPath + "/GDP.csv")
    print('GDP info', GDP.info())
    GDP = GDP.drop(columns=['Indicator Name', 'Indicator Code'])
    GDP = pd.melt(GDP, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='GDP')
    GDP = GDP.dropna()
    print('GDP info-----------melt--------\n')
    GDP.info()
    print('GDP head(10)\n')
    print(GDP.head(10))

    ex5 = pd.merge(annualFreshwater, arableLand, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex5 = pd.merge(ex5, foodProductionIndex, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex5 = pd.merge(ex5, agriculturalGDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex5 = pd.merge(ex5, GDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    print("ex5 info-->", ex5.info())
    print('ex5 head(10)\n')
    print(ex5.head(10))

    ex5.to_csv(inPath + "/ex5.csv")

#人口 vs gdp vs 農業gdp
def excel6():
    # Population
    population = pd.read_csv(inPath + "/Population.csv")
    print('Population info', population.info())
    population = population.drop(columns=['Indicator Name', 'Indicator Code'])
    population = pd.melt(population, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='population')
    population = population.dropna()
    print('Population info-----------melt--------\n')
    population.info()
    print('Population head(10)\n')
    print(population.head(10))

    print("-----------------------------------------------")

    # GDP
    GDP = pd.read_csv(inPath + "/GDP.csv")
    print('GDP info', GDP.info())
    GDP = GDP.drop(columns=['Indicator Name', 'Indicator Code'])
    GDP = pd.melt(GDP, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='GDP')
    GDP = GDP.dropna()
    print('GDP info-----------melt--------\n')
    GDP.info()
    print('GDP head(10)\n')
    print(GDP.head(10))

    print("-----------------------------------------------")

    # Agriculture_GDP
    agriculturalGDP = pd.read_csv(inPath + "/Agriculture_GDP.csv")
    print('Agriculture_GDP info', agriculturalGDP.info())
    agriculturalGDP = agriculturalGDP.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalGDP = pd.melt(agriculturalGDP, id_vars=['Country Name', 'Country Code'], var_name='year',
                              value_name='agriculturalGDP')
    agriculturalGDP = agriculturalGDP.dropna()
    print('Agriculture_GDP info-----------melt--------\n')
    agriculturalGDP.info()
    print('Agriculture_GDP head(10)\n')
    print(agriculturalGDP.head(10))

    ex6 = pd.merge(population, GDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex6 = pd.merge(ex6, agriculturalGDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    print("ex6 info-->", ex6.info())
    print('ex6 head(10)\n')
    print(ex6.head(10))

    ex6.to_csv(inPath + "/ex6.csv")

#Arable land (hectares per person) vs Land under cereal production (hectares)
def excel7():

    # ArableLand
    arableLand = pd.read_csv(inPath + "/ArableLand.csv")
    print('ArableLand info', arableLand.info())
    arableLand = arableLand.drop(columns=['Indicator Name', 'Indicator Code'])
    arableLand = pd.melt(arableLand, id_vars=['Country Name', 'Country Code'], var_name='year',
                         value_name='arableLand')
    arableLand = arableLand.dropna()
    print('ArableLand info-----------melt--------\n')
    arableLand.info()
    print('ArableLand head(10)\n')
    print(arableLand.head(10))

    print("-----------------------------------------------")

    # Land under cereal production
    landUnderCerealProduction = pd.read_csv(inPath + "/LandUnderCerealProduction.csv")
    print('LandUnderCerealProduction info', landUnderCerealProduction.info())
    landUnderCerealProduction = landUnderCerealProduction.drop(columns=['Indicator Name', 'Indicator Code'])
    landUnderCerealProduction = pd.melt(landUnderCerealProduction, id_vars=['Country Name', 'Country Code'], var_name='year',
                         value_name='landUnderCerealProduction')
    landUnderCerealProduction = landUnderCerealProduction.dropna()
    print('LandUnderCerealProduction info-----------melt--------\n')
    landUnderCerealProduction.info()
    print('LandUnderCerealProduction head(10)\n')
    print(landUnderCerealProduction.head(10))

    ex7 = pd.merge(arableLand, landUnderCerealProduction, on=['Country Name', 'Country Code', 'year'], how='inner')
    print("ex7 info-->", ex7.info())
    print('ex7 head(10)\n')
    print(ex7.head(10))

    ex7.to_csv(inPath + "/ex7.csv")

#Total natural resources rents (% of GDP) vs Gross savings (% of GDP) vs 農業進出口
# 自然資源是否會影響該國國家積蓄、是否以農業為主
def excel8():

    #Total natural resources rents
    totalNaturalResourcesRents = pd.read_csv(inPath + "/TotalNaturalResourcesRents.csv")
    print('TotalNaturalResourcesRents info', totalNaturalResourcesRents.info())
    totalNaturalResourcesRents = totalNaturalResourcesRents.drop(columns=['Indicator Name', 'Indicator Code'])
    totalNaturalResourcesRents = pd.melt(totalNaturalResourcesRents, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='totalNaturalResourcesRents')
    totalNaturalResourcesRents = totalNaturalResourcesRents.dropna()
    print('TotalNaturalResourcesRents info-----------melt--------\n')
    totalNaturalResourcesRents.info()
    print('TotalNaturalResourcesRents head(10)\n')
    print(totalNaturalResourcesRents.head(10))

    print("-----------------------------------------------")

    # Gross savings
    grossSavings = pd.read_csv(inPath + "/GrossSavings.csv")
    print('GrossSavings info', grossSavings.info())
    grossSavings = grossSavings.drop(columns=['Indicator Name', 'Indicator Code'])
    grossSavings = pd.melt(grossSavings, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='grossSavings')
    grossSavings = grossSavings.dropna()
    print('GrossSavings info-----------melt--------\n')
    grossSavings.info()
    print('GrossSavings head(10)\n')
    print(grossSavings.head(10))

    print("-----------------------------------------------")

    # imports
    im = pd.read_csv(inPath + "/imports.csv")
    print('import info', im.info())
    im = im.drop(columns=['Indicator Name', 'Indicator Code'])
    im = pd.melt(im, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='imports')
    im = im.dropna()
    print('import info-----------melt--------\n')
    im.info()
    print('import head(10)\n')
    print(im.head(10))

    print("-----------------------------------------------")

    # exports
    ex = pd.read_csv(inPath + "/exports.csv")
    print('export info', ex.info())
    ex = ex.drop(columns=['Indicator Name', 'Indicator Code'])
    ex = pd.melt(ex, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='exports')
    ex = ex.dropna()
    print('export info-----------melt--------\n')
    ex.info()
    print('export head(10)\n')
    print(ex.head(10))

    ex8 = pd.merge(totalNaturalResourcesRents, grossSavings, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex8 = pd.merge(ex8, im, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex8 = pd.merge(ex8, ex, on=['Country Name', 'Country Code', 'year'], how='inner')
    print("ex8 info-->", ex8.info())
    print('ex8 head(10)\n')
    print(ex8.head(10))

    ex8.to_csv(inPath + "/ex8.csv")

#Fertilizer consumption vs Crop production index
#化肥消耗量 vs 糧食生產指數
def excel9():

    #FertilizerConsumption
    fertilizerConsumption = pd.read_csv(inPath + "/FertilizerConsumption.csv")
    print('FertilizerConsumption info', fertilizerConsumption.info())
    fertilizerConsumption = fertilizerConsumption.drop(columns=['Indicator Name', 'Indicator Code'])
    fertilizerConsumption = pd.melt(fertilizerConsumption, id_vars=['Country Name', 'Country Code'],
                                         var_name='year', value_name='fertilizerConsumption')
    fertilizerConsumption = fertilizerConsumption.dropna()
    print('FertilizerConsumption info-----------melt--------\n')
    fertilizerConsumption.info()
    print('FertilizerConsumption head(10)\n')
    print(fertilizerConsumption.head(10))

    print("-----------------------------------------------")

    #CropProduction
    cropProduction = pd.read_csv(inPath + "/CropProduction.csv")
    print('CropProduction info', cropProduction.info())
    cropProduction = cropProduction.drop(columns=['Indicator Name', 'Indicator Code'])
    cropProduction = pd.melt(cropProduction, id_vars=['Country Name', 'Country Code'],
                                    var_name='year', value_name='cropProduction')
    cropProduction = cropProduction.dropna()
    print('CropProduction info-----------melt--------\n')
    cropProduction.info()
    print('CropProduction head(10)\n')
    print(cropProduction.head(10))

    # region
    region = pd.read_csv(inPath + "/all.csv")
    print('region info', region.info())
    region = region.drop(
        columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'intermediate-region', 'region-code',
                 'sub-region-code', 'intermediate-region-code'])
    print('region head(10)\n')
    print(region.head(10))

    ex9 = pd.merge(fertilizerConsumption, cropProduction, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex9 = pd.merge(ex9, region, right_on='name', left_on='Country Name', how='inner')
    print("ex9 info-->", ex9.info())
    print('ex9 head(10)\n')
    print(ex9.head(10))

    ex9.to_csv(inPath + "/ex9.csv")

#農業男女 vs 農業GDP
def excel10():

    # male
    male = pd.read_csv(inPath + "/male.csv")
    print('male info', male.info())
    male = male.drop(columns=['Indicator Name', 'Indicator Code'])
    male = pd.melt(male, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='male')
    male = male.dropna()
    print('male info-----------melt--------\n')
    male.info()
    print('male head(10)\n')
    print(male.head(10))

    print("-----------------------------------------------")

    # female
    female = pd.read_csv(inPath + "/female.csv")
    print('female info', female.info())
    female = female.drop(columns=['Indicator Name', 'Indicator Code'])
    female = pd.melt(female, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='female')
    female = female.dropna()
    print('female info-----------melt--------\n')
    female.info()
    print('female head(10)\n')
    print(female.head(10))

    print("-----------------------------------------------")

    # Agriculture_GDP
    agriculturalGDP = pd.read_csv(inPath + "/Agriculture_GDP.csv")
    print('Agriculture_GDP info', agriculturalGDP.info())
    agriculturalGDP = agriculturalGDP.drop(columns=['Indicator Name', 'Indicator Code'])
    agriculturalGDP = pd.melt(agriculturalGDP, id_vars=['Country Name', 'Country Code'], var_name='year',
                              value_name='agriculturalGDP')
    agriculturalGDP = agriculturalGDP.dropna()
    print('Agriculture_GDP info-----------melt--------\n')
    agriculturalGDP.info()
    print('Agriculture_GDP head(10)\n')
    print(agriculturalGDP.head(10))

    print("-----------------------------------------------")

    # region
    region = pd.read_csv(inPath + "/all.csv")
    print('region info', region.info())
    region = region.drop(
        columns=['alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'intermediate-region', 'region-code',
                 'sub-region-code', 'intermediate-region-code'])
    print('region head(10)\n')
    print(region.head(10))

    # GDP
    GDP = pd.read_csv(inPath + "/GDP.csv")
    print('GDP info', GDP.info())
    GDP = GDP.drop(columns=['Indicator Name', 'Indicator Code'])
    GDP = pd.melt(GDP, id_vars=['Country Name', 'Country Code'], var_name='year', value_name='GDP')
    GDP = GDP.dropna()
    print('GDP info-----------melt--------\n')
    GDP.info()
    print('GDP head(10)\n')
    print(GDP.head(10))


    ex10 = pd.merge(male, female, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex10 = pd.merge(ex10, agriculturalGDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex10 = pd.merge(ex10, GDP, on=['Country Name', 'Country Code', 'year'], how='inner')
    ex10 = pd.merge(ex10, region, right_on='name', left_on='Country Name', how='inner')
    print("ex10 info-->", ex10.info())
    print('ex10 head(10)\n')
    print(ex10.head(10))

    #農業人口總數
    ex10['totalpop'] = ex10['female']+ex10['male']
    ex10['aGDP'] = ex10['agriculturalGDP'] * ex10['GDP']
    print("ex10 info-->", ex10.info())
    ex10.info()

    ex10.to_csv(inPath + "/ex10.csv")

if __name__ == '__main__':
    # excel1()
    # excel2()
    # excel3()
    # excel4()
    # excel5()
    # excel6()
    # excel7()
    # excel8()
    # excel9()
    # excel10()
