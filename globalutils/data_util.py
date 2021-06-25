#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Mr Fan
# @Time: 2021年06月22
import os
import re
import json


def list_find(list1, list2):
    """
    在序列list1中寻找子串list2,如果找到，返回第一个下标；
    如果找不到，返回-1
    :param list1: (list, str)
    :param list2: (list, str)
    :return: i(int)起始下标， -1 未找到
    """
    n_list2 = len(list2)
    for i in range(len(list1)):
        if list1[i: i + n_list2] == list2:
            return i
    return -1


def valid_file(file_path: str):
    """
    传入文件路径，判断文件是否存在，存在则返回1, 不存在则返回0
    :param file_path: (str)文件路径
    :return: 1 0
    """
    # 文件状态
    state = 1
    # 判断文件是否存在
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        state -= 1

    return state


def valid_dir(dir_path: str):
    """
    传入文件夹路径，判断文件夹是否存在，存在则返回1，不存在则返回0
    :param dir_path: (str)
    :return: 1,0
    """
    # 文件夹状态
    state = 1
    # 判断文件夹是否存在
    if not os.path.exists(dir_path) or os.path.isfile(dir_path):
        state -= 1

    return state


def read_json(file_path: str):
    """
    传入json文件路径，读取文件内容，返回json解析后的数据。
    :param file_path: (str)json文件路径
    :return: data 读取得到的文章内容
    :raise: ValueError 如果不是json文件则报错
    """
    # 判断文件是否为.json文件
    if not os.path.exists(file_path) or os.path.isdir(file_path) or not file_path.endswith(".json"):
        print(f"{file_path} 文件错误！")
        raise ValueError

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except TypeError:
        with open(file_path, "r", encoding="gbk") as file:
            content = file.read()

    data = json.loads(content)

    return data


def save_json(content, file_path: str):
    """
    传入需要保存的数据，将数据转换为json字符串保存到指定路径file_path
    :param content: 需要保存的数据
    :param file_path: (str)指定路径
    :return: None 无返回值
    :raise: ValueError 如果不是json文件则报错
    """
    # 判断是否保存为.json
    if not file_path.endswith(".json"):
        print(f"{file_path} 需保存为.json文件")
        raise ValueError

    # 将列表或者字典处理成json字符串
    content = json.dumps(content, ensure_ascii=False, indent=4)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def file_reader(file_path: str):
    """
    传入文件路径，读取文件内容，以字符串方式返回文件内容。
    :param file_path: (str)文件路径
    :return: (str) content 文件内容
    :raise:
    """
    try:
        with open(file_path, 'r', encoding="gbk") as file:
            content = file.read()
    except Exception as e:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

    return content


def file_saver(content: str, file_path: str):
    """
    传入字符串内容，将内容保存到指定路径中。
    :param content: (str)文件内容
    :param file_path: (str)指定文件路径
    :return: None
    """
    assert isinstance(content, str)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def data_process(content):
    """
    对传入的中文字符串进行清洗，去除邮箱、URL等无用信息。
    :param content: (str)待清洗的中文字符串
    :return: (str) content 清洗后的中文字符串
    """
    assert isinstance(content, str)

    def normalize_num_str(content: str):
        """
        传入字符串，对字符串中的数字字符串进行处理，解决 1,000 类字符串中逗号引起的模型抽取问题
        :param content: 文本字符串
        :return: content(str)数字字符串规范化以后的文本内容
        """
        # 正则模板
        p = re.compile(r'(\d[,，]{1}\d)')
        # 查找所有的模板匹配组
        m = p.findall(content)
        for once in m:
            content = content.replace(once, re.sub('[,，]', "", once))

        return content

    if content:
        # 将文章中字符串内容的数字进行规范化，去除数字中的逗号
        content = normalize_num_str(content)
        # 清洗url标签
        content = re.sub('<.*?>', '', content)
        content = re.sub('【.*?】', '', content)
        # 剔除邮箱
        content = re.sub('([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})', '', content)
        content = re.sub('[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+', '', content)
        # 剔除URL
        content = re.sub("(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?", '', content)
        # 剔除IP地址
        content = re.sub('((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)', '', content)
        content = re.sub('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                         '',
                         content)
        # 剔除网络字符，剔除空白符
        content = content.strip().strip('\r\n\t').replace(u'\u3000', '').replace(u'\xa0', '')
        content = content.replace('\t', '').replace(' ', '').replace('\n', '').replace('\r', '')

    return content


def get_sentences(content: str, maxlen=160):
    """
    传入一篇中文文章，获取文章中的每一个句子，返回句子列表。对中文、日文文本进行拆分。
    # todo 可以考虑说话部分的分句， 例如‘xxx：“xxx。”xx，xxxx。’
    :param content: (str) 一篇文章
    :return: sentences(list) 分句后的列表
    :raise: TypeError
    """

    def supplement(sentences: list):
        """
        传入句子列表，判断句子是否因正则切分导致过长，使用暴力切分方式进行分句
        :param sentences: 句子列表
        :return: results(list)
        """
        data = []
        for once in sentences:
            if len(once) > maxlen:
                data.extend([f"{i}。" for i in re.split('[。？！?!]', once) if i])
            else:
                data.append(once)

        return data

    if not isinstance(content, str):
        print("The content you want to be split is not string!")
        raise TypeError
    # 需要保证字符串内本身没有这个分隔符
    split_sign = '%%%%'
    # 替换的符号用: $PACK$
    sign = '$PACK$'
    # 替换后的检索模板
    search_pattern = re.compile('\$PACK\$')
    # 需要进行替换的模板
    pack_pattern = re.compile('(“.+?”|（.+?）|《.+?》|〈.+?〉|[.+?]|【.+?】|‘.+?’|「.+?」|『.+?』|".+?"|\'.+?\')')
    # 正则匹配文本中所有需要替换的模板
    pack_queue = re.findall(pack_pattern, content)
    # 将文本中所有需要替换的，都替换成sign替换符号
    content = re.sub(pack_pattern, sign, content)

    # 分句模板
    pattern = re.compile('(?<=[。？！])(?![。？！])')
    result = []
    while content != '':
        # 查询文章中是否可分句
        s = re.search(pattern, content)
        # 如果不可分，则content是一个完整的句子
        if s is None:
            result.append(content)
            break
        # 获取需要分句的位置
        loc = s.span()[0]
        # 将第一个句子添加到结果中
        result.append(content[:loc])
        # 将剩余的部分继续分句
        content = content[loc:]

    # 使用切分符将之前分割好的内容拼接起来
    result_string = split_sign.join(result)
    while pack_queue:
        pack = pack_queue.pop(0)
        loc = re.search(search_pattern, result_string).span()
        result_string = f"{result_string[:loc[0]]}{pack}{result_string[loc[1]:]}"

    # 使用切分符将文章内容切分成句子
    sentences = supplement(result_string.split(split_sign))

    return sentences


def supplement_nums(part: str, s: str):
    """
    传入子串和原始字符串，不全子串前后的数值
    :param part: 子串
    :param s: 原始字符串
    :return: part(str)补全后的子串
    """
    start = list_find(s, part)
    end = start + len(part)

    if s[start] != s[0]:
        if s[start - 1].isdigit():
            for i in s[start - 1::-1]:
                if not i.isdigit():
                    break
                part = f"{i}{part}"

    if s[end - 1] != s[-1]:
        if s[end].isdigit():
            for i in s[end:]:
                if not i.isdigit():
                    break
                part = f"{i}{part}"

    return part


def normalize_num_str(content: str):
    """
    传入字符串，对字符串中的数字字符串进行处理，解决 1,000 类字符串中逗号引起的模型抽取问题
    :param content: 文本字符串
    :return: content(str)数字字符串规范化以后的文本内容
    """
    # 正则模板
    p = re.compile(r'(\d[,，]{1}\d)')
    # 查找所有的模板匹配组
    m = p.findall(content)
    for once in m:
        content = content.replace(once, re.sub('[,，]', "", once))

    return content


def getFiles(raw_path: str, target=None) -> list:
    """
    传入文件夹路径，返回文件夹下所有指定类型文件的路径，包括子文件夹中的文件
    :param dir_path:文件夹路径
    :param target: 目标文件后缀.txt,.json,.csv
    :return:files（list）文件路径列表
    """
    files = []
    if valid_dir(raw_path):
        dirs = os.listdir(raw_path)
        dirs = [os.path.join(raw_path, dir_name) for dir_name in dirs]
        for dir_path in dirs:
            files.extend(getFiles(dir_path, target))
    else:
        if target is None:
            files.append(raw_path)
        elif raw_path.endswith(target):
            files.append(raw_path)

    return files