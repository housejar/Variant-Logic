# -*-coding:utf-8 -*-
import os
import struct


class Wave(object):
    """此类用于产生具有周期性质的wave"""
    def __init__(self, cycle=10, end_round=10000):
        super(Wave, self).__init__()
        self.cycle = cycle
        self.end_round = end_round

    def square_wave_to_file(self, filename=''):
        i = 0
        out_file = open(filename, 'wb')
        while i < self.end_round:
            out_file.write('1'*self.cycle)
            out_file.write('0'*self.cycle)
            i += 1
        out_file.close()

    def square_wave_to_mem(self, cycle=10, end_round=1000):
        i = 0
        result_str = ''
        while i < end_round:
            result_str += '1'*cycle
            result_str += '0'*cycle
            i += 1
        return result_str


class Tools():
    """
    此类事用于对产生的01字符串进行相关的操作的
    """
    def get_file_size(self, absolute_filename=''):
        """
        获取文件大小
        """
        return os.path.getsize(absolute_filename)

    def xor_str(self, string1='', string2='', compare_len=0):
        """
        将两个01字符串进行异或，并输出到文件当中。
        """
        result_str = ''
        if compare_len == 0:
            return result_str
        index = 0
        while index < compare_len:
            if string1[index] == string2[index]:
                result_str += '0'
            else:
                result_str += '1'
            index += 1
        return result_str

    def xor_file(self, filename1='', filename2='', outputfile="d:\\result.dat"):
        try:
            file1_size = self.get_file_size(filename1)
            in_file1 = open(filename1)
            fiel2_size = self.get_file_size(filename2)
            in_file2 = open(filename2)
            buffer1 = in_file1.read(file1_size)
            buffer2 = in_file2.read(fiel2_size)
            outputfile = open(outputfile, 'wb')
            result = self.xor_str(
                buffer1,
                buffer2,
                min([file1_size, fiel2_size]))
            outputfile.write(result)
        except Exception, e:
            raise


def remove_temp_file(filename1='', filename2=''):
    """
    删除临时文件用的函数，如果模式不是文件模式的话，
    则此函数不会被调用
    """
    os.remove(filename1)
    os.remove(filename2)


def ones(binstr, N):
    """根据输入的二进制串计算1的个数"""
    count = 0
    if N == 1:
        return count
    for x in xrange(0, N):
        if binstr[x] == '1':
            count = count+1
    return count


def one_zeros(binstr, N):
    """
    计算01的个数，需要考虑循环的操作,N表示0-1向量的位长
    """
    count = 0
    if N == 1:
        return count
    for x in xrange(0, N):
        if(binstr[x] == '0' and binstr[(x+1) % N] == '1'):
            count = count + 1
    return count


def block_statstic(window_size=10, strbuffer='', buffer_size=0):
    if buffer_size < 2:
        return
    result = {}  # 存放统计结果的
    print buffer_size
    n_windows = buffer_size / window_size  # 向下取整的除法， python2 中的截断，python3中的真除法
    index = 0
    while index < buffer_size:
        # 开始判断操作
        print "now is ", strbuffer[index:index+window_size]
        binstr_ones = ones(strbuffer[index:index+window_size], window_size)
        binstr_one_zeros = one_zeros(
            strbuffer[index:index+window_size],
            window_size)
        if binstr_ones in result:
            p = result[binstr_ones]
            if binstr_one_zeros in p:
                # 如果有1-0的序列的话就进行自增
                p[binstr_one_zeros] += 1
            else:
                p[binstr_one_zeros] = 1
        else:
            result[binstr_ones] = {binstr_one_zeros: 1}
        print index
        index = index+window_size
    return result

def window_stastic(block_size=10):
    pass


def main():
    wave_craetor = Wave(cycle=10, end_round=10000)
    tools = Tools()
    sq_wave1 = wave_craetor.square_wave_to_mem(
        cycle=6,
        end_round=64)
    sq_wave2 = wave_craetor.square_wave_to_mem(
        cycle=8,
        end_round=64)
    binarystr = tools.xor_str(
        sq_wave1,
        sq_wave2,
        min(len(sq_wave1), len(sq_wave2)))
    result = block_statstic(
        window_size=6,
        strbuffer=binarystr,
        buffer_size=len(binarystr))
    print result

if __name__ == '__main__':
    main()