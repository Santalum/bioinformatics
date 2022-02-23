#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 22:32:52 2021

@author: stefan
"""

from Bio import pairwise2
from Bio import SeqIO
sequences=list(SeqIO.parse("sequences.fasta", "fasta"))

#alignments
alignment0=pairwise2.align.globalxx(sequences[0].seq,sequences[1].seq)
alignment1=pairwise2.align.globalxx(sequences[0].seq,sequences[2].seq)
alignment2=pairwise2.align.globalxx(sequences[0].seq,sequences[3].seq)
alignment3=pairwise2.align.globalxx(sequences[0].seq,sequences[4].seq)
alignment4=pairwise2.align.globalxx(sequences[0].seq,sequences[5].seq)

print (alignment0[0])
print (alignment1[0])
print (alignment2[0])
print (alignment3[0])
print (alignment4[0])