import re

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.inline_code_format = QTextCharFormat()
        self.inline_code_format.setForeground(QColor("#D14"))
        self.inline_code_format.setFontFamily("Courier")

        self.bold_format = QTextCharFormat()
        self.bold_format.setFontWeight(QFont.Bold)

        self.italic_format = QTextCharFormat()
        self.italic_format.setFontItalic(True)

        self.header_format = QTextCharFormat()
        self.header_format.setForeground(QColor("#6C63FF"))
        self.header_format.setFontWeight(QFont.Bold)

        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor("#7EAAFF"))

        self.code_block_format = QTextCharFormat()
        self.code_block_format.setForeground(QColor("#007F00"))
        self.code_block_format.setFontFamily("Courier")

        self.quote_format = QTextCharFormat()
        self.quote_format.setForeground(QColor("#888888"))
        self.quote_format.setFontItalic(True)

        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#5555AA"))

        self.todo_format = QTextCharFormat()
        self.todo_format.setForeground(QColor("#FFA500"))
        self.todo_format.setFontWeight(QFont.Bold)

        self.tag_format = QTextCharFormat()
        self.tag_format.setForeground(QColor("#B266FF"))

        self.mention_format = QTextCharFormat()
        self.mention_format.setForeground(QColor("#3399FF"))

        self.hr_format = QTextCharFormat()
        self.hr_format.setForeground(QColor("#999999"))

        self.inline_rules = [
            (re.compile(r'^#{1,6}\s+.*$'), self.header_format),
            (re.compile(r'^>\s+.*$'), self.quote_format),
            (re.compile(r'^[-*]\s+.*$'), self.list_format),
            (re.compile(r'\b(TODO|FIXME|NOTE)\b'), self.todo_format),
            (re.compile(r'#\w+'), self.tag_format),
            (re.compile(r'@\w+'), self.mention_format),
            (re.compile(r'^(\*\*\*|---)\s*$'), self.hr_format),
            (re.compile(r'\[(.*?)\]\((.*?)\)'), self.link_format),
            (re.compile(r'`([^`]+)`'), self.inline_code_format),
            (re.compile(r'\*\*(.+?)\*\*'), self.bold_format),
            (re.compile(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)'), self.italic_format),
        ]

        self.code_block_start = re.compile(r'^```.*$')
        self.code_block_end = re.compile(r'^```\s*$')

    def highlightBlock(self, text):
        if self.previousBlockState() == 1:
            self.setFormat(0, len(text), self.code_block_format)
            if self.code_block_end.match(text):
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(1)
            return

        if self.code_block_start.match(text):
            self.setFormat(0, len(text), self.code_block_format)
            self.setCurrentBlockState(1)
            return

        for pattern, fmt in self.inline_rules:
            for match in pattern.finditer(text):
                try:
                    start, end = match.span(1)
                except IndexError:
                    start, end = match.span(0)
                self.setFormat(start, end - start, fmt)

        self.setCurrentBlockState(0)
