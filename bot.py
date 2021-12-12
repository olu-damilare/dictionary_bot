import os

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from diction import get_info

telegram_bot_token = 'TELEGRAM_BOT_TOKEN'

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there. Provide any English word and I will give you a bunch "
                                                   "of information about it.")


# obtain the information of the word provided and format before presenting.
def get_word_info(update, context):
    # get the word info
    word_info = get_info(update.message.text)

    # If an invalid English word was provided by the user, return the custom response from get_info() and exit the
    # function
    if word_info.__class__ is str:
        update.message.reply_text(word_info)
        return

    # extract the word the user provided
    word = word_info['word']

    # extract the origin of the word
    origin = word_info['origin']
    meanings = '\n'

    synonyms = ''
    definition = ''
    example = ''
    antonyms = ''

    # a word may have several meanings. We'll use this counter to track each of the meanings provided from the response
    meaning_counter = 1

    for word_meaning in word_info['meanings']:
        meanings += 'Meaning ' + str(meaning_counter) + ':\n'

        for word_definition in word_meaning['definitions']:
            # extract the each of the definitions of the word
            definition = word_definition['definition']

            # extract each example for the respective definition
            if 'example' in word_definition:
                example = word_definition['example']

            # extract the collection of synonyms for the word based on the definition
            for word_synonym in word_definition['synonyms']:
                synonyms += word_synonym + ', '

            # extract the antonyms of the word based on the definition
            for word_antonym in word_definition['antonyms']:
                antonyms += word_antonym + ', '

        meanings += 'Definition: ' + definition + '\n\n'
        meanings += 'Example: ' + example + '\n\n'
        meanings += 'Synonym: ' + synonyms + '\n\n'
        meanings += 'Antonym: ' + antonyms + '\n\n\n'

        meaning_counter += 1

    # format the data into a string
    message = f"Word: {word}\n\nOrigin: {origin}\n{meanings}"

    update.message.reply_text(message)


# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://dictionary-bot1.herokuapp.com/' + telegram_bot_token
                      )
