# SQL & .env FILE
import os
import sql
from dotenv import  load_dotenv
load_dotenv()


# AIOGRAM
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# YOOKASSA
import uuid
from yookassa import Payment, Configuration


# DADATA & DELIVERY
import requests
from dadata import Dadata


# YOOKASSA CONFIGURATION
Configuration.account_id = os.getenv('YOOKASSA_SHOP_ID')
Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')


# DADATA CONFIGURATION
dadata = Dadata(os.getenv('DADATA_API'), os.getenv('DADATA_SECRET_KEY'))


# AIOGRAM CONFIGURATION
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO, filename='error.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)


# ID АДМИНОВ
admins = (331237254, 413630086, 6199961135)
admin_only = lambda message: message.from_user.id in admins


# ЦЕНА ФУТБОЛКИ
tshirtPrice = 1850
tshirtWeight = 250


# КЛАВИАТУРА ПОКУПКИ
buyKeyboard = InlineKeyboardMarkup()
buyKeyboard.add(InlineKeyboardButton(text="Купить", callback_data="buyCallback"))


# КЛАВИАТУРА ПОКУПКИ №2
buyAnotherKeyboard = InlineKeyboardMarkup()
buyAnotherKeyboard.add(InlineKeyboardButton(text="Купить", callback_data="buyAnother"))


# КЛАВИАТУРА ДОБАВЛЕНИЯ В КОРЗИНУ
afterPurchaseKeyboard = InlineKeyboardMarkup()
afterPurchaseKeyboard.add(InlineKeyboardButton(text="Купить еще 🔄", callback_data="buyAnother"))
afterPurchaseKeyboard.add(InlineKeyboardButton(text="Перейти в корзину 🛒", callback_data="goToCart"))


# КЛАВИАТУРА КОРЗИНЫ
cartKeyboard = InlineKeyboardMarkup()
cartKeyboard.add(InlineKeyboardButton(text="Очистить корзину", callback_data="clearCart"))
cartKeyboard.add(InlineKeyboardButton(text="Активировать промокод 🏷️", callback_data="addDiscount"))
cartKeyboard.add(InlineKeyboardButton(text="Оформить заказ 🧾", callback_data="createPayment"))


# КЛАВИАТУРА АДРЕСА
userInfoKeyboard = InlineKeyboardMarkup()
userInfoKeyboard.add(InlineKeyboardButton(text='✅ Всё верно', callback_data='acceptPaymentInfo'))
userInfoKeyboard.add(InlineKeyboardButton(text='✏ Изменить', callback_data='declinePaymentInfo'))


# FSM ОФОРМЛЕНИЯ ЗАКАЗА
class OrderStateGroup(StatesGroup):
    fullname = State()
    phone = State()
    address = State()


# FSM ДОБАВЛЕНИЯ ПРОМОКОДА
class DiscountStateGroup(StatesGroup):
    discount = State()


# FSM РАССЫЛКИ
class MessageStateGroup(StatesGroup):
    message = State()
    photo = State()


# ИНТЕРАКТИВНАЯ КЛАВИАТУРА
def CreateMenuKeyboard():
    menuKeyboard = InlineKeyboardMarkup()
    menuKeyboard.row(InlineKeyboardButton(text='-', callback_data='quantityMinus'),
                    InlineKeyboardButton(text='1 шт.', callback_data='quantityTotal'),
                    InlineKeyboardButton(text='+', callback_data='quantityPlus'))
    menuKeyboard.row(InlineKeyboardButton(text='S', callback_data='size_S'),
                    InlineKeyboardButton(text='✅ M', callback_data='size_M'),
                    InlineKeyboardButton(text='L', callback_data='size_L'),
                    InlineKeyboardButton(text='XL', callback_data='size_XL'),
                     InlineKeyboardButton(text='XXL', callback_data='size_XXL'))
    menuKeyboard.add(InlineKeyboardButton(text='Добавить в корзину 🛒', callback_data='addToCart'))
    return menuKeyboard


# КОМАНДА ПОКУПКИ
@dp.message_handler(commands=['start', 'buy'])
async def buyCommand(message: types.Message):
    dbUser = sql.SelectUserById(message['from']['id'])
    if len(dbUser) == 0:
        sql.InsertUser(message['from']['id'], message['from']['username'], message['from']['language_code'])

    photo = open("clothes/love_tren.jpg", 'rb')
    caption = f"*OnPump «LoveTren» OVERSIZED T-SHIRT*\n\n" \
              f"Состав: 100% хлопок\n" \
              f"Плотность: 185 г/м²\n" \
              f"Принт: DTF-печать\n" \
              f"Размеры: S / M / L / XL / XXL\n\n" \
              f"*Цена:* 1 850₽"
    await message.answer_photo(photo=photo, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=buyKeyboard)


# ПРОДОЛЖЕНИЕ ПОКУПКИ
@dp.callback_query_handler(text="buyCallback")
async def buyCallback(callback: types.CallbackQuery):
    menuKeyboard = CreateMenuKeyboard()
    sql.InsertUserPrecart(callback.message.chat.id, callback.message.message_id)
    await callback.message.edit_caption(f"*OnPump «LoveTren» OVERSIZED T-SHIRT*\n\n"
                                        f"*Выбранный размер:* M\n"
                                        f"*Итоговая стоимость:* 1 850₽ × 1 = 1 850₽\n\n"
                                        f"Если все верно, нажмите *кнопку «Добавить в корзину»*",
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=menuKeyboard)


# ИЗМЕНЕНИЕ РАЗМЕРА
@dp.callback_query_handler(text_startswith="size_")
async def changeSizeCallback(callback: types.CallbackQuery):
    button = None
    totalButton = None

    userPrecart = sql.SelectUserPrecart(callback.message.chat.id, callback.message.message_id)

    menuKeyboard = CreateMenuKeyboard()
    buttonTextList = ['S', 'M', 'L', 'XL', 'XXL']
    buttonRow = menuKeyboard.values['inline_keyboard'][1]

    for i in range(len(buttonRow)):
        buttonRow[i].text = f"{buttonTextList[i]}"
        if callback.data == buttonRow[i]['callback_data']:
            button = buttonRow[i]
    button.text = f"✅ {callback.data.replace('size_', '')}"

    buttonRow = menuKeyboard.values['inline_keyboard'][0]
    for i in range(len(buttonRow)):
        if buttonRow[i]['callback_data'] == "quantityTotal":
            totalButton = buttonRow[i]
    totalButton.text = f"{userPrecart[0][4]} шт."

    sql.UpdateUserPrecartSize(callback.data.replace('size_', ''), callback.message.chat.id, callback.message.message_id)
    priceFormat = '{:,}'.format(tshirtPrice * userPrecart[0][4]).replace(',', ' ')
    await callback.message.edit_caption(f"*OnPump «LoveTren» OVERSIZED T-SHIRT*\n\n"
                                        f"*Выбранный размер:* {callback.data.replace('size_', '')}\n"
                                        f"*Итоговая стоимость:* 1 850₽ × {userPrecart[0][4]} = {priceFormat}₽\n\n"
                                        f"Если все верно, нажмите *кнопку «Добавить в корзину»*", parse_mode=ParseMode.MARKDOWN, reply_markup=menuKeyboard)


# ИЗМЕНЕНИЕ КОЛИЧЕСТВА
@dp.callback_query_handler(text_startswith="quantity")
async def changeQuantityCallback(callback: types.CallbackQuery):
    button = None
    totalButton = None

    userPrecart = sql.SelectUserPrecart(callback.message.chat.id, callback.message.message_id)

    menuKeyboard = CreateMenuKeyboard()
    buttonTextList = ['S', 'M', 'L', 'XL', 'XXL']
    buttonRow = menuKeyboard.values['inline_keyboard'][1]

    for i in range(len(buttonRow)):
        buttonRow[i].text = f"{buttonTextList[i]}"
        if buttonRow[i]['callback_data'].replace("size_", '') == userPrecart[0][3]:
            button = buttonRow[i]
    button.text = f"✅ {userPrecart[0][3]}"

    buttonRow = menuKeyboard.values['inline_keyboard'][0]
    for i in range(len(buttonRow)):
        if callback.data == buttonRow[i]['callback_data']:
            button = buttonRow[i]
        if buttonRow[i]['callback_data'] == "quantityTotal":
            totalButton = buttonRow[i]

    quantity = userPrecart[0][4]
    if button.callback_data == "quantityMinus" and quantity > 1:
        quantity -= 1
    elif button.callback_data == "quantityPlus":
        quantity += 1

    totalButton.text = f"{quantity} шт."
    sql.UpdateUserPrecartQuantity(quantity, callback.message.chat.id, callback.message.message_id)
    priceFormat = '{:,}'.format(tshirtPrice * quantity).replace(',', ' ')
    await callback.message.edit_caption(f"*OnPump «LoveTren» OVERSIZED T-SHIRT*\n\n"
                                        f"*Выбранный размер:* {userPrecart[0][3]}\n"
                                        f"*Итоговая стоимость:* 1 850₽ × {quantity} = {priceFormat}₽\n\n"
                                        f"Если все верно, нажмите *кнопку «Добавить в корзину»*", parse_mode=ParseMode.MARKDOWN, reply_markup=menuKeyboard)


# ДОБАВЛЕНИЕ В КОРЗИНУ
@dp.callback_query_handler(text="addToCart")
async def addToCart(callback: types.CallbackQuery):
    userPrecart = sql.SelectUserPrecart(callback.message.chat.id, callback.message.message_id)
    sql.InsertUserCart(callback.message.chat.id, userPrecart[0][3], userPrecart[0][4])
    sql.DeleteUserPrecart(callback.message.chat.id, callback.message.message_id)
    priceFormat = '{:,}'.format(tshirtPrice * userPrecart[0][4]).replace(',', ' ')
    await callback.message.delete()
    await callback.message.answer(f"*👕 Товар успешно добавлен в корзину:*\n"
                                  f"OnPump «LoveTren» OVERSIZED T-SHIRT\n"
                                  f"*Размер:* {userPrecart[0][3]}\n"
                                  f"*Количество:* {userPrecart[0][4]}\n"
                                  f"*Итоговая стоимость:* {priceFormat}₽", parse_mode=ParseMode.MARKDOWN, reply_markup=afterPurchaseKeyboard)


# КУПИТЬ ЕЩЕ (ПОСЛЕ ДОБАВЛЕНИЯ В КОРЗИНУ)
@dp.callback_query_handler(text="buyAnother")
async def buyAnother(callback: types.CallbackQuery):
    photo = open("clothes/love_tren.jpg", 'rb')
    caption = f"*OnPump «LoveTren» OVERSIZED T-SHIRT*\n\n" \
              f"Состав: 100% хлопок\n" \
              f"Плотность: 185 г/м²\n" \
              f"Принт: DTF-печать\n" \
              f"Размеры: S / M / L / XL / XXL\n\n" \
              f"*Цена:* 1 850₽"
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=buyKeyboard)


# КОМАНДА КОРЗИНЫ
@dp.message_handler(commands=['cart'])
async def cartCommand(message: types.Message):
    totalSum = 0
    msg = f"*Корзина 🛒*\n" \
          f"➖➖➖➖➖\n"

    cart = sql.SelectUserCart(message.chat.id)
    uDiscount = sql.SelectUserDiscount(message.chat.id)

    if len(cart) > 0:
        for index, items in enumerate(cart):
            totalSum += tshirtPrice * items[3]
            priceFormat = '{:,}'.format(tshirtPrice * items[3]).replace(',', ' ')
            msg += f"{index + 1}. OnPump «LoveTren» OVERSIZED T-SHIRT [{items[2]}] × {items[3]} = {priceFormat}₽\n"

        if len(uDiscount) > 0:
            discount = sql.SelectDiscountById(uDiscount[0][2])
            totalSum = totalSum - (totalSum * discount[0][2] / 100)
            totalSum = '{:,}'.format(totalSum).replace(',', ' ').replace('.0', '')
            msg += f"➖➖➖➖➖\n" \
                   f"*Активированный промокод:* {discount[0][1]}\n" \
                   f"*Итоговая стоимость:* {totalSum}₽"
        else:
            totalSum = '{:,}'.format(totalSum).replace(',', ' ')
            msg += f"➖➖➖➖➖\n" \
                   f"*Итоговая стоимость:* {totalSum}₽"
        await message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=cartKeyboard)
    else:
        await message.answer(f"*Корзина 🛒*\n"
                                         f"➖➖➖➖➖\n"
                                         f"Пусто...\n"
                                         f"➖➖➖➖➖\n"
                                         f"*Итоговая стоимость:* 0₽", parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=buyAnotherKeyboard)


# ПЕРЕХОД В КОРЗИНУ
@dp.callback_query_handler(text="goToCart")
async def goToCart(callback: types.CallbackQuery):
    await callback.message.delete()
    totalSum = 0
    msg = f"*Корзина 🛒*\n" \
          f"➖➖➖➖➖\n"

    cart = sql.SelectUserCart(callback.message.chat.id)
    uDiscount = sql.SelectUserDiscount(callback.message.chat.id)

    if len(cart) > 0:
        for index, items in enumerate(cart):
            totalSum += tshirtPrice * items[3]
            priceFormat = '{:,}'.format(tshirtPrice * items[3]).replace(',', ' ')
            msg += f"{index + 1}. OnPump «LoveTren» OVERSIZED T-SHIRT [{items[2]}] × {items[3]} = {priceFormat}₽\n"

        if len(uDiscount) > 0:
            discount = sql.SelectDiscountById(uDiscount[0][2])
            totalSum = totalSum - (totalSum * discount[0][2] / 100)
            totalSum = '{:,}'.format(totalSum).replace(',', ' ').replace('.0', '')
            msg += f"➖➖➖➖➖\n" \
                   f"*Активированный промокод:* {discount[0][1]}\n" \
                   f"*Итоговая стоимость:* {totalSum}₽"
        else:
            totalSum = '{:,}'.format(totalSum).replace(',', ' ')
            msg += f"➖➖➖➖➖\n" \
                   f"*Итоговая стоимость:* {totalSum}₽"
        await callback.message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=cartKeyboard)
    else:
        await callback.message.answer(f"*Корзина 🛒*\n"
                             f"➖➖➖➖➖\n"
                             f"Пусто...\n"
                             f"➖➖➖➖➖\n"
                             f"Итоговая стоимость: 0₽", parse_mode=ParseMode.MARKDOWN,
                             reply_markup=buyAnotherKeyboard)


# ДОБАВЛЕНИЕ ПРОМОКОДА
@dp.callback_query_handler(text="addDiscount")
async def addDiscount(callback: types.CallbackQuery):
    await callback.message.delete()
    await DiscountStateGroup.discount.set()
    await callback.message.answer("Введите промокод, для активации скидки:")


# ПОЛУЧЕНИЕ ПРОМОКОДА, ВВЕДЕННОГО ПОЛЬЗОВАТЕЛЕМ
@dp.message_handler(state=DiscountStateGroup.discount)
async def getDiscount(message: types.Message, state: FSMContext):
    discountKeyboard = InlineKeyboardMarkup()
    discountKeyboard.add(InlineKeyboardButton(text="Ввести другой промокод 🏷️", callback_data="addDiscount"))
    discountKeyboard.add(InlineKeyboardButton(text="Вернуться в корзину 🛒", callback_data="goToCart"))

    sKeyboard = InlineKeyboardMarkup()
    sKeyboard.add(InlineKeyboardButton(text='Вернуться в корзину 🛒', callback_data='goToCart'))

    await state.finish()
    discount = sql.SelectDiscount(message.text)
    if len(discount) > 0:
        sql.DeleteUserDiscount(message.chat.id)
        sql.InsertUserDiscount(message.chat.id, discount[0][0])
        sql.UpdateDiscountUsage(discount[0][0])
        await message.answer(f"Промокод `{discount[0][1]}` на скидку в {discount[0][2]}% успешно применен!", parse_mode=ParseMode.MARKDOWN, reply_markup=sKeyboard)
    else:
        await message.answer("Промокод не найден!", reply_markup=discountKeyboard)


# ОЧИСТКА КОРЗИНЫ
@dp.callback_query_handler(text="clearCart")
async def clearCart(callback: types.CallbackQuery):
    sql.DeleteUserCart(callback.message.chat.id)
    sql.DeleteUserDiscount(callback.message.chat.id)
    await callback.message.edit_text(f"*Корзина 🛒*\n"
                                     f"➖➖➖➖➖\n"
                                     f"Пусто...\n"
                                     f"➖➖➖➖➖\n"
                                     f"*Итоговая стоимость:* 0₽", parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=buyAnotherKeyboard)


# СОЗДАТЬ ПЛАТЕЖ
@dp.callback_query_handler(text="createPayment")
async def createPayment(callback: types.CallbackQuery):
    await OrderStateGroup.fullname.set()
    await callback.message.answer(f"👤 *Укажите ФИО как показано на примере ниже:*\n"
                                  f"Иванов Иван Иванович", parse_mode=ParseMode.MARKDOWN)


# ПОЛУЧЕНИЕ ФИО ПОЛЬЗОВАТЕЛЯ
@dp.message_handler(state=OrderStateGroup.fullname)
async def getName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await OrderStateGroup.next()
    await message.answer(f"📱*Укажите номер телефона*\n"
                         f"*В формате:* +79012345678", parse_mode=ParseMode.MARKDOWN)


# ПОЛУЧЕНИЕ ТЕЛЕФОНА ПОЛЬЗОВАТЕЛЯ
@dp.message_handler(state=OrderStateGroup.phone)
async def getPhone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        await OrderStateGroup.next()
        await message.answer("🚚 *Укажите пункт выдачи СДЭКа*\n\n"
                     "*Например:* Москва Тверская 4 кв 56\n", parse_mode=ParseMode.MARKDOWN)


# ПОЛУЧЕНИЕ АДРЕСА ПОЛЬЗОВАТЕЛЯ
@dp.message_handler(state=OrderStateGroup.address)
async def getAddress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        result = dadata.clean("address", message.text)
        if result['country'] in ("Россия", "Казахстан", "Беларусь"):
            await message.answer(f"👤 *ФИО:* {data['fullname']}\n"
                                 f"📱*Телефон:* {data['phone']}\n"
                                 f"🚚 *Указанный адрес:* {result['result']}\n\n"
                                 f"Проверьте правильность введенных данных!", parse_mode=ParseMode.MARKDOWN, reply_markup=userInfoKeyboard)
            sql.InsertPaymentInfo(message.chat.id, data['fullname'], data['phone'], result['result'], result['postal_code'], result['country'])
        else:
            await message.answer(f"Извините, на данный момент доставка по адресу `{result['result']}` невозможна!", parse_mode=ParseMode.MARKDOWN)
    await state.finish()


# ИЗМЕНЕНИЕ ИНФОРМАЦИИ ПОЛЬЗОВАТЕЛЯ (ИНФОРМАЦИЯ ОТ ПОЛЬЗОВАТЕЛЯ НЕ ВЕРНА)
@dp.callback_query_handler(text="declinePaymentInfo")
async def declinePaymentInfo(callback: types.CallbackQuery):
    await OrderStateGroup.fullname.set()
    await callback.message.answer(f"👤 *Укажите ФИО как показано на примере ниже:*\n"
                                  f"Иванов Иван Иванович", parse_mode=ParseMode.MARKDOWN)


# ФОРМИРОВАНИЕ ССЫЛКИ НА ПЛАТЕЖ (ИНФОРМАЦИЯ ОТ ПОЛЬЗОВАТЕЛЯ ВЕРНА)
@dp.callback_query_handler(text="acceptPaymentInfo")
async def acceptPaymentInfo(callback: types.CallbackQuery):
    sizes = ""
    amount = 0
    delivery = 0
    paymentValue = 0
    info = sql.SelectUserPaymentInfo(callback.message.chat.id)
    cart = sql.SelectUserCart(callback.message.chat.id)

    username = sql.SelectUsernameById(callback.message.chat.id)
    if username[0][0] is None:
        username = info[0][1]
    else:
        username = username[0][0]

    desc = f"Заказ от пользователя @{username}. Размеры: "

    uDiscount = sql.SelectUserDiscount(callback.message.chat.id)

    for index, items in enumerate(cart):
        amount += items[3]
        sizes += f"{items[2]} {items[3]};"
        paymentValue += tshirtPrice * items[3]

    if len(uDiscount) > 0:
        discount = sql.SelectDiscountById(uDiscount[0][2])
        paymentValue = paymentValue - (paymentValue * discount[0][2] / 100)

    if info[0][6] == "Россия":
        r = requests.get(f"https://postprice.ru/engine/russia/api.php?from=432072&to={info[0][5]}&mass={amount * tshirtWeight}&vat=1&apikey={os.getenv('POSTPRICE_API')}")
        if amount < 2:
            delivery = int(r.json()['pkg']) + 24 + 30
        else:
            delivery = int(r.json()['pkg']) + 64 + 60
    elif info[0][6] == "Беларусь":
        if amount < 2:
            delivery = 490 + 24 + 30
        else:
            delivery = 490 + 24 + 60
    elif info[0][6] == "Казахстан":
        if amount < 2:
            delivery = 520 + 24 + 30
        else:
            delivery = 520 + 24 + 60
    paymentValue = str(paymentValue + delivery).replace('.0', '')

    payment = Payment.create({
        "amount": {
          "value": f"{paymentValue}.00",
          "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/onpumpbot"
        },
        "capture": True,
        "description": f"{desc}{sizes}"
    }, uuid.uuid4())
    sql.InsertReceipt(callback.message.chat.id, payment.id, sizes, paymentValue, info[0][2], info[0][3], info[0][4])

    photo = open("clothes/love_tren.jpg", 'rb')
    confirmation_url = payment.confirmation.confirmation_url
    priceFormat = '{:,}'.format(int(paymentValue)).replace(',', ' ')
    caption = f"👤 *ФИО:* {info[0][2]}\n" \
              f"📱*Телефон:* {info[0][3]}\n" \
              f"🚚 *Указанный адрес:* {info[0][4]}\n\n" \
              f"📦 *Стоимость доставки:* {delivery}₽\n" \
              f"*Итоговая стоимость:* {priceFormat}₽"

    payKeyboard = InlineKeyboardMarkup()
    payKeyboard.add(InlineKeyboardButton(text="Заплатить 💳", url=confirmation_url))
    payKeyboard.add(InlineKeyboardButton(text="Проверить статус платежа", callback_data=f"checkData_{payment.id}"))
    await callback.message.answer_photo(photo=photo, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=payKeyboard)


# ПРОВЕРКА СТАТУСА ПЛАТЕЖА
@dp.callback_query_handler(text_startswith="checkData_")
async def checkData(callback: types.CallbackQuery):
    paymentId = callback.data.replace("checkData_", '')
    payment = Payment.find_one(paymentId)
    sql.UpdateReceiptStatus(paymentId, payment.status)

    if payment.status == "pending":
        await callback.message.answer(f"❌ Оплата не произведена! ", parse_mode=ParseMode.MARKDOWN)
    elif payment.status == "canceled":
        await callback.message.answer(f"❌ Платеж отменен!", parse_mode=ParseMode.MARKDOWN)
    elif payment.status == "succeeded":
        np = sql.InsertSucceededPayment(paymentId)
        sql.DeleteReceipt(paymentId)
        sql.DeleteUserCart(callback.message.chat.id)
        sql.DeleteUserDiscount(callback.message.chat.id)
        sql.DeleteUserPaymentInfo(callback.message.chat.id)
        sql.InsertNotify(paymentId)
        sql.InsertTrack(np)
        await callback.message.delete()
        await callback.message.answer(f"✅ Оплата прошла успешно! После отправки бот пришлет Вам трек-код. ", parse_mode=ParseMode.MARKDOWN)

        info = sql.SelectSucceededPayment(paymentId)
        username = sql.SelectUsernameById(callback.message.chat.id)
        if username[0][0] is None:
            username = info[0][1]
        else:
            username = username[0][0]

        msg = f"Пользователь @{username} оплатил заказ №{info[0][0]} на сумму {info[0][4]}₽\n\n" \
              f"*Размеры:* {info[0][3]}\n" \
              f"*ФИО:* {info[0][6]}\n" \
              f"*Телефон:* {info[0][7]}\n" \
              f"*Адрес:* {info[0][8]}"
        await bot.send_message(-912473672, msg, parse_mode=ParseMode.MARKDOWN)
        sql.UpdateNotify(paymentId)


# ВЫВОД ПОЛЬЗОВАТЕЛЮ ЕГО ЗАКАЗОВ
@dp.message_handler(commands=['orders'])
async def ordersCommand(message: types.Message):
    msg = "*Список всех ваших заказов:*\n\n"
    payments = sql.SelectUserPayments(message.chat.id)

    for p in payments:
        code = sql.SelectTrackCodeByPaymentId(p[0])
        priceFormat = '{:,}'.format(p[4]).replace(',', ' ')
        msg += f"*Заказ №*`{p[0]}` на сумму {priceFormat}₽\n"

        if code[0][0] is not None:
            msg += f"*Трек-код*: `{code[0][0]}`\n\n"
        else:
            msg += f"*Трек-код*: отсутствует\n\n"
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


# СПИСОК ВСЕХ КОМАНД
@dp.message_handler(admin_only, commands=['help', 'info', 'information'])
async def helpMessage(message: types.Message):
    await message.answer(f"*Доступные команды:*\n\n"
                         f"/update - обновить все платежи\n\n"
                         f"/send <номер заказа> <трек-код> - отправить трек-код по номеру заказа\n\n"
                         f"/without - список заказов без трек-кода\n\n"
                         f"/get <трек-код> - информация о заказе по трек-коду\n\n"
                         f"/order <номер заказ> - информация о заказе\n\n"
                         f"/sizes - информация о заказанных размерах\n\n"
                         f"/gain - информация о выручке\n\n"
                         f"/users - количество пользователей в БД\n\n"
                         f"/promo <промокод> - информация по промокоду\n\n"
                         f"/msg - общая рассылка", parse_mode=ParseMode.MARKDOWN)


# ОБНОВИТЬ ПЛАТЕЖИ
@dp.message_handler(admin_only, commands=['update'])
async def updateReceipts(message: types.Message):
    receipts = sql.SelectReceipts()
    for item in receipts:
        paymentId = item[2]
        payment = Payment.find_one(paymentId)
        sql.UpdateReceiptStatus(paymentId, payment.status)

        if payment.status == "canceled":
            sql.DeleteReceipt(paymentId)
        elif payment.status == "succeeded":
            np = sql.InsertSucceededPayment(paymentId)
            username = sql.SelectUsernameById(item[1])
            sql.DeleteReceipt(paymentId)
            sql.DeleteUserCart(item[1])
            sql.DeleteUserPaymentInfo(item[1])
            sql.InsertNotify(paymentId)
            sql.InsertTrack(np)

            await bot.send_message(item[1], "✅ Оплата прошла успешно! После отправки бот пришлет Вам трек-код. ",
                                          parse_mode=ParseMode.MARKDOWN)

            if username[0][0] is None:
                username = item[1]
            else:
                username = username[0][0]

            msg = f"Пользователь @{username} оплатил заказ №{np} на сумму {item[4]}₽\n\n" \
                  f"*Размеры:* {item[3]}\n" \
                  f"*ФИО:* {item[6]}\n" \
                  f"*Телефон:* {item[7]}\n" \
                  f"*Адрес:* {item[8]}"
            await bot.send_message(-912473672, msg, parse_mode=ParseMode.MARKDOWN)
            sql.UpdateNotify(paymentId)


# ОТПРАВКА ТРЕК-КОДА ПО НОМЕРУ ЗАКАЗА
@dp.message_handler(admin_only, commands=['send', 'send_track'])
async def sendTrack(message: types.Message):
    args = message.get_args()
    args = args.split()
    payment = sql.SelectSucceededPaymentById(args[0])
    sql.UpdateTrack(args[0], args[1])
    await bot.send_message(payment[0][1], f"🧾 Ваш трек-код для заказа №{args[0]}: `{args[1]}`\n", parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(message.chat.id, "Трек-код отправлен!")


# СПИСОК ЗАКАЗОВ БЕЗ ТРЕК-КОДА
@dp.message_handler(admin_only, commands=['without', 'without_track'])
async def withoutTrack(message: types.Message):
    payments = sql.SelectPaymentsWoTrackCode()
    for p in payments:
        username = sql.SelectUsernameById(p[1])
        if username[0][0] is None:
            username = p[1]
        else:
            username = username[0][0]

        msg = f"Заказ №{p[0]} на сумму {p[4]}₽ от пользователя @{username}\n\n" \
              f"*Размеры:* {p[3]}\n" \
              f"*ФИО:* {p[6]}\n" \
              f"*Телефон:* {p[7]}\n" \
              f"*Адрес:* {p[8]}"
        await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


# ПОЛУЧИТЬ ЗАКАЗ ПО ТРЕК-КОДУ
@dp.message_handler(admin_only, commands=['get', 'get_track'])
async def getTrack(message: types.Message):
    args = message.get_args()
    payment = sql.SelectPaymentByTrackCode(args)
    username = sql.SelectUsernameById(payment[0][1])
    if username[0][0] is None:
        username = payment[0][1]
    else:
        username = username[0][0]

    msg = f"Заказ №{payment[0][0]} на сумму {payment[0][4]}₽ от пользователя @{username}\n\n" \
          f"*Размеры:* {payment[0][3]}\n" \
          f"*ФИО:* {payment[0][6]}\n" \
          f"*Телефон:* {payment[0][7]}\n" \
          f"*Адрес:* {payment[0][8]}"
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


# ПОЛУЧИТЬ ИНФОРМАЦИЮ О ЗАКАЗЕ ПО ЕГО НОМЕРУ
@dp.message_handler(admin_only, commands=['order'])
async def getOrder(message: types.Message):
    args = message.get_args()
    payment = sql.SelectPayment(args)
    username = sql.SelectUsernameById(payment[0][1])
    if username[0][0] is None:
        username = payment[0][1]
    else:
        username = username[0][0]

    msg = f"Заказ №{payment[0][0]} на сумму {payment[0][4]}₽ от пользователя @{username}\n\n" \
          f"*Размеры:* {payment[0][3]}\n" \
          f"*ФИО:* {payment[0][6]}\n" \
          f"*Телефон:* {payment[0][7]}\n" \
          f"*Адрес:* {payment[0][8]}"
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


# РАЗМЕРЫ ПО ВСЕМ ЗАКАЗАМ
@dp.message_handler(admin_only, commands=['sizes'])
async def selectSizes(message: types.Message):
    s, m, l, xl, xxl = 0, 0, 0, 0, 0

    payments = sql.SelectSucceededPayments()
    for p in payments:
        pSize = p[3].split(';')
        for index, size in enumerate(pSize):
            size = size.replace(' ', '')
            if size.startswith('S'):
                s += int(size.replace("S", ''))
            elif size.startswith('M'):
                m += int(size.replace("M", ''))
            elif size.startswith('L'):
                l += int(size.replace("L", ''))
            elif size.startswith('XL'):
                xl += int(size.replace("XL", ''))
            elif size.startswith('XXL'):
                xxl += int(size.replace("XXL", ''))

    await message.answer(f"*Размер S:* {s}\n"
                         f"*Размер M:* {m}\n"
                         f"*Размер L:* {l}\n"
                         f"*Размер XL:* {xl}\n"
                         f"*Размер XXL:* {xxl}", parse_mode=ParseMode.MARKDOWN)


# ВЫРУЧКА
@dp.message_handler(admin_only, commands=['gain'])
async def getGain(message: types.Message):
    gain = sql.SelectGain()
    total = '{:,}'.format(gain[0][0]).replace(',', ' ')
    await message.answer(f"*Общая выручка:* {total}₽", parse_mode=ParseMode.MARKDOWN)


# КОЛИЧЕСТВО ПОЛЬЗОВАТЕЛЕЙ В БД
@dp.message_handler(admin_only, commands=['users'])
async def usersAmount(message: types.Message):
    amount = sql.SelectUsersAmount()
    await message.answer(f"*Всего пользователей:* {amount[0][0]}", parse_mode=ParseMode.MARKDOWN)


# ИНФОРМАЦИЯ ПО ПРОМОКОДАМ
@dp.message_handler(admin_only, commands=['promo'])
async def promoUsages(message: types.Message):
    args = message.get_args()
    promo = sql.SelectDiscount(args)
    await message.answer(f"Промокод `{promo[0][1]}`\n"
                         f"*Всего использований:* {promo[0][3]}", parse_mode=ParseMode.MARKDOWN)


# РАССЫЛКА
@dp.message_handler(admin_only, commands=['msg'])
async def sendAll(message: types.Message):
    await MessageStateGroup.message.set()
    await message.answer("Напиши текст сообщения ")


# ПОЛУЧЕНИЕ ТЕКСТА РАССЫЛКИ
@dp.message_handler(state=MessageStateGroup.message)
async def getMessage(message: types.Message, state: FSMContext):
    messageKeyboard = InlineKeyboardMarkup()
    messageKeyboard.add(InlineKeyboardButton(text="🖼 Добавить фото", callback_data="addPhotoToMessage"))
    messageKeyboard.add(InlineKeyboardButton(text="📨 Отправить сообщение", callback_data="sendMessage"))
    messageKeyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancelMessage"))

    async with state.proxy() as data:
        data['message'] = message.md_text.replace('\\', '')
        await message.answer(f"Ваше сообщение:\n\n{data['message']}", parse_mode=ParseMode.MARKDOWN, reply_markup=messageKeyboard)


# ДОБАВЛЕНИЕ ФОТО К ТЕКСТУ РАССЫЛКИ
@dp.callback_query_handler(text="addPhotoToMessage", state='*')
async def addPhotoToMessage(callback: types.CallbackQuery, state: FSMContext):
    await MessageStateGroup.photo.set()
    await callback.message.answer("Пришлите фото")


# ПОЛУЧЕНИЕ ФОТО
@dp.message_handler(state=MessageStateGroup.photo, content_types=['photo'])
async def getPhoto(message: types.Message, state: FSMContext):
    messageKeyboard = InlineKeyboardMarkup()
    messageKeyboard.add(InlineKeyboardButton(text='📨 Отправить сообщение', callback_data='sendPhotoMessage'))
    messageKeyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancelMessage'))

    async with state.proxy() as data:
        data['photo'] = message.photo[0]['file_id']
        await message.answer_photo(photo=data['photo'], caption=data['message'], parse_mode=ParseMode.MARKDOWN, reply_markup=messageKeyboard)


# ОТПРАВИТЬ СООБЩЕНИЕ (БЕЗ ФОТО)
@dp.callback_query_handler(text="sendMessage", state='*')
async def sendMessage(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Сообщение отправлено всем пользователям!")

    async with state.proxy() as data:
        users = sql.SelectUsers()
        for u in users:
            await bot.send_message(u[0], data['message'], parse_mode=ParseMode.MARKDOWN)
    await state.finish()


# ОТПРАВИТЬ СООБЩЕНИЕ (С ФОТО)
@dp.callback_query_handler(text="sendPhotoMessage", state='*')
async def sendPhotoMessage(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Сообщение отправлено всем пользователям!")

    async with state.proxy() as data:
        users = sql.SelectUsers()
        for u in users:
            await bot.send_photo(u[0], photo=data['photo'], caption=data['message'], parse_mode=ParseMode.MARKDOWN)
    await state.finish()


# ОТМЕНИТЬ РАССЫЛКУ
@dp.callback_query_handler(text="cancelMessage", state='*')
async def cancelMessage(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("❌ Отменено")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)