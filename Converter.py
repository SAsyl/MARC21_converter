import csv
from typing import Tuple

US = ''  # hex(31), 1F hex
RS = ''  # hex(30), 1E hex
GS = ''  # hex(29), 1D hex
# print(len(US), len(RS), len(GS))


def length_calculation(element: dict, tags: dict) -> tuple[int, int]:
    field_length = 0
    code_length = 2

    for key_of_element in element.keys():
        if element[key_of_element] == '':
            element[key_of_element] = ' '

    additional_length = 4  # '  '{US}a
    accumulated_sum = 0
    size_of_tag = 0
    for key_of_element in tags.keys():
        size_of_element = len(element[key_of_element])
        # print(f"'{element[key_of_element]}'", size_of_element)

        if len(tags[key_of_element]) != 3:
            size_of_tag += size_of_element
            size_of_tag += additional_length
            size_of_tag += accumulated_sum

            element[key_of_element] = [element[key_of_element], size_of_tag]

            field_length += size_of_tag
            code_length += 1

            size_of_tag = 0
            accumulated_sum = 0
        else:
            accumulated_sum += size_of_element
            accumulated_sum += 2

    code_length *= 12
    field_length += code_length

    return field_length, code_length

'''
with open("./MegaPro/BooksDB/LittlePart.csv", "r", encoding='utf-16') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')

    with open("./MegaPro/BooksDB/new.csv", "w", encoding='utf-16', newline='') as newFile:
        header = "Authors|Header|PublicationPlace|PublishingOffice|Year|Content|Language|ISBN" \
                 "|Tags|LBC|PartNumber|Copy|InventoryNumbers".split('|')
        writer = csv.DictWriter(newFile, fieldnames=header, delimiter='|')

        writer.writeheader()

        for row in reader:
            del row['NM'], row['Status'], row['Rubric'], row['HAC'], row['Output'], row['Abstract']
            del row['PublicationNote'], row['PublicationType'], row['Bibliography']
            del row['Subheader'], row['UDC'], row['PartName'], row['SourceTitle'], row['ElectronicResource']

            writer.writerow(row)
'''
with open("./MegaPro/BooksDB/testother.csv", "r", encoding='utf-16') as first_element:
    reader = csv.DictReader(first_element, delimiter='|')

    element = next(reader)

    tagsDict = {'ISBN': [20, 'a'], 'Language': [41, 'a'], 'LBC': [84, 'a'], 'Authors': [100, 'a'],
                'Header': [245, 'a', 1], 'PartNumber': [245, 'b'], 'PublicationPlace': [260, 'a', 1],
                'PublishingOffice': [260, 'b', 2], 'Year': [260, 'c'], 'Content': [300, 'a'],
                'Tags': [650, 'a'], 'Copy': [852, 'a', 1], 'InventoryNumbers': [852, 'b']
                # 'Subheader': [500, 'a'], 'UDC': [80, 'a'], 'PartName': [300, 'b'], 'SourceTitle': [300, 'c'], 'ElectronicResource': [653, 'a'],
                }
    """ Not included Subheader, Rubric, UDC, HAC, PartName, SourceTitle, Output, ElectronicResource,
                   Abstract, PublicationNote, PublicationType, Bibliography columns
    """
    # print(len(tagsDict))

    total_field_length, total_code_length = length_calculation(element, tagsDict)
    print(element)

    NoteMarc = f"{total_field_length:05}nam  22{total_code_length:05}   450 "
    # print(NoteMarc)

    starting_position = 0
    for key in tagsDict.keys():
        if isinstance(element[key], list) and len(element[key]) == 2:
            size = element[key][1]
            NoteMarc += f"{tagsDict[key][0]:03}{size:04}{starting_position:05}"
            starting_position += size
    NoteMarc += f"{RS}  "

    # print(NoteMarc)

    for key in tagsDict.keys():
        if len(tagsDict[key]) == 2:
            NoteMarc += f"{US}{tagsDict[key][1]}{element[key][0]}{RS}  "
        else:
            NoteMarc += f"{US}{tagsDict[key][1]}{element[key][0]}"

    NoteMarc = NoteMarc[:-2] + GS

    print(NoteMarc)

    with open("./MegaPro/BooksDB/results.mrc", "w", encoding='utf-16') as resFile:
        resFile.write(NoteMarc)
