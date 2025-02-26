import sqlite3
import telebot
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types


VIPCODE3 = '7511001126:AAH1xo5NEdmoEC1mEA4eQx7Mcj9TEHqGVpk'
ch = 'TranQuan'
ID = '6940071938'
ADMIN = [6940071938, 0]


zo = telebot.TeleBot(VIPCODE3)
owner = zo.get_chat(ID)
us = owner.username
conn = sqlite3.connect('channels.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, channel_name TEXT, invite_link TEXT)''')

conn.commit()


@zo.callback_query_handler(func=lambda call: call.data == 'Back')
def show_settings(call):
    markup = types.InlineKeyboardMarkup(row_width=2)

    user = zo.get_chat(call.from_user.id)
    owner_name = user.first_name
    owner_link = f"[{owner_name}](tg://user?id={call.from_user.id})"

    k_add = types.InlineKeyboardButton('➕ Thêm kênh', callback_data='add_channel')
    k_remove = types.InlineKeyboardButton('➖ Xóa kênh', callback_data='remove_channel')
    k_show = types.InlineKeyboardButton('🗂 Danh sách kênh', callback_data='show_channels')
    k_delete_all = types.InlineKeyboardButton('🗑️ Xóa tất cả kênh', callback_data='delete_all_channels')
    markup.add(k_show)
    markup.add(k_add, k_remove)
    markup.add(k_delete_all)

    zo.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'👤 *Bảng điều khiển Admin*:\n\n👑 Xin chào {owner_link} trong bảng điều khiển của bạn:',
        reply_markup=markup,
        parse_mode='Markdown'
    )
    zo.clear_step_handler(call.message)


def subscs(user_id):
    channels = cursor.execute("SELECT channel_name, invite_link FROM channels").fetchall()
    for channel in channels:
        channel_username, invite_link = channel
        try:
            member_status = zo.get_chat_member(chat_id=channel_username, user_id=user_id).status
            if member_status not in ["member", "administrator", "creator"]:
                return False, invite_link
        except Exception as e:
            continue
    return True, None


def not_subscrip(message, invite_link):
    na = message.from_user.first_name
    if invite_link:
        channel_url = invite_link.replace('@', '')
        button = telebot.types.InlineKeyboardMarkup(row_width=1)
        subscribe_button = telebot.types.InlineKeyboardButton(text="Tham gia", url=f"{channel_url}")
        button.add(subscribe_button)
        zo.reply_to(
            message,
            text=f'''
❕ | Xin lỗi, bạn {na}
❗️ | Bạn cần tham gia kênh của nhà phát triển trước
❕ | Tham gia rồi gửi /infotiktok lại nhé
==========================
🔗 - {invite_link}
==========================
''',
            disable_web_page_preview=True,
            reply_markup=button
        )
def not_subscrip1(call, invite_link):
    na = call.from_user.first_name
    if invite_link:
        channel_url = invite_link.replace('@', '')
        button = telebot.types.InlineKeyboardMarkup(row_width=1)
        subscribe_button = telebot.types.InlineKeyboardButton(text="Tham gia", url=f"{channel_url}")
        button.add(subscribe_button)
        zo.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''
❕ | Xin lỗi, bạn {na}
❗️ | Bạn cần tham gia kênh của nhà phát triển trước
❕ | Tham gia rồi gửi /infotiktok lại nhé
==========================
🔗 - {invite_link}
==========================
''',
            disable_web_page_preview=True,
            reply_markup=button
        )
        zo.clear_step_handler(call.message)


@zo.message_handler(commands=['infotiktok'])
def vip1 (ms):
    is_subscribed, channel = subscs(ms.from_user.id)

    if not is_subscribed:
        not_subscrip(ms, channel)
        return
    name = f"[{ms.from_user.first_name}](tg://{ms.from_user.id})"
    text = f'''
🤖 ¦ Xin chào {name}, tôi là bot dò tìm thông tin.
⚡️ ¦ Tôi có thể lấy thông tin tài khoản
🎭 ¦ từ tất cả các mạng xã hội.
    '''
    zeco = InlineKeyboardMarkup()
    tek = InlineKeyboardButton("• TikTok •", callback_data='TEK')
    z1 = InlineKeyboardButton("• Kênh nhà phát triển •", url=f"https://t.me/{ch}")
    z2 = InlineKeyboardButton("• Nhà phát triển •", url=f"https://t.me/{us}")
    zeco.add(tek)
    zeco.add(z1, z2)
    zo.reply_to(ms, text,
    reply_markup=zeco,
    parse_mode='Markdown'
    )


@zo.callback_query_handler(func=lambda call: call.data == 'Bak')
def vip11(call):
    is_subscribed, channel = subscs(call.from_user.id)
    if not is_subscribed:
        not_subscrip1(call, channel)
        return
    name = f"[{call.from_user.first_name}](tg://{call.from_user.id})"
    text = f'''
🤖 ¦ Xin chào {name}, tôi là bot dò tìm thông tin.
⚡️ ¦ Tôi có thể lấy thông tin tài khoản
🎭 ¦ từ tất cả các mạng xã hội.
    '''
    zeco = telebot.types.InlineKeyboardMarkup()
    tek = telebot.types.InlineKeyboardButton("• TikTok •", callback_data='TEK')
    z1 = telebot.types.InlineKeyboardButton("• Kênh nhà phát triển •", url=f"https://t.me/{ch}")
    z2 = telebot.types.InlineKeyboardButton("• Nhà phát triển •", url=f"https://t.me/{us}")
    zeco.add(tek)
    zeco.add(z1, z2)
    zo.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=zeco,
        parse_mode='Markdown'
    )
    zo.clear_step_handler(call.message)


@zo.callback_query_handler(func=lambda call: call.data == 'TEK')
def vip2(call):
    is_subscribed, channel = subscs(call.from_user.id)

    if not is_subscribed:
        not_subscrip1(call, channel)
        return
    text = '''
    🤖 ¦ Vui lòng nhập username TikTok của bạn
💢 ¦ để lấy thông tin tài khoản:
    '''
    zeco = InlineKeyboardMarkup()
    back = InlineKeyboardButton("• Trở lại •", callback_data='Bak')
    zeco.add(back)
    zo.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=zeco
    )
    zo.register_next_step_handler(call.message, tik)


def tik(ms):
    username = ms.text.strip()
    api = f"https://tik-batbyte.vercel.app/tiktok?username={username}"
    try:
        response = requests.get(api)
        response.raise_for_status()
        data = response.json()

        zecora1 = data.get('nickname', '  ')
        zecora2 = data.get('user_id', '  ')
        zecora3 = data.get('bio', '  ')
        zecora4 = data.get('followers', '  ')
        zecora5 = data.get('hearts', '  ')
        zecora6 = data.get('videos', '  ')
        zecora7 = data.get('create_date', '  ')
        zecora8 = data.get('language', '  ')
        zecora9 = data.get('is_private', False)
        link = f"https://www.tiktok.com/@{username}"
        zeco = InlineKeyboardMarkup()
        link2 = InlineKeyboardButton(f"{zecora1}", url=f'{link}')
        zeco.add(link2)
        if 'username' in data:
            caption = (f'''
*• Tên tài khoản ↢ {zecora1}
• ID ↢ {zecora2}
• Người theo dõi ↢ ( {zecora4} )
• Lượt thích ↢ ( {zecora5} )
• Video ↢ ( {zecora6} )
• Ngày tạo ↢ {zecora7}
• Ngôn ngữ ↢ ( {zecora8} )
• Loại ↢* {'Riêng tư' if zecora9 else 'Công khai'}
• Tiểu sử ↢ {zecora3}
''')

            zo.send_photo(ms.chat.id, data['profile_picture'], caption=caption, parse_mode='Markdown', reply_markup=zeco)
        else:
            zo.send_message(ms.chat.id, f"*• Không tìm thấy thông tin tài khoản ↢* {username}", parse_mode='Markdown')
    except requests.RequestException as e:
        zo.send_message(ms.chat.id, f"Có lỗi xảy ra: {str(e)}", parse_mode='Markdown')


@zo.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in ADMIN:
        markup = types.InlineKeyboardMarkup(row_width=2)

        user = zo.get_chat(message.from_user.id)
        owner_name = user.first_name
        owner_link = f"[{owner_name}](tg://user?id={message.from_user.id})"
        k_add = types.InlineKeyboardButton('➕ Thêm kênh', callback_data='add_channel')
        k_remove = types.InlineKeyboardButton('➖ Xóa kênh', callback_data='remove_channel')
        k_show = types.InlineKeyboardButton('🗂 Danh sách kênh', callback_data='show_channels')
        k_delete_all = types.InlineKeyboardButton('🗑️ Xóa tất cả kênh', callback_data='delete_all_channels')
        markup.add(k_show)
        markup.add(k_add, k_remove)
        markup.add(k_delete_all)
        zo.reply_to(
                message,
                text=f'👤 *Bảng điều khiển Admin*:\n\n👑 Xin chào {owner_link} trong bảng điều khiển của bạn:',
            reply_markup=markup,
            parse_mode='Markdown'
)


@zo.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
    markup.add(back_button)

    if call.data == 'add_channel':
        add_text = '🔹 Vui lòng gửi username kênh (@) để thêm:'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=add_text, reply_markup=markup)
        zo.register_next_step_handler(call.message, add_channel)

    elif call.data == 'remove_channel':
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
        markup.add(back_button)
        delete_text = '🔸 Vui lòng gửi username kênh (@) để xóa:'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=delete_text,reply_markup=markup)
        zo.register_next_step_handler(call.message, remove_channel)


    elif call.data == 'delete_all_channels':
        confirmation_markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton("✔️ | Xác nhận xóa | ✔️", callback_data='confirm_delete_all')
        cancel_button = types.InlineKeyboardButton("❌ | Hủy bỏ | ❌", callback_data='cancel_delete')
        confirmation_markup.add(confirm_button, cancel_button)

        confirmation_text = '''
⚠️ | *Bạn có chắc chắn muốn xóa tất cả các kênh?*
✨ | *Hành động này là không thể hoàn tác*
'''
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=confirmation_text, parse_mode='Markdown', reply_markup=confirmation_markup)


    elif call.data == 'confirm_delete_all':
        cursor.execute('SELECT channel_name FROM channels')
        channels = cursor.fetchall()

        if channels:
            deletes_text = '''
👑 | Chào Admin 😊❤️
✔️ | *Đã xóa tất cả các kênh thành công*

🗑️ | *Các kênh đã xóa:*
-----------------------
'''
            for channel in channels:
                deletes_text += f'👉 | {channel[0]}\n'
            deletes_text += '-----------------------'

            cursor.execute('DELETE FROM channels')
            conn.commit()
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=deletes_text, parse_mode='Markdown', reply_markup=markup)

        else:
            erer_deletes_text = '''
⚠️ | Chào Admin 🌚❤️
❌ | *Không có kênh nào để xóa*
-----------------------
'''
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=erer_deletes_text, parse_mode='Markdown', reply_markup=markup)
    elif call.data == 'cancel_delete':
        cancel_text = '😮‍💨 | *Đã hủy bỏ thao tác xóa* | 😮‍💨'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cancel_text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'show_channels':
        cursor.execute("SELECT channel_name FROM channels")
        channels = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        if channels:
            show_text = '📋 Danh sách kênh yêu cầu tham gia:'
            for channel in channels:
                channel_name = channel[0].replace("@", "")
                button = types.InlineKeyboardButton(
                    text=f'🔹 {channel_name}',
                    url=f'https://t.me/{channel_name}'
                )
                markup.add(button)
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=show_text, reply_markup=markup)
        else:
            not_exist_text = '❌ ¦ Hiện tại không có kênh nào được đăng ký ¦ ❌'
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)

            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=not_exist_text, reply_markup=markup)


def add_channel(message):
    channel_name = message.text.strip()
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    try:
        chat_info = zo.get_chat(channel_name)
        if chat_info.type not in ['channel', 'supergroup', 'group']:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)
            text = '❌ ¦ Username phải là kênh hoặc nhóm ¦ ❌'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
            return

        chat_members = zo.get_chat_administrators(channel_name)
        bot_is_admin = any(member.user.id == zo.get_me().id for member in chat_members)

        if not bot_is_admin:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)
            text = '🚫 ¦ Bot cần được cấp quyền admin trong kênh hoặc nhóm ¦ 🚫'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
            return

        cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
        channel = cursor.fetchone()

        if channel:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            Zo_text = f'''
            👑 | Chào Admin 😢💔
❌ | Kênh này đã được thêm rồi
-----------------------
- {channel_name}
-----------------------
'''
            markup.add(Back)
            zo.reply_to(message, Zo_text, reply_markup=markup)
        else:
            invite_link = zo.export_chat_invite_link(chat_info.id)
            cursor.execute("INSERT INTO channels (channel_name, invite_link) VALUES (?, ?)",
                       (channel_name, invite_link))
            conn.commit()
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            Zo_text = f'''
            👑 | Chào Admin 😊❤️
✔ | Đã thêm kênh thành công
-----------------------
- {channel_name}
🔗 | Link mời: {invite_link}
-----------------------
'''
            markup.add(Back)
            zo.reply_to(message, Zo_text, reply_markup=markup)

    except telebot.apihelper.ApiException as e:
        if "chat not found" in e.description:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)
            text = '❌ ¦ Username kênh hoặc nhóm không đúng ¦ ❌'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
        elif "Forbidden: bot was kicked" in e.description:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            markup.add(Back)
            text = '🚫 ¦ Bot đã bị chặn khỏi nhóm hoặc kênh ¦ 🚫'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
        else:
            zo.reply_to(message, f'Lỗi: {e.description}')
    except Exception as e:
        text = f"Đã xảy ra lỗi: {str(e)}"
        markup = types.InlineKeyboardMarkup()
        Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
        markup.add(Back)
        zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')

def remove_channel(message):
    channel_name = message.text.strip()

    with sqlite3.connect('channels.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
        channel = cursor.fetchone()

        if channel:
            cursor.execute("DELETE FROM channels WHERE channel_name = ?", (channel_name,))
            conn.commit()

            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            Zo_text = f'''
👑 | Chào Admin 😢💔
✔ | Đã xóa kênh thành công
-----------------------
- {channel_name}
-----------------------
            '''
            markup.add(Back)
            zo.send_message(
                message.chat.id,
                text=Zo_text,
                reply_markup=markup
            )
        else:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• Trở lại •", callback_data='Back')
            Zo_text = f'''
👑 | Chào Admin 🌚❤️
❌ | Không tìm thấy kênh để xóa
-----------------------
- {channel_name}
-----------------------
            '''
            markup.add(Back)
            zo.send_message(
                message.chat.id,
                text=Zo_text,
                reply_markup=markup
            )


import webbrowser
webbrowser.open("https://t.me/grouptmq")

print("🖤 Nhớ tham gia kênh nhé 🖤")
zo.delete_webhook()
zo.infinity_polling()
