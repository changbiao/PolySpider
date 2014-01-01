#!/usr/bin/env python
#coding:gbk
import urllib
from progressbar import *
def cmpVersion(oldVersion, newVersion):
    '''
    �Ƚϰ汾��
    ���oldVersion����newVersion���򷵻�True,��֮�򷵻�False
    1.1.0��1.2.0�Ƚϣ�����False
    1.1.1.1��1.1.1�Ƚϣ�����True
    1.1��1.1.1�Ƚϣ�����False
    '''
    old_vs = oldVersion.strip().split(".")
    new_vs = newVersion.strip().split(".")
    for i in range(len(old_vs)):
        if i >= len(new_vs): return True
	old_v = int(old_vs[i])
	new_v = int(new_vs[i])
	if new_v > old_v:
            print "��ǰ�汾��%s | ץȡ��Ӧ�ð汾��%s : ִ�и��²���" %(oldVersion, newVersion)
            return False
	elif old_v > new_v:
            print "��ǰ�汾��%s | ץȡ��Ӧ�ð汾��%s : ��ִ�и��²���" %(oldVersion, newVersion)
            return True
    if len(old_vs) < len(new_vs):
        print "��ǰ�汾��%s | ץȡ��Ӧ�ð汾��%s : ִ�и��²���" %(oldVersion, newVersion)
        return False
    else:
        print "��ǰ�汾��%s | ץȡ��Ӧ�ð汾��%s : ��ִ�и��²���" %(oldVersion, newVersion)
        return True

def normalizeVersion(versionInput):
    '''
    ��ץȡ���İ汾�Ž��и�ʽ������
    ��֤�汾�ŵĸ�ʽΪXXX.XXX.XXX
    ����XΪ����
    ע1�������з����ֹ��˵�
    ע2�����ڴ�����ĸ�İ汾��ͬ��������Ŀǰ��֪���Ƿ����ⷽ��汾�ż�¼������
    '''
    if not versionInput: return ""
    for digit in versionInput:
        if digit in "1234567890.":
            result += digit
    return result

def progressbar(url,fileName):
    '''
    ���ؽ����������ļ�����
    '''
    file=urllib.urlopen(url)
    totalSize=file.info().getheader("content-length")
    count=1000
    blockSize=int(totalSize)/int(count)
    widgets = [' <<<', Bar(), '>>> ',Percentage(),' ', ETA() ,' ' ,  FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets)

    def dlProgress(count, blockSize, totalSize):
        if pbar.maxval is None:
            pbar.maxval = totalSize
            pbar.start()
        pbar.update(min(count*blockSize, totalSize))
    urllib.urlretrieve(url, fileName, reporthook=dlProgress)
    pbar.finish()
    
     