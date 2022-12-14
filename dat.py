from PyQt6.QtWidgets import(
	QApplication,
	QMainWindow,
	QTableWidget,
	QTableWidgetItem,
	QMessageBox,
	QInputDialog,
	QToolBar,
	QHeaderView
)

from PyQt6.QtGui import(
	QAction
)

from PyQt6.QtCore import(
	Qt,
	QSettings,
)

class Main_window(QMainWindow):

	def __init__(self):
		super().__init__()

		self.table = QTableWidget(self)
		self.toolbar = QToolBar(self)

		self.setCentralWidget(self.table)
		self.addToolBar(self.toolbar)
		self.setup_toolbar()
		self.setup_table()
		self.load_data()

	def load_data(self):
		settings = QSettings("conat", "dat")
		settings.beginGroup("datum")

		for key in settings.allKeys():
			idxes = key.split('-')
			row = int(idxes[0])
			col = int(idxes[1])

			if row >= self.table.rowCount():
				self.table.setRowCount(row + 1)

			value = settings.value(key) if col == 0 else int(settings.value(key))

			item = QTableWidgetItem()
			item.setData(Qt.ItemDataRole.EditRole, value)
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

			self.table.setItem(row, col, item)

	def store_data(self):
		settings = QSettings("conat", "dat")
		settings.beginGroup("datum")
		settings.clear()

		for i in range(self.table.rowCount()):
			for j in range(self.table.columnCount()):
				settings.setValue(str(i) + '-' + str(j), self.table.item(i, j).text())

	def setup_table(self):
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["Name", "Points", "Balance"])
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
		self.table.setSortingEnabled(True)
		self.table.sortItems(1, Qt.SortOrder.DescendingOrder)

	def setup_toolbar(self):
		self.insert_record_action = QAction("Insert Record")
		self.withdraw_action = QAction("Withdraw")
		self.transfer_action = QAction("Transfer")
		self.delete_record_action = QAction("Delete Record")

		self.insert_record_action.triggered.connect(self.on_insert_record_clicked)
		self.withdraw_action.triggered.connect(self.on_withdraw_clicked)
		self.transfer_action.triggered.connect(self.on_transfer_clicked)
		self.delete_record_action.triggered.connect(self.on_delete_record_clicked)

		self.toolbar.addActions([self.insert_record_action, self.withdraw_action, self.transfer_action,
			self.delete_record_action])

	def on_delete_record_clicked(self):
		(row, row_ok) = QInputDialog().getInt(self, "Delete Record", "ID of record to delete:");

		if not row_ok:
			return

		if row <= 0 or row > self.table.rowCount():
			msg_box = QMessageBox(self)
			msg_box.setText("Invalid ID")
			msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
			msg_box.setIcon(QMessageBox.Icon.Critical)
			msg_box.exec()
			return self.on_delete_record_clicked()

		# todo: add confirmation
		self.table.removeRow(row - 1)
	
	def on_insert_record_clicked(self):
		input_dialog = QInputDialog(self)
		(name, name_ok) = input_dialog.getText(self, "Insert Record", "Name")

		if not name_ok:
			return

		if len(name) == 0:
			msg_box = QMessageBox(self)
			msg_box.setText("Name cannot be empty")
			msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
			msg_box.setIcon(QMessageBox.Icon.Critical)
			msg_box.exec()
			return self.on_insert_record_clicked()

		(points, points_ok) = input_dialog.getInt(self, "Insert Record", "Default Points for " + name)

		if not points_ok:
			return

		(balance, balance_ok) = input_dialog.getInt(self, "Insert Record", "Default Balance of " + name)

		if not balance_ok:
			return

		self.table.setSortingEnabled(False)
		self.table.insertRow(self.table.rowCount())

		name_item = QTableWidgetItem()
		points_item = QTableWidgetItem()
		balance_item = QTableWidgetItem()

		name_item.setData(Qt.ItemDataRole.EditRole, name)
		points_item.setData(Qt.ItemDataRole.EditRole, points)
		balance_item.setData(Qt.ItemDataRole.EditRole, balance)

		for item in [name_item, points_item, balance_item]:
			item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

		self.table.setItem(self.table.rowCount() - 1, 0, name_item)
		self.table.setItem(self.table.rowCount() - 1, 1, points_item)
		self.table.setItem(self.table.rowCount() - 1, 2, balance_item)

		self.table.setSortingEnabled(True)

	def on_withdraw_clicked(self):
		pass

	def on_transfer_clicked(self):
		pass

def main():
	app = QApplication([])
	window = Main_window()
	window.show()
	app.exec()
	window.store_data() # ugly, fix it somehow

if __name__ == '__main__':
	main()
