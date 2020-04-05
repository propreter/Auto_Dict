import File_Process
import Auto_Dict
import Text_Aligner
import shutil
import os
import File_Save

aligner = 'A'
dictionary = 'D'


def create_cache(rel_path):
    global cache_dir
    cache_name = 'cache'

    # 生成缓存目录
    cache_dir = os.path.join(rel_path, cache_name)
    print('建立缓存文件夹，请稍等！')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir


def delete_cache():
    shutil.rmtree(cache_dir)


# 程序入口
def main():
    src_file = input("请指定文件：")
    # 获取源文件相对路径和文件名
    src_rel_path = os.path.split(src_file)[0]

    # 生成缓存文件夹
    cache_path = create_cache(src_rel_path)

    # 文本处理
    word_list = File_Process.file_process(src_file, cache_path)

    # 文本处理方式
    treatment = input("请选择处理方式：").upper()
    sheet_name = input("请输入所属领域：")
    excel_name = input("请输入词汇表名称：")
    if treatment == aligner:
        print('正在对齐文本，请稍等！')
        entry = Text_Aligner.text_aligner(word_list)
        # 保存文件
        print('\r\n正在保存文件，请稍等！')
        File_Save.save_text_2_excel(entry, src_rel_path, sheet_name,
                                    excel_name)
    elif treatment == dictionary:
        print('正在查找单词，请稍等！')
        entry = Auto_Dict.auto_dict(word_list)
        # 保存文件
        print('\r\n正在保存文件，请稍等！')
        File_Save.save_entry_2_excel(entry, src_rel_path, sheet_name,
                                     excel_name)
    else:
        print("您输入的内容有误，请重新输入！")

    # 清理缓存文件
    delete_cache()


if __name__ == "__main__":
    main()
