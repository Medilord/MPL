
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
    dataframe = pandas.read_csv(FileName)
    for index, row in dataframe.iterrows:
        data[row['Letter']].append(row['Value'])
    Medians = {
        'A':[],
        'B':[],
        'C':[],
        'D':[]
    }
    Deviation = {
        'A':[],
        'B':[],
        'C':[],
        'D':[]
    }
    
    for Let in ['A', 'B', 'C', 'D']:
        length = len(data[Let])
        list = data[Let]
        list.sort()
        if(length > 1):
            if((length % 2) == 0):
                median = list[(length // 2)]
            else:
                median = list[(length // 2) + 1]
        elif (length == 1):
            median = list[0]
        else:
            median = -1
        
        Medians[Let] = median
        for num in data[Let]:
            


    print(f"Файл {FileName}: \nA: {Medians['A']}, {Deviation['A']} \n\
    B: {Medians['B']}, {Deviation['B']} \n\
    C: {Medians['C']}, {Deviation['C']} \n\
    D: {Medians['D']}, {Deviation['D']}\n")


            

    return


generateFile("test")