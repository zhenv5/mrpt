# -*- coding: utf-8 -*-
#
# Author: Teemu Henrikki Pitkänen <teemu.pitkanen@helsinki.fi>
# University of Helsinki / Helsinki Institute for Information Technology 2016
#

import mrptlib


class MRPTIndex(object):
    """
    Wraps the extension module written in C++ and ensures that the arguments are given as lists, not ndarrays.
    """
    def __init__(self, X, n0, n_trees):
        """
        Builds the MRPT index for the input data
        :param X: Input data as a NxDim matrix
        :param n0: The maximum leaf-size of any rp-tree in the index
        :param n_trees: The number of trees used in the index
        :return:
        """
        self.index = mrptlib.MrptIndex(X.tolist(), n0, n_trees)

    def ann(self, q, k, n_extra_branches=0, votes_required=0):
        """
        The MRPT approximate nearest neighbor query.
        :param q: The query object, ie. the vector whose nearest neighbors are searched for
        :param k: The number of neighbors the user wants the query to return
        :param n_extra_branches: The number of extra branches to be explored by the priority queue trick
        :param votes_required: The number of votes an object has to get to be included in the linear search part of the query.
        :return: The indices of the approximate nearest neighbors in the original input data given to the constructor.
        """
        if votes_required == 0 and n_extra_branches == 0:
            return self.index.old_ann(q.tolist(), k)  # <--- Avoids some overhead in case voting is not employed
        return self.index.ann(q.tolist(), k, votes_required, n_extra_branches)
