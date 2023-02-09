# encoding:utf-8
"""
web channel
"""

import sqlite3
import time

from channel.channel import Channel
from common.log import logger
from flask import render_template


class WebChannel(Channel):
    def __init__(self):
        self.html = 'chat.html'
        self.db = 'web_history.db'
        self.table = "web_historys"
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(f"""
          CREATE TABLE IF NOT EXISTS {self.table}
          (_id integer primary key autoincrement,
            time_now TEXT, 
            query TEXT,
            reply_text TEXT,
            ip TEXT)
            """)
        cursor.close()

    def startup(self):
        pass

    #     server.run(debug=True, host='0.0.0.0', port=80)

    def handle(self, request):
        logger.info(request)
        try:
            question = request.get_json().get("question")
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return self.failure_reply(e)
        reply_text = self.process_question(question)
        return self.success_reply(reply_text)

    def process_question(self, question):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        reply_text = ''
        try:
            reply_text = self.build_reply_content(question, "openAI", None)
        except Exception as e:
            reply_text = str(e)
            return str(e)
        finally:
            try:
                cursor.execute(f"INSERT INTO {self.table} VALUES (null, ?, ?, ?)",
                               (time_now, question, reply_text))
                conn.commit()
            except Exception as e:
                return str(reply_text) + f" \n----\n 此条信息存入数据库失败\n ----\n 原因：{e}"
            finally:
                conn.close()
        return reply_text

    def reply(self, msg, receiver):
        """
        用于主动发送回复消息，适用场景 wx
        """
        pass

    def verify(self, request):
        return {
            "status": 200,
            "message": None,
            "reply": 'web 不需要校验请求用户身份'
        }

    def handle_html(self, request):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        try:
            # query = request.get_json().get("question")
            if len(request.form['question']) < 1:
                return render_template(self.html,
                                       question="null", res="问题不能为空")
            query = request.form['question']
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return self.failure_reply(e)
        reply_text = self.process_question(query)
        web_history = self._get_history()
        return render_template(self.html, question=query, res=str(reply_text), web_history=web_history)

    def reply_template(self, request):
        return render_template(self.html, question=0)

    def _get_history(self, ip=None):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table} ORDER BY _id DESC")
        data = cursor.fetchall()
        logger.info(f'历史记录：{data}')
        return data

    def show_history(self, request):
        data = self._get_history()
        return self.success_reply(data)

    def failure_reply(self, reply_text, code=400):
        return {
            "code": code,
            "message": "failed",
            "reply": reply_text
        }

    def success_reply(self, reply_text):
        return {
            "code": 200,
            "message": "success",
            "reply": reply_text
        }
