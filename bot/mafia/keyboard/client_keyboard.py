from mafia.config import BOT_TYPE
from responses import responses
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

kb_client_builder = ReplyKeyboardBuilder()

kb_client_builder.button(text="Сюжет")
kb_client_builder.button(text="Ход игры")
kb_client_builder.button(text="Роли")
kb_client_builder.button(text="Челленджи")
kb_client_builder.button(text="Купить магфию")

kb_client_builder.adjust(3, 1)

kb_client = kb_client_builder.as_markup()
kb_client.resize_keyboard = True

# RULES

kb_rules_builder = ReplyKeyboardBuilder()

kb_rules_builder.button(text="Ночь")
kb_rules_builder.button(text="Утро")
kb_rules_builder.button(text="Дневные голосования")
kb_rules_builder.button(text="Назад")

kb_rules_builder.adjust(3, 1)

kb_rules = kb_rules_builder.as_markup()
kb_rules.resize_keyboard = True

# GAME

kb_game_builder = ReplyKeyboardBuilder()

kb_game_builder.button(text="Рандомное задание")
kb_game_builder.button(text="Назад")
kb_game_builder.adjust(1, 1)

kb_game = kb_game_builder.as_markup()
kb_game.resize_keyboard = True

# BUY

kb_buy_builder = InlineKeyboardBuilder()
kb_buy_builder.button(text="Менеджер", url="https://t.me/magfia_admin")

kb_buy = kb_buy_builder.as_markup()

# ROLES

kb_roles_builder = InlineKeyboardBuilder()
kb_roles_builder.button(text=responses[BOT_TYPE]["vil_kb"], callback_data="vil")
kb_roles_builder.button(text=responses[BOT_TYPE]["dl_kb"], callback_data="dl")
kb_roles_builder.button(text=responses[BOT_TYPE]["her_kb"], callback_data="her")
kb_roles_builder.button(text=responses[BOT_TYPE]["doc_kb"], callback_data="doc")
kb_roles_builder.button(text=responses[BOT_TYPE]["dem_kb"], callback_data="dem")
kb_roles_builder.button(text=responses[BOT_TYPE]["bad_kb"], callback_data="bad")
kb_roles_builder.button(text=responses[BOT_TYPE]["pri_kb"], callback_data="pri")
kb_roles_builder.button(text=responses[BOT_TYPE]["pol_kb"], callback_data="pol")
kb_roles_builder.button(text=responses[BOT_TYPE]["aut_kb"], callback_data="aut")
kb_roles_builder.adjust(2, repeat=True)

kb_roles = kb_roles_builder.as_markup()

# CHANNEL

kb_check_menu_builder = InlineKeyboardBuilder()
kb_check_menu_builder.button(text="ПОДПИСАТЬСЯ", url=responses[BOT_TYPE]["url"])
kb_check_menu_builder.button(text="ПОДТВЕРДИТЬ ПОДПИСКУ", callback_data="sub_done")
kb_check_menu_builder.adjust(1, 1)

kb_check_menu = kb_check_menu_builder.as_markup()