from PyQt6.QtWidgets import(
	QApplication,
	QMainWindow,
	QTableWidget,
	QTableWidgetItem,
	QMessageBox,
	QInputDialog,
	QToolBar,
	QHeaderView,
)

from PyQt6.QtGui import(
	QAction,
)

from PyQt6.QtCore import(
	Qt,
)

class Main_window(QMainWindow):

	def __init__(self):
		super().__init__()

		self.table = QTableWidget()
		self.toolbar = QToolBar()

		self.setCentralWidget(self.table)
		self.addToolBar(self.toolbar)

		self.setup_toolbar()
		self.setup_table()

		self.load_data()

	def __deinit__(self):
		self.store_data()
		pass

	def load_data(self):
		pass

	def store_data(self):
		pass

	def setup_table(self):
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["Name", "Points", "Balance"])
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

	def setup_toolbar(self):
		self.insert_record_action = QAction("Insert Record")
		self.withdraw_action = QAction("Withdraw")
		self.transfer_action = QAction("Transfer")

		self.insert_record_action.triggered.connect(self.on_insert_record_clicked)
		self.withdraw_action.triggered.connect(self.on_withdraw_clicked)
		self.transfer_action.triggered.connect(self.on_transfer_clicked)

		self.toolbar.addActions([self.insert_record_action, self.withdraw_action, self.transfer_action])
	
	def on_insert_record_clicked(self):
		input_dialog = QInputDialog()
		(name, name_ok) = input_dialog.getText(self, "Insert Record", "Name")

		if not name_ok:
			return

		if len(name) == 0:
			msg_box = QMessageBox(self)
			msg_box.setText("Name cannot be empty")
			msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
			msg_box.setIcon(QMessageBox.Icon.Critical)
			msg_box.show()
			return

		(points, points_ok) = input_dialog.getDouble(self, "Insert Record", "Default Points for " + name)

		if not points_ok:
			return

		(balance, balance_ok) = input_dialog.getDouble(self, "Insert Record", "Default Balance of " + name)

		if not balance_ok:
			return

		self.table.insertRow(self.table.rowCount())

		name_item = QTableWidgetItem(name)
		points_item = QTableWidgetItem(str(points))
		balance_item = QTableWidgetItem(str(balance))

		for item in [name_item, points_item, balance_item]:
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

		self.table.setItem(self.table.rowCount() - 1, 0, name_item)
		self.table.setItem(self.table.rowCount() - 1, 1, points_item)
		self.table.setItem(self.table.rowCount() - 1, 2, balance_item)

	def on_withdraw_clicked(self):
		pass

	def on_transfer_clicked(self):
		pass

def main():
	app = QApplication([])
	window = Main_window()
	window.show()
	app.exec()

if __name__ == '__main__':
	main()
