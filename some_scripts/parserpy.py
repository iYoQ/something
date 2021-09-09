'''Read *.rpy files, parse into string lines.

'''

import sys
import os
import re
import glob


class ParseRpy():
    '''main_dir its path to folder with *.rpy files.
    On default its current directory.

    '''
    def __init__(self, main_dir=sys.path[0]):
        self.__main_dir = main_dir

        if not os.path.exists(f'{self.__main_dir}/eng'):
            os.mkdir(f'{self.__main_dir}/eng')
        if not os.path.exists(f'{self.__main_dir}/finale_rpy'):
            os.mkdir(f'{self.__main_dir}/finale_rpy')

        self.__rpy_list = glob.glob(f'{self.__main_dir}/*.rpy')

    @property
    def main_dir(self):
        '''Path to *.rpy

        '''

        return self.__main_dir

    @main_dir.setter
    def main_dir(self, path):
        self.__main_dir = path

    @property
    def rpy_list(self):
        '''List of *.rpy

        '''

        return '\n'.join(i for i in self.__rpy_list)

    def update_rpy_list(self):
        '''Update list if change main_dir

        '''

        self.__rpy_list = glob.glob(f'{self.__main_dir}/*.rpy')

    def __str__(self):
        return f'path to *.rpy:\n {self.main_dir}\nlist of rpy:\n {self.rpy_list}'

    def parser_rpy_to_text(self) -> str:
        '''Parser text from *.rpy files into ../eng.

        '''

        if not self.__rpy_list:
            return 'empty found *.rpy files'

        for file in self.__rpy_list:
            file_name = os.path.basename(os.path.splitext(file)[0])
            path_out = f'{self.__main_dir}/eng/{file_name}.txt'

            with open(file, 'r', encoding='utf-8') as f_in:
                for line_no, line in enumerate(f_in, start=1):
                    if re.search('[а-яА-Я]|^ *(#|old|new)|"(\.{3}|[^a-zA-Z]+)"$', line):
                        continue

                    if not (tmp := re.findall('"(.+?)"$', line)):
                        continue

                    result = tmp[0].replace('\n', '')

                    with open(path_out, 'a') as f_out:
                        print(f'"{result}" :{line_no}', end='\n\n', file=f_out)

        return '\n--> complete <--'

    def create_translate_rpy(self) -> str:
        '''Create *rpy file with text from ../eng.

        '''

        if not self.__rpy_list:
            return 'empty found *.rpy files'

        for file in self.__rpy_list:
            file_name = os.path.basename(os.path.splitext(file)[0])
            path_out = f'{self.__main_dir}/finale_rpy/{file_name}.rpy'
            path_translate = f'{self.__main_dir}/eng/{file_name}.txt'

            with open(file, 'r', encoding='utf-8-sig') as f_old_rpy:
                for line_num, line in enumerate(f_old_rpy, start=1):
                    with open(path_out, 'a', encoding='utf-8') as f_new_rpy:
                        if re.search('^\n$|^\w+|[а-яА-Я]|^ *(#|old|new)|"(\.{3}|[^a-zA-Z]+)"$', line):
                            print(line, file=f_new_rpy, end='')
                            continue

                        with open(path_translate, 'r', encoding='utf-8') as f_trans:
                            for line_trans in f_trans:
                                line_tmp = line_trans.replace('\n', '')
                                line_tmp = re.sub('\.$', '', line_tmp)

                                if not (str_num := re.search('\d+$', line_tmp)):
                                    continue

                                if line_num == int(str_num.group()):
                                    result = re.sub(' *\.?: *\d+\.?$', '', line_trans)
                                    if re.search('\w"$', result):
                                        result = re.sub('"$', '."', result)

                                    if not (start_str := re.match(' {4}[\w ]+ ', line)):
                                        print(f'    {result}', file=f_new_rpy)
                                        continue

                                    print(f'{start_str.group()}{result}', file=f_new_rpy, end='')
                                    break

        return '\n--> complete <--'
