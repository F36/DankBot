from telegram.ext.dispatcher import run_async

from .drake import drake
from .helpers import \
	helper_b, helper_gif, helper_image, \
	helper_text, helper_fry, helper_generate, helper_despacito
from .utils.text import commands, cookbook, chars, vapourtext


@run_async
def start_handler(bot, update):
	update.message.reply_markdown('*This is DankBot!*\n' + commands, quote=True)


@run_async
def help_handler(bot, update):
	update.message.reply_markdown(commands, quote=True)


@run_async
def cookbook_handler(bot, update):
	update.message.reply_markdown(cookbook, quote=True)


@run_async
def alt_handler(bot, update):
	text = update.message.text[4:].lower()
	result, upper = [update.message.from_user.first_name, ':'], False
	for i in text:
		if i.lower() in chars:
			result.append(i.upper() if upper else i.lower())
			upper = not upper
		else:
			result.append(i)
	if update.message.reply_text("".join(result), quote=True):
		update.message.delete()


@run_async
def vapourize_handler(bot, update):
	text = update.message.text[10:]
	result = [update.message.from_user.first_name, ': ']
	for i in text:
		if i in vapourtext:
			result.append(vapourtext[i])
		else:
			result.append(i)
	if update.message.reply_text("".join(result)):
		update.message.delete()


@run_async
def reply_handler(bot, update):
	if helper_fry(bot, update):
		return

	if helper_generate(bot, update):
		return

	main_handler(bot, update)


@run_async
def main_handler(bot, update):
	textn = update.message.text
	text = textn.lower()
	words = text.split()

	if ', not ' in text:
		drake(
			update,
			textn[text.find(', not ') + 6:],
			textn[:text.find(', not ')]
		)

	elif '🅱️' in text:
		helper_b(update, text)

	elif 'dankbot play despacito' in text or 'alexa play despacito' in text:
		helper_despacito(update, text)

	elif helper_gif(update, text, words):
		return

	elif helper_image(update, text, words):
		return

	elif helper_text(update, text, words):
		return

	else:
		print(
			'(%s) %s: %s' % (
				update.message.chat.title,
				update.message.from_user.first_name,
				textn
			)
			if update.message.chat.type == 'group' else
			'%s: %s' % (update.message.from_user.first_name, textn)
		)


@run_async
def all_handler(bot, update):
	print(update.message)
	if update.message.chat.id != 623912829:
		return

	update.message.reply_text(
		update.message.animation.file_id if update.message.animation
		else update.message.audio.file_id if update.message.audio
		else update.message.document.file_id if update.message.document
		else update.message.photo[::-1][0].file_id if update.message.photo
		else update.message.video.file_id if update.message.video
		else update.message.video_note.file_id if update.message.video_note
		else update.message.voice.file_id if update.message.voice
		else update.message,
		quote=True)
