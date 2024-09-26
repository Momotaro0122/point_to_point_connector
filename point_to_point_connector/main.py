'''
Point to point connector.
Description:Dyn constraint verts by verts base on user selected.
Show: None
Author: Martin Lee
Created: 09 May 2023
Last Updated: 09 May 2023 - Martin Lee
Usuage -
--import func--
import point_to_point_connector.main as ppc
reload(ppc)
ppc.main()
'''

import point_to_point_ui
reload(point_to_point_ui)

from point_to_point_ui import PointToPointConstraintUI, maya_main_window


def main():
    window = PointToPointConstraintUI(maya_main_window())
    window.show()


if __name__ == "__main__":
    main()

