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
		return False
	elif old_v > new_v:
		return True
    if len(old_vs) < len(new_vs):
        return False
    else:
        return True
'''
���ؽ����������ļ�����
'''
def progressbar(url,fileName):
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
    
     