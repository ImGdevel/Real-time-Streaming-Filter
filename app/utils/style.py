from .colors import Colors
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QIcon, QPixmap

class Style:
    #Title Bar Colors
    
    def shadow(target):
        shadow_effect = QGraphicsDropShadowEffect(target)
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)
        return shadow_effect
        
    # 이미지 크기를 조정할 함수
    def resize_icon(icon_path, width, height):
        pixmap = QPixmap(icon_path)
        resized_pixmap = pixmap.scaled(width, height)
        return QIcon(resized_pixmap)
    
    title_bar_style = f"""
            background-color: {Colors.base_color_03};
            color: {Colors.textColor01};
            font-size: 16px;
            padding: 10px;
            border-radius: 0px;  
            
    """
    
    title_bar_button = f"""
            QPushButton {{
                background-color: {Colors.base_color_03};
                font-size: 18px;
                border-radius: 5px;  
                border: none;
                margin-right: 5px;
            }}
            QPushButton:hover {{
                background-color: {Colors.base_color_06};
            }}
        """

    push_button = f"""
        QPushButton {{
    	    background-position: left center;
            background-repeat: no-repeat;
    	    border: none;
    	    border-left: 22px solid transparent;
    	    background-color:transparent;
    	    text-align: left;
    	    padding-left: 44px;
        }}
        
        QPushButton:hover{{
    	    background-color: rgb(40, 44, 52);\n"
        }}
        
        QPushButton:pressed {{
        background-color: rgb(189, 147, 249);
    	color: rgb(255, 255, 255);
        }}
    """
    
    
    
    
    frame_style = f"""
        background-color: {Colors.base_color_06};
        color: white;
        border-radius: 5px;
        padding: 0px;
    """
    
    frame_style_background = f"""
        background-color: {Colors.base_color_04};
        color: white;
        border-radius: 5px;
        padding: 0px;
    """
    
    frame_style_line = f"""
        background-color: {Colors.base_color_06};
        color: white;
        border: 1px solid #222222;
        border-radius: 5px;
        padding: 0px;
    """
    
    dialog_style = f"""

        background-color: {Colors.base_color_04};
        border: 1px solid {Colors.base_color_07};
        color: white;
        border-radius: 0px;  
        padding: 0px;
    """
    
    frame_style_none_line = f"""
        background-color: {Colors.base_color_06};
        border-radius: 5px;  
        border: none;
        margin: 0px;
        padding: 5px;
    """
    
    
    frame_inner_style = f"""
        background-color: {Colors.base_color_03};
        padding: 5px;

    """
    
    mini_button_style = f"""
        QPushButton {{
            background-color: {Colors.base_color_06};
            border: 2px solid {Colors.base_color_04};
            border-radius: 5px;
            font-size: 15px;
            padding: 0px;
        }}
        
        QPushButton:hover {{
            background-color: {Colors.base_color_07}; 
            border: 2px solid {Colors.base_color_08};
        }}

        QPushButton:pressed {{
            background-color: {Colors.base_color_04};
        }}
    """
    
    line_edit_style = f"""
        QLineEdit {{
            background-color: {Colors.base_color_04};
            border-radius: 5px;
            border: 2px solid {Colors.base_color_04};
            padding-left: 10px;
            selection-color: rgb(255, 255, 255);
            selection-background-color: rgb(255, 121, 198);
        }}
        QLineEdit:hover {{
            border: 2px solid rgb(64, 71, 88);
        }}
        QLineEdit:focus {{
            border: 2px solid rgb(91, 101, 124);
        }}
    """
    
    
    list_button_style = f"""
        QPushButton {{
            background-color: {Colors.base_color_06};
            border: 2px solid {Colors.base_color_04};
            border-radius: 5px;
            text-align: center;
            font-size: 16px;
        }}

        QPushButton:hover {{
            background-color: {Colors.base_color_07}; 
            border: 2px solid {Colors.base_color_08};
        }}

        QPushButton:pressed {{
            background-color: {Colors.base_color_04};
        }}

        QPushButton:focus {{
            outline: none;
        }}

        QPushButton:checked {{
            background-color: {Colors.identity_color_05};
        }}

    """
    
    list_button_style_none_line = f"""
        QPushButton {{
            background-color: {Colors.base_color_06};
            border: none;
            border-radius: 5px;
            text-align: left;
            padding-left: 10px;
            font-size: 16px;
        }}

        QPushButton:hover {{
            background-color: {Colors.base_color_07}; 
            border: none;
        }}

        QPushButton:pressed {{
            background-color: {Colors.base_color_04};
        }}

    """

    list_widget_style = f"""
        background-color: {Colors.base_color_03};
        border-radius: 5px;
        border-left: 3px solid {Colors.base_color_01};
        border-top: 3px solid {Colors.base_color_01};
        padding: 0px;
    """

    list_frame_style = f"""
        background-color: {Colors.base_color_06};
        border-radius: 5px;
        padding: 10px 20px;
    """
    
    list_frame_label = f"""
        color: white; 
        font-size: 18px; 
        font-weight: bold; 
        padding: 5px 10px;
    """

    title_label = f"""
        font-weight: bold; 
        font-size: 20px;
        border: none;
    """
    
    title_label_middle = f"""
        font-weight: bold; 
        font-size: 16px;
        border: none;
    """



    setting_list_button_style = f"""
        QWidget{{
            background-color: {Colors.base_color_06};
            border: 2px solid {Colors.base_color_03};
            border-radius: 0px;
            padding: 0px;
            margin: 0px;
        }}

        QPushButton {{
            background-color: {Colors.base_color_06};
            border: 2px solid {Colors.base_color_03};
            border-top: 2px solid {Colors.base_color_F};
            padding: 5px;
            margin: 0px;
            border-radius: 0px;
            text-align: left;
            font-size: 16px;
        }}

        QPushButton:hover {{
            background-color: {Colors.base_color_07}; 
            border: 2px solid {Colors.base_color_08};
        }}
        
        QPushButton:checked::hover {{
            background-color: {Colors.base_color_04};
            border: 2px solid {Colors.base_color_03};
            border-top: 2px solid {Colors.base_color_F};
        }}
    

        QPushButton:checked {{
            background-color: {Colors.base_color_04};
        }}

    """
    
    
    cam_button = f"""
        QPushButton {{
            background-color: {Colors.base_color_05};
            border: none;
            border-radius: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-size: 15px;
            padding: 0px;
        }}
        QPushButton:hover {{
            background-color: {Colors.base_color_07};
        }}
        
    """
    
    cam_button_selected = f"""
        QPushButton {{
            background-color: {Colors.base_color_06};
            border: none;
            border-radius: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-size: 15px;
            padding: 0px;
        }}
    """
    
    slider = f"""
    QSlider::groove:horizontal {{
        
        border-radius: 5px;
        height: 10px;
    	margin: 0px;
    	background-color: rgb(52, 59, 72);
    }}
    QSlider::groove:horizontal:hover {{
    	background-color: rgb(55, 62, 76);
    }}
    QSlider::handle:horizontal {{
        background-color: rgb(100, 181, 246);
        border: none;
        height: 10px;
        width: 10px;
        margin: 0px;
    	border-radius: 5px;
    }}
    QSlider::handle:horizontal:hover {{
        background-color: rgb(21, 101, 192);
    }}
    QSlider::handle:horizontal:pressed {{
        background-color: rgb(13, 71, 161);
    }}

    QSlider::groove:vertical {{
        border-radius: 5px;
        width: 10px;
        margin: 0px;
    	background-color: rgb(52, 59, 72);
    }}
    QSlider::groove:vertical:hover {{
    	background-color: rgb(55, 62, 76);
    }}
    QSlider::handle:vertical {{
        background-color: rgb(100, 181, 246);
    	border: none;
        height: 10px;
        width: 10px;
        margin: 0px;
    	border-radius: 5px;
    }}
    QSlider::handle:vertical:hover {{
        background-color: rgb(21, 101, 192);
    }}
    QSlider::handle:vertical:pressed {{
        background-color: rgb(13, 71, 161)
    }}

    """