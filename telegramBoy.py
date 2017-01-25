#!/usr/bin/python
# -*- coding: utf-8 -*-
import telegram
import logging
import random
import requests

import randPorno
import diceRoll
import typeCheck
# from cleverbot import Cleverbot

import time
import re
import csv

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

updater = Updater(token='301986485:AAH07FYwuKuYFs-yycUYFQUSxlgDfrV8-yc')
dispatcher = updater.dispatcher


invalidSyntaxMessage = "I'm sorry, that didn't make sense to me."


def about(bot, update):
    print ('Sending Info')
    message = \
        """*Hi! My name's Teleboy! Here are some of the things I can do.*
*/echo:* Need to hear it from someone else? I'll echo whatever you put after '/echo'.

*/roll XdY:* Who doesn't love a good dice roller? Replace the 'x' and 'y' with the number of dice you're rolling, and the number of sides on them respectively.

*/flip:* Dice are lame. You know what's not lame? COINS!

*/timer:* Need a reminder for something that's not very important? Use this extremely unreliable timer! Type '/timer ', followed by the number of minutes you need, then an optional message.

*/porno:* I guess you'll just have to find out.

*/fmk:* Marry, fuck, kill. Type '/mfk', followed by three people separated by commas.

*/choose:* Chooses! Type '/choose'  followed by a bunch of choices separated by commas.

If you've got any questions or concerns, just shoot a message to good ol' @gingerfeld. He's my dad."""

    bot.sendMessage(parse_mode='Markdown',
                    chat_id=update.message.chat_id, text=message,
                    disable_web_page_preview=True)


about_handler = CommandHandler('about', about)


def echo(bot, update, args):
    print ('Echoing')
    bot.sendMessage(chat_id=update.message.chat_id, text=' '.join(args))
echo_handler = CommandHandler('echo', echo, pass_args=True)

def roll(bot, update, args):
    print ('Rolling')

    response = invalidSyntaxMessage

    
    text = ' '.join(args)
    dieSet = diceRoll.roll(text)

    if(dieSet):
        response = dieSet.analyzedRoll()
        if(response == False):
            response = invalidSyntaxMessage
    
    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='Markdown',
                    text=str(response))
roll_handler = CommandHandler('roll', roll, pass_args=True)


def flip(bot, update):
    print ('Flipping')
    response = diceRoll.flip()
    bot.sendMessage(chat_id=update.message.chat_id, text=response)


flip_handler = CommandHandler('flip', flip)

def porno(bot, update):
    response=randPorno.porno()
    bot.sendMessage(chat_id=update.message.chat_id, text=response,
                    disable_web_page_preview=True, parse_mode='Markdown')


porno_handler = CommandHandler('porno', porno)

timers = []


def timer(bot, update, args):
    print('Timing')
    confirmString = "Sorry, that doesn't make sense to me"
    numString = ' '.join(args)

    containsFloat = False

    potentialFloat = numString[0]
    numString = numString[1:]

    while (len(numString) >= 1) & typeCheck.isfloat(potentialFloat):
        potentialFloat += numString[0]
        numString = numString[1:]
        containsFloat = True

    if len(numString) != 0:
        numString = potentialFloat[-1] + numString
        potentialFloat = potentialFloat[:-1]
    if containsFloat:
        floatNum = float(potentialFloat)
        confirmString = 'Setting timer for ' + potentialFloat \
            + ' minutes. WARNING: This timer will currently NOT be stored in the likely event of a reboot.'
        timers.append([time.time() + floatNum * 60,
                      update.message.from_user.first_name,
                      update.message.chat_id, bot, numString])

    bot.sendMessage(chat_id=update.message.chat_id, text=confirmString)


timer_handler = CommandHandler('timer', timer, pass_args=True)


def fmk(bot, update, args):
    cantidates = ' '.join(args)
    parsedCantidates = cantidates.split(',')
    response = "Sorry, that doesn't make sense to me."

    if len(parsedCantidates) == 3:
        for index in range(3):
            randIndex = random.randint(0, 2)
            temp = parsedCantidates[index]
            parsedCantidates[index] = parsedCantidates[randIndex]
            parsedCantidates[randIndex] = temp
            response = 'Fuck: ' + parsedCantidates[0] + '\nMarry: ' \
                + parsedCantidates[1] + '\nKill: ' + parsedCantidates[2]
        else:
            print(parsedCantidates)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
fmk_handler = CommandHandler('fmk',fmk, pass_args = True)

def choose(bot, update, args):
    cantidates = ' '.join(args)
    parsedCantidates = cantidates.split(',')
    response = "Sorry, that doesn't make sense to me."

    if len(parsedCantidates) > 1:
        response = (parsedCantidates[random.randint(0,len(parsedCantidates)-1)])
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
choose_handler = CommandHandler('choose',choose, pass_args = True)

running = True
def stop(bot, update):
    print('Stopping')
    running = False
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Shutting down. You'd better be Daniel.")
    updater.stop()
stop_handler = CommandHandler('stop', stop)

dispatcher.add_handler(about_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(flip_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(timer_handler)
dispatcher.add_handler(porno_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(fmk_handler)
dispatcher.add_handler(choose_handler)

updater.start_polling(timeout=5)

while running:
    print("Checking timers" + str(time.time()))
    if len(timers) > 0:
        for i in timers:
            if i[0] < time.time():
                i[3].sendMessage(chat_id=i[2], text=i[1] + ': TIMER EXPIRED. \n' + i[4])
                timers.remove(i)
    time.sleep(0.5)
#updater.idle()

print('Shutting down...')
