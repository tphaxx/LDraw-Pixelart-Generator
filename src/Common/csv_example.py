from abc import ABC


class CsvExample(ABC):

    @staticmethod
    def show_csv():
        text = "CSV file format example:\n" \
               "\n" \
               "id,name,rgb,is_trans\n" \
               "0,Black,05131D,f\n" \
               "1,Blue,0055BF,f\n" \
               "2,Green,237841,f\n" \
               "3,Dark Turquoise,008F9B,f\n" \
               "...\n" \
               "\n" \
               "Column \'is_trans\' will ignore and can remove.\n"
        return text

