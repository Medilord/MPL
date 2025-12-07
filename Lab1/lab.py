
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

    

    return


generateFile("test")