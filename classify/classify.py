"""
author: 汪宝瑞
create time: 2020-03-09
update time: 2020-03-14
"""

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pkg_resources

import torch
from torch.utils.data import TensorDataset, DataLoader
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertConfig, BertForSequenceClassification


class InputFeatures(object):

    def __init__(self, input_ids, input_mask, segment_ids):

        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids


def convert_example_to_feature(text, tokenizer, max_seq_length=30):

    tokens_text = tokenizer.tokenize(text)
    if len(tokens_text) > max_seq_length - 2:
        tokens_text = tokens_text[0:(max_seq_length - 2)]

    tokens = []
    segment_ids = []
    tokens.append("[CLS]")
    segment_ids.append(0)
    for token in tokens_text:
        tokens.append(token)
        segment_ids.append(0)
    tokens.append("[SEP]")
    segment_ids.append(0)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    input_mask = [1] * len(input_ids)

    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)

    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    return InputFeatures(
        input_ids=input_ids,
        input_mask=input_mask,
        segment_ids=segment_ids
    )


class Classifier:

    def __init__(self):

        self.label_list = ["xuexi", "huodong", "xunwu", "chushou", "qiugou", "huzhu", "zhaopin"]
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese', do_lower_case=True)

        filepath = pkg_resources.resource_filename(__name__, "../.FILE/checkpoints/bert_classification.pth")
        state_dict = torch.load(filepath, map_location=torch.device('cpu'))
        self.model = BertForSequenceClassification(BertConfig(21128), 7)
        self.model.load_state_dict(state_dict['state_dict'])

    def get_label(self, target):
        """
        获取目标字符串所属类别
        """

        feature = convert_example_to_feature(target, self.tokenizer)
        all_input_ids = torch.tensor([feature.input_ids], dtype=torch.long)
        all_input_mask = torch.tensor([feature.input_mask], dtype=torch.long)
        all_segment_ids = torch.tensor([feature.segment_ids], dtype=torch.long)
        test_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        dataloader = DataLoader(test_data, batch_size=1)

        self.model.eval()
        pred = 0
        for input_ids, input_mask, segment_ids in dataloader:
            logits = self.model(input_ids, segment_ids, input_mask)
            pred = logits.max(1)[1]

        return self.label_list[pred]
