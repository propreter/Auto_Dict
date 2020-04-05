from File_Process import char_discriminator

# 判断文本字符
regexp_char = r'[A-Za-z]+'


def text_aligner(text_list):
    # 对齐文本
    chn_cnt = 1
    eng_cnt = 1
    chn_text = []
    eng_text = []
    info_dict = {}

    for text in text_list:
        if char_discriminator(text):
            chn_text.append(text)
            chn_cnt += 1
        else:
            eng_text.append(text)
            eng_cnt += 1

    # if chn_cnt == eng_cnt:
    #     print("中英文文本已对齐")
    #     for i in range(chn_cnt):
    #         info_dict[chn_text[i]] = eng_text[i]
    # elif chn_cnt < eng_cnt:
    #     for j in range(chn_cnt):
    #         info_dict[chn_text[j]] = eng_text[j]
    #     for m in range(eng_cnt - chn_cnt):
    #         info_dict[m] = eng_text[chn_cnt + m]
    # elif chn_cnt > eng_cnt:
    #     for k in range(eng_cnt):
    #         info_dict[chn_text[k]] = eng_text[k]
    #     for n in range(chn_cnt - eng_cnt):
    #         info_dict[chn_text[eng_cnt + n]] = n
    if chn_cnt <= eng_cnt:
        for i in range(eng_cnt - chn_cnt):
            chn_text.append(' ')
    elif chn_cnt > eng_cnt:
        for i in range(chn_cnt - eng_cnt):
            eng_text.append(' ')
    for j in range(len(chn_text)):
        info_dict[chn_text[j]] = eng_text[j]

    return info_dict
