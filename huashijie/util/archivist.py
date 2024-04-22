import os


def new_archivist():
    print("zh: 第一次运行，请输入可以唯一标识您节点的字符串。（合法字符：字母、数字、-、_）")
    print("en: First run, please input a string that can uniquely identify your node. (Legal characters: letters, numbers, -, _)")
    with open("ARCHIVIST.conf", "w") as f:
        f.write(input("ARCHIVIST: "))
    return get_archivist()

def get_archivist():
    if arch := os.getenv("ARCHIVIST", ""):
        return arch
    if os.path.exists("ARCHIVIST.conf"):
        with open("ARCHIVIST.conf", "r") as f:
            return f.read().splitlines()[0].strip()
    return ""