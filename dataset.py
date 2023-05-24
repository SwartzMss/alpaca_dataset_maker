import streamlit as st
from collections import deque
from datetime import datetime
import os
import time
import json

def save_answers_as_json(file_path):
    jsonData = []
    jsonDataTmpForinstruction = ''
    for index in range(0, len(st.session_state.chat_history), 2):
        question = st.session_state.chat_history[index]
        answer = st.session_state.chat_history[index + 1] if index + 1 < len(st.session_state.chat_history) else ''
        jsonDataTmpForinstruction += "[Round {}]\n问:{}\n答:".format(len(jsonData), question)
        item = {
            "instruction": jsonDataTmpForinstruction,
            "input": "",
            "output": answer
        }
        jsonData.append(item)
        jsonDataTmpForinstruction +=answer
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(jsonData, file, ensure_ascii=False, indent=2)


def generate_dataset():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{current_time}.json"
    # 生成文件路径
    file_path = os.path.join(os.getcwd(), file_name)

    # 保存为JSON文件
    save_answers_as_json(file_path)

    # 显示成功提示
    st.success(f"数据集已生成并保存为 {file_name}")

def main():
    st.title("多轮对话数据集生成器")

    # 获取 session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = deque(maxlen=20)  # 创建并存储聊天记录
    if 'new_message' not in st.session_state:
        st.session_state.new_message = ""  # 初始化新消息

    # 创建一个 Streamlit container，方便后续布局
    container = st.container()

    # 创建两行
    row1 = container.columns(1)
    row2 = container.columns(1)

    # 在第一行显示输入框
    with row1[0]:
        st.session_state.new_message = st.text_input("请输入你的消息", value=st.session_state.new_message)  # 使用固定的key
        send_button = row1[0].button("发送消息")  # 新增发送按钮
        save_button = row1[0].button("保存为Json")

    if save_button:
        #if len(st.session_state.chat_history) < 3:
        #    st.error(f"请至少使用三条数据")
        #    return
        generate_dataset()
        st.session_state.chat_history.clear()  # 清空聊天历史
    
    # 当用户输入新消息并按下 Enter 键时
    if send_button and st.session_state.new_message:
        st.session_state.chat_history.append(st.session_state.new_message)  # 添加新消息到聊天历史

    # 在第二行显示聊天历史
    with row2[0]:
        for index,message in enumerate(st.session_state.chat_history):  # 现在是按照插入顺序显示
            # 根据计数器决定消息类型
            message_type = "问" if index % 2 == 0 else "答"
            st.markdown(f"**{message_type}**: {message}")

if __name__ == "__main__":
    main()
