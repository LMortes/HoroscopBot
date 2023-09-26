import asyncio
import datetime

import aiomysql
import os
from dotenv import load_dotenv
load_dotenv()
loop = asyncio.get_event_loop()
async def connection(loop):
    try:
        # global conn
        conn = await aiomysql.connect(
            host=os.getenv('MSQL_HOST'),
            user=os.getenv('MSQL_USER'),
            password=os.getenv('MSQL_PASSWORD'),
            db=os.getenv('MSQL_DB'),
            loop=loop,
            charset='utf8mb4',
            autocommit=True
        )
        # print('Connect to MYSQL DB succesfull!')
        return conn
    except Exception as er:
        print('Error in connection to MYSQL DB: ', er)


async def user_exists(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT id FROM users WHERE user_id = %s', user_id)
        await con.commit()
        if cur.rowcount > 0:
            return True
        else:
            return False


async def add_user(user_id, referal_link=None):
    con = await connection(loop)
    async with con.cursor() as cur:
        current_date = datetime.datetime.now()
        formatted_current_datetime = current_date.strftime('%Y-%m-%d %H:%M:%S')
        if referal_link != None:
            await cur.execute('INSERT INTO `users`(`user_id`, `active`, `referal_link`,`registration_date`)\
                                            VALUES (%s,%s,%s,%s)', (user_id, 1, referal_link, formatted_current_datetime))
        else:
            await cur.execute('INSERT INTO `users`(`user_id`, `active`, `registration_date`)\
                                            VALUES (%s,%s,%s)', (user_id, 1, formatted_current_datetime))
        await con.commit()


async def add_unique_user(name_link):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('UPDATE `referals_links` SET unique_users = unique_users + 1, users = users + 1 WHERE name_link = %s', name_link)
        await con.commit()

# ------------------------------ ADMIN MAILING -------------------------------------
async def check_table_for_sender(table_name):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s)', (table_name,))
        await con.commit()
        result = await cur.fetchone()
        return result[0]

async def create_table_for_sender(table_name):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute(f'CREATE TABLE `db_horo`.{table_name} ( `user_id` BIGINT(255) NOT NULL , `status` VARCHAR(255) NULL , `description` VARCHAR(255) NULL , PRIMARY KEY (`user_id`)) ENGINE = InnoDB;')
        await cur.execute(f'INSERT INTO {table_name}(`user_id`, `status`, `description`) SELECT `user_id`, %s, NULL FROM users', 'waiting')
        await con.commit()

async def delete_table_after_sender(table_name):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute(f'DROP TABLE {table_name}')
        await con.commit()

async def get_users_for_sender(table_name):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute(f'SELECT user_id FROM {table_name} WHERE status = %s', 'waiting')
        await con.commit()
        result_users = await cur.fetchall()
        if cur.rowcount > 0:
            return result_users
        else:
            return False

async def change_active_user(user_id, active, table_name, status, desc):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('UPDATE `users` SET `active` = %s WHERE user_id = %s', (active, user_id))
        await cur.execute(f'UPDATE {table_name} SET `status` = %s, `description` = %s WHERE user_id = %s', (status, desc, user_id))
        await con.commit()

async def change_active_user_if_dont_active(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('UPDATE `users` SET `active` = 1 WHERE user_id = %s AND active = 0', user_id)
        await con.commit()


# --------------------------- ADMIN STATISTICS ---------------------------------------

async def get_count_users():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users')
        await con.commit()
        count_users = await cur.fetchone()
        return count_users[0]


async def get_count_dead_users():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE active = 0')
        await con.commit()
        if cur.rowcount > 0:
            count_dead_users = await cur.fetchone()
            return count_dead_users[0]
        else:
            return 0


async def get_count_alive_users():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE active = 1')
        await con.commit()
        if cur.rowcount > 0:
            count_alive_users = await cur.fetchone()
            return count_alive_users[0]
        else:
            return 0


async def get_count_random_users():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE referal_link IS NULL')
        await con.commit()
        if cur.rowcount > 0:
            count_random_users = await cur.fetchone()
            return count_random_users[0]
        else:
            return 0


async def get_referal_link_names():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT name_link FROM referals_links')
        await con.commit()
        if cur.rowcount > 0:
            names_links = await cur.fetchall()
            names = []
            for name in names_links:
                names.append(name[0])
            return names
        else:
            return False

# -------------------------------------- OP ------------------------------------
async def get_channels_op():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM channels_op')
        await con.commit()
        channels = await cur.fetchall()
    return channels


async def delete_channel_op(channel_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('DELETE FROM channels_op WHERE id = %s', channel_id)
        await con.commit()


async def add_channel_op(channel_info):
    con = await connection(loop)
    channel_info[0] = channel_info[0].replace(" ", "")
    channel_info[2] = channel_info[2].replace(" ", "")
    async with con.cursor() as cur:
        await cur.execute('INSERT INTO `channels_op`(`chan_name`, `chan_id`, `chan_link`) VALUES (%s, %s, %s)', (channel_info[0], channel_info[1], channel_info[2]))
        await con.commit()


# ------------------------------- ADMIN REFERAL ----------------------------------
async def get_referal_link_info():
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM referals_links')
        await con.commit()
        if cur.rowcount > 0:
            ref_links_info = await cur.fetchall()
            return ref_links_info
        else:
            return False


async def get_referal_link_info_by_id(ref_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT * FROM referals_links WHERE id = %s', ref_id)
        await con.commit()
        ref_info = await cur.fetchall()
        return ref_info[0]


async def get_ref_users_alive(name_link):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE active = 1 AND referal_link = %s', name_link)
        await con.commit()
        if cur.rowcount > 0:
            count_users = await cur.fetchone()
            return count_users[0]
        else:
            return 0

async def get_ref_users_op(name_link):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE subscribed_op = 1 AND referal_link = %s', name_link)
        await con.commit()
        if cur.rowcount > 0:
            count_ref_op_users = await cur.fetchone()
            return count_ref_op_users[0]
        else:
            return 0

async def get_unique_users_hour_and_day(name_link):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT COUNT(id) FROM users WHERE registration_date >= NOW() - INTERVAL 1 HOUR AND referal_link = %s', name_link)
        if cur.rowcount > 0:
            row = await cur.fetchone()
            count_hour = row[0]
        else:
            count_hour = 0
        await cur.execute('SELECT COUNT(id) FROM users WHERE registration_date >= NOW() - INTERVAL 24 HOUR AND referal_link = %s', name_link)
        if cur.rowcount > 0:
            row = await cur.fetchone()
            count_day = row[0]
        else:
            count_day = 0
        await con.commit()
    return count_hour, count_day

async def delete_referal_link(ref_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('DELETE FROM referals_links WHERE id = %s', ref_id)
        await con.commit()

async def add_referal_link(name_link):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('INSERT INTO `referals_links`(`name_link`) VALUES (%s)', name_link)
        await con.commit()



# --------------------------- CHANNELS_OP ------------------------------

async def get_subscribed_op(user_id):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('SELECT subscribed_op FROM users WHERE user_id = %s', user_id)
        await con.commit()
        is_subscribed = await cur.fetchone()
        return is_subscribed[0]


async def change_subscribed_op(user_id, subscribed):
    con = await connection(loop)
    async with con.cursor() as cur:
        await cur.execute('UPDATE `users` SET `subscribed_op` = %s WHERE user_id = %s', (subscribed, user_id))
        await con.commit()


