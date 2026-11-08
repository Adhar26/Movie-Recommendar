import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QFrame)
from PySide6.QtCore import Qt, QThread, Signal
from app.core.service import RecommenderService


class MovieCard(QFrame):
    def __init__(self, movie, on_rate):
        super().__init__()
        self.setFixedSize(190, 240)
        self.setStyleSheet("QFrame{background:#1f1f1f; border-radius:8px;} QLabel{color:white;}")
        layout = QVBoxLayout(self)

        title = QLabel(movie["title"])
        title.setWordWrap(True)
        title.setStyleSheet("font-weight:bold; font-size:14px;")
        genres = QLabel((movie["genres"] or "").replace("|", " - "))
        genres.setWordWrap(True)
        genres.setStyleSheet("color:#aaaaaa; font-size:11px;")
        layout.addWidget(title)
        layout.addWidget(genres)
        layout.addStretch()

        row = QHBoxLayout()
        for s in range(1, 6):
            b = QPushButton(str(s))
            b.setFixedWidth(28)
            b.clicked.connect(lambda checked=False, s=s: on_rate(movie["id"], s))
            row.addWidget(b)
        layout.addLayout(row)


class RetrainWorker(QThread):
    done = Signal()

    def __init__(self, svc):
        super().__init__()
        self.svc = svc

    def run(self):
        self.svc.refresh()
        self.done.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recommender")
        self.resize(1000, 420)
        self.setStyleSheet("QMainWindow{background:#141414;} QLabel{color:white;}")
        self.svc = RecommenderService()

        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)

        top = QHBoxLayout()
        self.user_box = QLineEdit("1")
        self.user_box.setFixedWidth(60)
        load_btn = QPushButton("Load")
        load_btn.clicked.connect(self.load_recs)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search movies...")
        self.search_box.returnPressed.connect(self.search)
        retrain_btn = QPushButton("Retrain")
        retrain_btn.clicked.connect(self.retrain)
        for w in (QLabel("User ID:"), self.user_box, load_btn, self.search_box, retrain_btn):
            top.addWidget(w)
        main.addLayout(top)

        self.row_title = QLabel("")
        self.row_title.setStyleSheet("font-size:18px; font-weight:bold;")
        main.addWidget(self.row_title)

        self.row_layout = QHBoxLayout()
        holder = QWidget()
        holder.setLayout(self.row_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(holder)
        main.addWidget(scroll)

        self.status = QLabel("")
        main.addWidget(self.status)
        self.load_recs()

    def user_id(self):
        return int(self.user_box.text())

    def show_row(self, title, movies):
        self.row_title.setText(title)
        while self.row_layout.count():
            item = self.row_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for m in movies:
            self.row_layout.addWidget(MovieCard(m, self.rate))
        self.row_layout.addStretch()

    def load_recs(self):
        self.show_row("Recommended for you", self.svc.get_recommendations(self.user_id(), 20))

    def search(self):
        q = self.search_box.text().strip()
        if q:
            self.show_row(f"Results for '{q}'", self.svc.search_movies(q, 20))

    def rate(self, movie_id, rating):
        self.svc.rate_movie(self.user_id(), movie_id, rating)
        self.status.setText(f"Saved {rating} stars. Click Retrain to update recommendations.")

    def retrain(self):
        self.status.setText("Retraining in background...")
        self.worker = RetrainWorker(self.svc)
        self.worker.done.connect(self.on_retrained)
        self.worker.start()

    def on_retrained(self):
        self.load_recs()
        self.status.setText("Recommendations updated.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
