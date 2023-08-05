#encoding=utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(title='title', body='body', input_email_list=None, path_attach=None):
    # 发件人和收件人信息
    sender_email = 'caochl123@163.com'
    receiver_email = ['yjfdl123@163.com', '944815227@qq.com']

    if input_email_list:
        receiver_email = input_email_list
    print("receive:", receiver_email)
    
    # 创建带附件的邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg["To"] = ", ".join(receiver_email)
    msg['Subject'] = title

    # 添加邮件正文

    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    if path_attach:
        attachment_path = path_attach
        print("attach:", path_attach)
        with open(attachment_path, 'r', encoding='utf-8') as attachment:
            attachment_data = attachment.read()
            attachment_mime = MIMEText(attachment_data, 'plain')
            attachment_mime.add_header('Content-Disposition', f'attachment; filename=1.txt')  # 替换为你的附件文件名
            msg.attach(attachment_mime)

    # 添加附件

    # 发送邮件
    smtp_server = 'smtp.163.com'  # 替换为你的 SMTP 服务器地址
    smtp_port = 25  # 替换为你的 SMTP 服务器端口号
    
    username = 'caochl123@163.com'  # 替换为你的 SMTP 服务器用户名
    password = 'RXTBUZRJWFCVCYYD'  # 替换为你的 SMTP 服务器密码
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', str(e))


if __name__=="__main__":
    # send_email('title', 'body', 'articles.py')
    #send_email('title', 'body', '特斯拉涨价打破了定价逻辑？#特斯拉 #商业新说 #新能源汽车 #简佳人儿.txt')
    send_email('t1', 't2')
