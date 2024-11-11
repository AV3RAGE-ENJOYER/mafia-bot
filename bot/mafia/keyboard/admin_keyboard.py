from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ADMIN

kb_admin_builder = ReplyKeyboardBuilder()
kb_admin_builder.button(text="Создать рассылку")
kb_admin_builder.button(text="Посмотреть статистику")
kb_admin_builder.button(text="Назад")

kb_admin_builder.adjust(2, 1)

kb_admin = kb_admin_builder.as_markup()
kb_admin.resize_keyboard = True

kb_admin_cancel_builder = ReplyKeyboardBuilder()
kb_admin_cancel_builder.button(text="Отмена")

kb_admin_cancel = kb_admin_cancel_builder.as_markup()
kb_admin_cancel.resize_keyboard = True

kb_admin_confirm_builder = ReplyKeyboardBuilder()
kb_admin_confirm_builder.button(text="Да")
kb_admin_confirm_builder.button(text="Отмена")

kb_admin_confirm = kb_admin_confirm_builder.as_markup()
kb_admin_confirm.resize_keyboard = True