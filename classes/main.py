'''
Created on Mar 25, 2015

@author: Liyan Xu; Hongmou Zhang

Adapted and redeveloped from the original WolongABM Visual Basic program;
by Liyan Xu, Yansheng Yang, Hong You, and Hailong Li;
with major improvements.

'''
import sys
 
from PyQt4 import QtCore, QtGui

import main_submodules


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
      
    main_window = QtGui.QMainWindow()
  
    main = main_submodules.Ui_frm_SEEMS_main()
    main.setupUi(main_window)
      
    main_window.show()
  
    sys.exit(app.exec_())


'''
How come the following codes different from the above lines?
'''

# if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#            
#     main_window = QtGui.QMainWindow()
#        
#     main_submodules.Ui_frm_SEEMS_main().setupUi(main_window)
#            
#     main_window.show()
#        
#     sys.exit(app.exec_())
