import sys
import os
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import *

BOOKMARKS_FILE = 'bookmarks.json'

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.setGeometry(300, 150, 1200, 800)

        self.bookmarks = self.load_bookmarks()

        # Crearea widgetului QTabWidget pentru taburi
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tabs)

        # Crearea barei de instrumente
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Buton pentru a merge înapoi
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.navigate_back)
        navbar.addAction(back_btn)

        # Buton pentru a merge înainte
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.navigate_forward)
        navbar.addAction(forward_btn)

        # Buton pentru reîncărcare pagină
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.reload_page)
        navbar.addAction(reload_btn)

        # Buton pentru a deschide un nou tab
        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(new_tab_btn)

        # Buton pentru a salva bookmarkul
        save_bookmark_btn = QAction('Save Bookmark', self)
        save_bookmark_btn.triggered.connect(self.save_bookmark)
        navbar.addAction(save_bookmark_btn)

        # Buton pentru a arăta bookmarkurile
        show_bookmarks_btn = QAction('Show Bookmarks', self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(show_bookmarks_btn)

        # Câmp pentru a introduce URL-ul
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Creare tab inițial
        self.add_new_tab(QUrl('https://www.google.com'), 'New Tab')

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl('https://www.google.com')

        # Crearea unui QWebEngineView pentru noul tab
        browser = CustomWebEngineView(self)
        browser.setUrl(qurl)

        # Adăugarea tabului nou
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Actualizarea câmpului URL când se schimbă pagina în noul tab
        browser.urlChanged.connect(lambda q: self.update_url_bar(q, browser))

    def add_new_window(self, qurl):
        # Creare fereastră nouă
        new_window = Browser()
        new_window.show()
        new_window.add_new_tab(qurl)

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.setUrl(QUrl(url))

    def update_url_bar(self, q, browser=None):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(q.toString())

    def navigate_back(self):
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            if current_browser.history().canGoBack():
                current_browser.back()

    def navigate_forward(self):
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            if current_browser.history().canGoForward():
                current_browser.forward()

    def reload_page(self):
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.reload()

    def save_bookmark(self):
        url = self.tabs.currentWidget().url().toString()
        if url:
            name, ok = QInputDialog.getText(self, "Save Bookmark", "Enter a name for the bookmark:")
            if ok and name:
                self.bookmarks[name] = url
                self.save_bookmarks()

    def show_bookmarks(self):
        if not self.bookmarks:
            QMessageBox.information(self, "Bookmarks", "No bookmarks saved.")
            return

        # Creare dialog pentru bookmarkuri
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        bookmarks_layout = QVBoxLayout()

        list_widget = QListWidget()
        for name, url in self.bookmarks.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, url)
            list_widget.addItem(item)

        list_widget.itemDoubleClicked.connect(self.open_bookmark)
        bookmarks_layout.addWidget(list_widget)
        bookmarks_dialog.setLayout(bookmarks_layout)
        bookmarks_dialog.exec_()

    def open_bookmark(self, item):
        url = item.data(Qt.UserRole)
        if url:
            current_browser = self.tabs.currentWidget()
            if isinstance(current_browser, QWebEngineView):
                current_browser.setUrl(QUrl(url))
            else:
                self.add_new_tab(QUrl(url), item.text())

    def view_page_source(self, html):
        # Creare tab pentru sursa paginii
        text_edit = QTextEdit()
        text_edit.setPlainText(html)  # Afișează sursa paginii în noul tab
        self.tabs.addTab(text_edit, "Page Source")
        self.tabs.setCurrentWidget(text_edit)

    def save_page_as(self, url):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "HTML Files (*.html);;All Files (*)")
        if file_name:
            page = self.tabs.currentWidget().page()
            page.toHtml(lambda html: self._save_to_file(file_name, html))

    def _save_to_file(self, file_name, html):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(html)

    def load_bookmarks(self):
        if os.path.exists(BOOKMARKS_FILE):
            with open(BOOKMARKS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_bookmarks(self):
        with open(BOOKMARKS_FILE, 'w') as f:
            json.dump(self.bookmarks, f, indent=4)


class CustomWebEngineView(QWebEngineView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def contextMenuEvent(self, event):
        page = self.page()
        hit_test_result = page.contextMenuData()

        menu = QMenu(self)

        # Opțiune pentru a deschide linkul într-un tab nou
        if hit_test_result.linkUrl().isValid():
            open_in_new_tab_action = QAction('Open in New Tab', self)
            open_in_new_tab_action.triggered.connect(lambda: self.main_window.add_new_tab(hit_test_result.linkUrl()))
            menu.addAction(open_in_new_tab_action)
            
            open_in_new_window_action = QAction('Open in New Window', self)
            open_in_new_window_action.triggered.connect(lambda: self.main_window.add_new_window(hit_test_result.linkUrl()))
            menu.addAction(open_in_new_window_action)

        # Opțiune pentru a vizualiza sursa paginii
        view_source_action = QAction('View Page Source', self)
        view_source_action.triggered.connect(self.view_page_source)
        menu.addAction(view_source_action)

        # Opțiune pentru a salva pagina
        save_page_action = QAction('Save Page As...', self)
        save_page_action.triggered.connect(lambda: self.main_window.save_page_as(self.main_window.tabs.currentWidget().url().toString()))
        menu.addAction(save_page_action)

        menu.exec_(event.globalPos())

    def view_page_source(self):
        # Obținerea sursei paginii și transmiterea către metoda view_page_source din fereastra principală
        self.page().toHtml(self.main_window.view_page_source)


app = QApplication(sys.argv)
QApplication.setApplicationName('Muap - Simple Browser')
window = Browser()
window.show()
sys.exit(app.exec_())
