'''
@Author: 一蓑烟雨任平生
@Date: 2020-02-18 17:08:33
@LastEditTime: 2020-03-08 15:54:21
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /BTMpy/src/main.py
'''
# -*- coding: utf-8 -*-
import time
from Model import *
import sys
import indexDocs
import topicDisplay
import os
import logging


def usage():
    print("Training Usage: \
    btm est <K> <W> <alpha> <beta> <n_iter> <save_step> <docs_pt> <model_dir>\n\
    \tK  int, number of topics, like 20\n \
    \tW  int, size of vocabulary\n \
    \talpha   double, Pymmetric Dirichlet prior of P(z), like 1.0\n \
    \tbeta    double, Pymmetric Dirichlet prior of P(w|z), like 0.01\n \
    \tn_iter  int, number of iterations of Gibbs sampling\n \
    \tsave_step   int, steps to save the results\n \
    \tdocs_pt     string, path of training docs\n \
    \tmodel_dir   string, output directory")


def BTM(argvs):
    if (len(argvs) < 4):
        usage()
    else:
        if (argvs[0] == "est"):
            K = argvs[1]
            W = argvs[2]
            alpha = argvs[3]
            beta = argvs[4]
            n_iter = argvs[5]
            save_step = argvs[6]
            docs_pt = argvs[7]
            dir = argvs[8]
            print("===== Run BTM, K="+str(K)+", W="+str(W)+", alpha="+str(alpha)+", beta=" +
                  str(beta)+", n_iter="+str(n_iter)+", save_step="+str(save_step)+"=====")
            clock_start = time.time()
            model = Model(K, W, alpha, beta, n_iter, save_step)
            model.run(docs_pt, dir)
            clock_end = time.time()
            print("procedure time : "+str(clock_end-clock_start))
        else:
            usage()


if __name__ == "__main__":

    # 12 类为临界值
    os.chdir('D:/BaiduNetdiskDownload/BTM/BTM-master/BTM/src')
    logging.basicConfig(
        filename='data_job_titles_set_class.log', level=logging.INFO)

    # perplexity_list = []
    # for K in range(2, 3):
    mode = "est"
    K = 9
    W = None
    alpha = 0.5
    beta = 0.5
    # alpha = 0.5
    # beta = 0.5

    # n_iter = 10  # 十次迭代
    n_iter = 10  # 十次迭代
    save_step = 100

    dir = "../output/"
    print('os.getcwd()', os.getcwd())

    input_dir = "../sample-data/"
    model_dir = dir + "model/"  # 模型存放的文件夹
    voca_pt = dir + "voca.txt"  # 生成的词典
    dwid_pt = dir + "doc_wids.txt"  # 每篇文档由对应的序号单词组成
    doc_pt = input_dir + "job_titles_class.dat"  # 输入的文档
    # doc_pt = input_dir + "job_titles_class.dat"  # 输入的文档 set后的job_titles数据6w+
    # 输入的文档 set后的data_warehouse数据 1.4w+
    # doc_pt = input_dir + "test_warehouse_set.dat"

    print("=============== Index Docs =============")

    # W生成的词典
    W = indexDocs.run_indexDocs(
        ['indexDocs', doc_pt, dwid_pt, voca_pt])  # 返回的是词典

    print("W : "+str(W))

    argvs = []
    argvs.append(mode)
    argvs.append(K)
    argvs.append(W)
    argvs.append(alpha)
    argvs.append(beta)
    argvs.append(n_iter)
    argvs.append(save_step)
    argvs.append(dwid_pt)
    argvs.append(model_dir)
    argvs.append(voca_pt)

    print("=============== Topic Learning =============")

    logging.info("=============== Topic Learning =============")
    logging.info("===== Run BTM, K="+str(K)+", W="+str(W)+", alpha="+str(alpha)+", beta=" +
                 str(beta)+", n_iter="+str(n_iter)+", save_step="+str(save_step)+"=====")

    BTM(argvs)

    print("================ Topic Display =============")
    logging.info('================ Topic Display =============')

    log_str = topicDisplay.run_topicDicplay(
        ['topicDisplay', model_dir, K, voca_pt])

    logging.info(log_str)
    topicDisplay.perplexity(argvs)
    perplexity = topicDisplay.perplexity(argvs)
    logging.info('*******perplexity_{}:{}\n\n'.format(K, perplexity))
