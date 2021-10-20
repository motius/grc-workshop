#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np


filepath= "/home/funki/Desktop/GRC_workshop/03/base_rec.binary"

f = np.fromfile(open(filepath), dtype=np.float32)


print (f)

