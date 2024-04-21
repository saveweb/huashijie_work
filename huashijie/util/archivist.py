import os


def new_archivist():
    print("zh: 未避免您的节点被 ban，请不要在同一个 IP 下多开！")
    print("en: To avoid being banned, please do not run concurrently on the same IP!")
    print("zh: 第一次运行，请输入可以唯一标识您节点的字符串。（合法字符：字母、数字、-、_）")
    print("en: First run, please input a string that can uniquely identify your node. (Legal characters: letters, numbers, -, _)")
    with open("ARCHIVIST.conf", "w") as f:
        f.write(input("ARCHIVIST: "))
    return get_archivist()

def get_archivist():
    if not os.path.exists("ARCHIVIST.conf"):
        return ""
    print("zh: 未避免您的节点被 ban，请不要在同一个 IP 下多开！")
    print("en: To avoid being banned, please do not run concurrently on the same IP!")
    with open("ARCHIVIST.conf", "r") as f:
        return f.read().splitlines()[0].strip()