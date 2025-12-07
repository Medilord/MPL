
# Необходимо на python написать код генерации 5 csv файлов вида:

# Категория, значение. Где категория это рандомная буква от A до D, а значение рандомное число с плавающей точкой (float к примеру)

# Далее нужно параллельно обработать эти 5 файлов. Обработка заключается в поиске медианы и стандартного отклонения в рамках каждой буквы. Т.е. на выходе вы получите результат в виде:

# А, медиана, отклонение
# Б, медиана, отклонение
# ...
# Д, медиана, отклонение

# После этого нужно из результатов также найти медиану из медиан и стандартное отклонение из медиан. Получив такой же результат

# А, медиана медиан, стандартное отклонение медиан
# ...
# Д, то же самое



from concurrent.futures import ProcessPoolExecutor
import random
import pandas


def generateFile(FileName: str):
    lineCount = random.randint(100,1000)
    data = {
        'Letter': [],
        'Value': []
    }
    
    
    for i in range(1, lineCount):
        data['Letter'].append(chr(random.randint(65, 68)))
        data['Value'].append(random.uniform(0.0, 100.0))

    dataFrame = pandas.DataFrame(data)
    dataFrame.to_csv(FileName, index=False)
    return


def processCSV(FileName: str):
    data = {
        'A':[],
        'B':[],
        'C':[],
        'D':[]
    }
    result = {
        'Letter':[],
        'Median':[],
        'Dispersion':[]
    }
    dataframe = pandas.read_csv(FileName)
    for index, row in dataframe.iterrows():
        data[row['Letter']].append(row['Value'])

    
    for Let in data.keys():
        length = len(data[Let])
        list = data[Let]
        list.sort()
        if(length > 1):
            if((length % 2) == 0):
                median = (list[(length // 2) - 1] + list[length // 2]) / 2
            else:
                median = list[length // 2]
        elif (length == 1):
            median = list[0]
        else:
            median = -1
        
        Mean = sum(list)/length
        SumDispersionSquares = 0

        for num in list:
            SumDispersionSquares += (num - Mean) ** 2
        dispersion = (SumDispersionSquares/length) ** 0.5

        if (median != -1):
            result['Letter'].append(Let)
            result['Median'].append(median)
            result['Dispersion'].append(dispersion)
            
    return result

def processMedians(results: list[dict]):
    Medians = {
        'A':[],
        'B':[],
        'C':[],
        'D':[]
    }
    result = {
        'Letter':[],
        'ResMedian':[],
        'ResDispersion':[]
    }

    for res in results:
        for let, median in zip(res['Letter'], res['Median']):
            Medians[let].append(median)
    
    for Let in Medians.keys():
        length = len(Medians[Let])
        list = Medians[Let]
        list.sort()
        if(length > 1):
            if((length % 2) == 0):
                median = (list[(length // 2) - 1] + list[length // 2]) / 2
            else:
                median = list[length // 2]
        elif (length == 1):
            median = list[0]
        else:
            median = -1

        Mean = sum(list)/length
        SumDispersionSquares = 0

        for num in list:
            SumDispersionSquares += (num - Mean) ** 2
        dispersion = (SumDispersionSquares/length) ** 0.5

        if (median != -1):
            result['Letter'].append(Let)
            result['ResMedian'].append(median)
            result['ResDispersion'].append(dispersion)

    return result


if __name__ == "__main__":

    FileNames = []
    for i in range(1, 6):
        name = "file_" + str(i) + ".csv"
        FileNames.append(name)
        generateFile(name)

    with ProcessPoolExecutor() as PPE:
        results = list(PPE.map(processCSV, FileNames))

    print("____Результаты обработки____")

    for i, result in enumerate(results, 0):
        print(("\nФайл: " + FileNames[i]))
        dataframe = pandas.DataFrame(result)
        print(dataframe.to_string(index=False))

        

    finalResult = processMedians(results)


    print("____Финальные результаты____")
    dataframe = pandas.DataFrame(finalResult)
    print(dataframe.to_string(index=False))
