import os
import sqlite3
from dotenv import  load_dotenv


load_dotenv()
db = os.getenv('DB')


def SelectUserById(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM users WHERE id = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUserPrecart(userId, messageId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM precart WHERE userId = ? AND messageId = ? "
    sql_query_data = (userId, messageId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUserCart(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM cart WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUserPaymentInfo(userId,):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM paymentInfo WHERE userId = ? ORDER BY id DESC LIMIT 1 "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUsernameById(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT username FROM [users] WHERE id = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectSucceededPaymentById(id):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments WHERE id = ? "
    sql_query_data = (id,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectSucceededPayment(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments WHERE paymentId = ? "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectReceipts():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM receipts "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUsers():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM users "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectPayment(id):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments WHERE id = ? "
    sql_query_data = (id,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectPaymentsWoTrackCode():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments LEFT OUTER JOIN tracks ON succeededPayments.id = tracks.paymentId WHERE tracks.code is NULL "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectPaymentByTrackCode(track):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments LEFT OUTER JOIN tracks ON succeededPayments.id = tracks.paymentId WHERE tracks.code = ? "
    sql_query_data = (track,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectTrackCodeByPaymentId(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT tracks.code FROM succeededPayments LEFT OUTER JOIN tracks ON succeededPayments.id = tracks.paymentId WHERE succeededPayments.id = ? "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUsersAmount():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT COUNT(id) FROM users "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectGain():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT SUM(price) FROM succeededPayments "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectSucceededPayments():
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments "
    sql_cursor.execute(sql_query,)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectDiscount(promo):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM discounts WHERE promo = ? "
    sql_query_data = (promo,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectDiscountById(id):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM discounts WHERE id = ? "
    sql_query_data = (id,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUserDiscount(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM userDiscount WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def SelectUserPayments(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " SELECT * FROM succeededPayments WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def InsertUser(userId, username, language_code):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO users (id, username, language_code) VALUES (?, ?, ?) "
    sql_query_data = (userId, username, language_code)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertUserCart(userId, size, quantity):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO cart(userId, size, quantity) VALUES (?, ?, ?) "
    sql_query_data = (userId, size, quantity)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertUserPrecart(userId, messageId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO precart(userId, messageId, size, quantity) VALUES (?, ?, 'M', 1) "
    sql_query_data = (userId, messageId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertPaymentInfo(userId, fio, phone, address, postal_code, country):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO paymentInfo (userId, fio, phone, address, postal_code, country) VALUES (?, ?, ?, ?, ?, ?) "
    sql_query_data = (userId, fio, phone, address, postal_code, country)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertReceipt(userId, paymentId, sizes, price, fio, phone, address):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO receipts (userId, paymentId, sizes, price, status, fio, phone, address) VALUES (?, ?, ?, ?, 'pending', ?, ?, ?) "
    sql_query_data = (userId, paymentId, sizes, price, fio, phone, address)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertSucceededPayment(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO succeededPayments SELECT * FROM receipts WHERE receipts.paymentId = ? "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertNotify(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO notifications(paymentId, notify) VALUES(?, 0) "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertTrack(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO tracks(paymentId) VALUES(?) "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def InsertUserDiscount(userId, discountId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " INSERT INTO userDiscount(userId, discountId) VALUES (?, ?) "
    sql_query_data = (userId, discountId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def UpdateDiscountUsage(discountId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE discounts SET usages = usages + 1 WHERE id = ? "
    sql_query_data = (discountId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.lastrowid


def UpdateUserPrecartSize(size, userId, messageId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE precart SET size = ? WHERE userId = ? AND messageId = ? "
    sql_query_data = (size, userId, messageId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def UpdateUserPrecartQuantity(quantity, userId, messageId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE precart SET quantity = ? WHERE userId = ? AND messageId = ? "
    sql_query_data = (quantity, userId, messageId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def UpdateReceiptStatus(paymentId, status):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE receipts SET status = ? WHERE paymentId = ? "
    sql_query_data = (status, paymentId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def UpdateNotify(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE notifications SET notify = 1 WHERE paymentId = ? "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def UpdateTrack(paymentId, code):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " UPDATE tracks SET code = ? WHERE paymentId = ? "
    sql_query_data = (code,paymentId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def DeleteUserCart(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " DELETE FROM cart WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def DeleteUserPrecart(userId, messageId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " DELETE FROM precart WHERE userId = ? AND messageId = ? "
    sql_query_data = (userId, messageId)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def DeleteReceipt(paymentId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " DELETE FROM receipts WHERE paymentId = ? "
    sql_query_data = (paymentId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def DeleteUserDiscount(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " DELETE FROM userDiscount WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()


def DeleteUserPaymentInfo(userId):
    sql_connection = sqlite3.connect(db)
    sql_cursor = sql_connection.cursor()
    sql_query = " DELETE FROM paymentInfo WHERE userId = ? "
    sql_query_data = (userId,)
    sql_cursor.execute(sql_query, sql_query_data)
    sql_connection.commit()
    return sql_cursor.fetchall()