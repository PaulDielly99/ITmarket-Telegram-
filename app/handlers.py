from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.database.requests import (get_item_by_id, set_user,
                                   set_basket, get_basket, 
                                   get_item_by_id, delete_basket)

import app.keyboards as kb

router = Router()



@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}, приветствую!🙋\n\n'
                             'Добро пожаловать в интрнет магазин IT-услуг🖥🔧\n\nВыберите пункт меню👇🏻',
                             reply_markup=kb.main)
    else:
        await message.answer('🔥Вы вернулись на главную🔥')
        await message.message.answer('Выберите пункт меню👇🏻',
                                        reply_markup=kb.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text='Выберите категорию📋',
                                     reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите услугу✨',
                                     reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item = await get_item_by_id(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.answer_photo(photo=item.photo, caption=f'{item.name}\n\n{item.description}\n\nЦена: {item.price} рублей',
                                     reply_markup=await kb.basket(item.id))


@router.callback_query(F.data.startswith('order_'))
async def basket(callback: CallbackQuery):
    await set_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('✅🔥Услуга добавлен в корзину✅🔥')


@router.callback_query(F.data == 'mybasket')
async def mybasket(callback: CallbackQuery):
    await callback.answer('')
    basket = await get_basket(callback.from_user.id)
    counter = 0
    for item_info in basket:
        item = await get_item_by_id(item_info.item)
        await callback.message.answer_photo(photo=item.photo, caption=f'{item.name}\n\n{item.description}'
                                            f'\n\nЦена: {item.price} рублей💰',
                                            reply_markup=await kb.delete_from_basket(item.id))
        counter += 1
    await callback.message.edit_text('Ваша корзина пуста😔',reply_markup=kb.to_main) if counter == 0 else await callback.answer('')
    

@router.callback_query(F.data.startswith('delete_'))
async def delete_from_basket(callback: CallbackQuery):
    await delete_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.message.delete()
    await callback.answer('Вы удалили услугу из корзины😔')


@router.callback_query(F.data == 'contacts')
async def contact(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('По всем вашим вопросам вы сможете написать мне:'
                                     '\n\n@Paul_Dielly🛠',reply_markup=kb.to_main)



