from .pane import Pane
from item import Item

class Log(Pane):
    def __init__(self):
        super(Log, self).__init__(0, 10)
        self.line_length = 60
        self.scroll_y = 0
        self.lines = []
        self.last_message = ''
        self.last_message_idx = 0
        self.shown = False
        self.show_last_message = True

    def apply_on(self, display):
        super().apply_on(display)
        left = self.x + 2

        title = 'Message log'
        display[1][left:left+len(title)] = list(title)

        if len(self.lines) == 0:
            return

        for idx, line in enumerate(self.lines):
            if not (self.scroll_y <= idx < self.scroll_y+self.h-4):
                continue
            line = f'{idx+1}: {line}'
            if len(line) > self.line_length:
                line = line[:self.line_length-2] + '..'
            else:
                line = line[:self.line_length]
            display[2+idx-self.scroll_y][left:left+len(line)] = list(line)

        # if self.scroll_y > 0: # more above
        #     if len(self.text.split('\n')) > self.scroll_y + self.h-4: # more below
        #         text = '      -^- more -v-'
        #     else:
        #         text = '      -^- more ---'
        # elif len(self.text.split('\n')) > self.scroll_y + self.h-4: # more below
        #     text = '      --- more -v-'
        # else:
        #     text = ''
        # display[self.h-2][left:left+len(text)] = list(text)

        text = 'Press [l] to close.'
        display[self.h-2][left:left+len(text)] = list(text)
        
    def recv_key(self, key):
        if key == 'l':
            self.shown = False
            self.reset_scroll()
        elif key == 'down':
            self.scroll_y = min(max(0, len(self.lines) - self.h + 4), self.scroll_y + 1)
        elif key == 'up':
            self.scroll_y = max(0, self.scroll_y-1)

    def add_message(self, *messages):
        self.show_last_message = True
        message = ' '.join(str(message).strip() for message in messages)
        # for message in messages:
        message = str(message).strip()
        self.last_message = message
        # TODO add a "store" flag to messages
        if [s for s in ['{', 'cancelled', 'You see'] if s in message]:
            return
        self.lines.append(message)
        self.reset_scroll()

    def get_last_message(self):
        if self.show_last_message:
            idx = self.last_message_idx
            self.last_message_idx = len(self.lines) - 1
            messages = self.lines[idx+1:]
            if self.last_message not in self.lines: # HACK display unstored messages
                messages.append(self.last_message)
            return ' '.join(messages)
        else:
            return ''


    def hide_last_message(self):
        self.show_last_message = False

    def reset_scroll(self):
        self.scroll_y = max(0, len(self.lines) - self.h+4)
