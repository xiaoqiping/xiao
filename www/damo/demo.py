#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
path = r'D:\config.json'

file=open(r'D:\new_config.json','a', encoding='utf_8')

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        value = line[:-1]  # 去掉换行符

        value = value.replace(" ", "")
        print(value)
        file.write(value)

file.close()





