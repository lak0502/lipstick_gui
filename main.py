import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from db_connect import db, cursor

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('cms.ui', self)
    self.id = 0

    self.tb_lipstick.setColumnWidth(0, 50)
    self.tb_lipstick.setColumnWidth(1, 150)
    self.tb_lipstick.setColumnWidth(2, 150)
    self.tb_lipstick.setColumnWidth(3, 100)

    self.show_all_lipsticks()
    self.btn_add.clicked.connect(self.insert_lipstick)
    self.btn_search.clicked.connect(self.search_lipstick)
    self.btn_clear.clicked.connect(self.clear)
    self.btn_update.clicked.connect(self.update_lipstick)
    self.btn_delete.clicked.connect(self.delete_lipstick)
    self.tb_lipstick.cellClicked.connect(self.selected_row)

  def say_hi(self):
    QMessageBox.information(self, 'Information', 'Hello World!')

  def update_lipstick(self):
    price = int(self.txt_price.text())
    sql = 'update lipstick set price = ? where id = ?'
    values = (price, self.id)

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Update lipstick successful!')
      self.show_all_lipsticks()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to update lipstick!')
    self.clear()

  def delete_lipstick(self):
    sql = 'delete from lipstick where id = ?'
    values = (self.id, )

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Delete lipstick successful!')
      self.show_all_lipsticks()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to delete lipstick!')
    self.clear()

  def selected_row(self):
    row = self.tb_lipstick.currentRow()
    self.id = self.tb_lipstick.item(row, 0).text()
    self.txt_color.setText(self.tb_lipstick.item(row, 1).text())
    self.txt_Texture.setText(self.tb_lipstick.item(row, 2).text())
    self.txt_price.setText(self.tb_lipstick.item(row, 3).text())

    self.btn_update.setEnabled(True)
    self.btn_delete.setEnabled(True)
    self.btn_add.setEnabled(False)

    self.txt_color.setEnabled(False)
    self.txt_Texture.setEnabled(False)

  def search_lipstick(self):
    color = self.txt_search.text()
    # print(color)
    sql = 'select * from lipstick where color like ?'
    values = (f'%{color}%', )

    lipsticks = cursor.execute(sql, values).fetchall()
    self.show_lipsticks(lipsticks)

    self.txt_search.setText('')

  def show_all_lipsticks(self):
    sql = 'select * from lipstick'
    lipsticks = cursor.execute(sql).fetchall()

    self.show_lipsticks(lipsticks)

  def show_lipsticks(self, lipsticks):
      n = len(lipsticks)
      self.tb_lipstick.setRowCount(n)
      row = 0
      for lipstick in lipsticks:  #lipstick[0] => (1, 'Toyota', 'Yaris Cross', 2025, 867778)
        self.tb_lipstick.setItem(row, 0, QTableWidgetItem(str(lipstick[0])))
        self.tb_lipstick.setItem(row, 1, QTableWidgetItem(lipstick[1]))
        self.tb_lipstick.setItem(row, 2, QTableWidgetItem(lipstick[2]))
        self.tb_lipstick.setItem(row, 3, QTableWidgetItem(str(lipstick[3])))

        row += 1

  def insert_lipstick(self):
    color = self.txt_color.text()
    texture = self.txt_Texture.text()
    price = self.txt_price.text()

    sql = 'insert into lipstick(color, texture, price) values(?, ?, ?)'
    values = (color, texture, price)


    rs = cursor.execute(sql, values)
    db.commit()
    if rs.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Insert lipstick successful!')
      self.show_all_lipsticks()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to insert lipstick!')

    self.clear()

  def clear(self):
    self.txt_color.setText('')
    self.txt_Texture.setText('')
    self.txt_price.setText('')

    self.txt_color.setEnabled(True)
    self.txt_Texture.setEnabled(True)

    self.tb_lipstick.clearSelection()

    self.btn_add.setEnabled(True)
    self.btn_update.setEnabled(False)
    self.btn_delete.setEnabled(False)

    self.show_all_lipsticks()


  
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()