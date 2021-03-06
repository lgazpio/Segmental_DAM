import os
import sys
import argparse
import numpy as np

from utils import *

def main(arguments):
    '''
    Read SICK official dataset and produce txt files for sent1, sent2 and entailment label
    '''
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_folder', help="location of folder with the sick files")
    parser.add_argument('--out_folder', help="location of the output folder")
    
    args = parser.parse_args(arguments)

    for split in ["train", "dev", "test"]:        
        src_out = open(os.path.join(args.out_folder, "src-"+split+".txt"), "w")
        targ_out = open(os.path.join(args.out_folder, "targ-"+split+".txt"), "w")
        label_out = open(os.path.join(args.out_folder, "label-"+split+".txt"), "w")
        label_set = set(["neutral", "entailment", "contradiction"])

        for line in open(os.path.join(args.data_folder, "SICK_"+split+".txt"),"r"):
            d = line.split("\t")
            label = d[3].strip().lower()
            premise = d[1].strip().lower()
            hypothesis = d[2].strip().lower()
            if label in label_set:
                for punct in punctuations:
                    if punct in premise:
                        premise = premise.replace(punct,"")
                premise = [w for w in premise.split() if w not in stopwords]
                premise = " ".join(lemmatize(" ".join(premise)))

                for punct in punctuations:
                    if punct in hypothesis:
                        hypothesis = hypothesis.replace(punct,"")
                hypothesis = [w for w in hypothesis.split() if w not in stopwords]
                hypothesis = " ".join(lemmatize(" ".join(hypothesis)))
                
                src_out.write(premise + "\n")
                targ_out.write(hypothesis + "\n")
                label_out.write(label + "\n")

        src_out.close()
        targ_out.close()
        label_out.close()
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
