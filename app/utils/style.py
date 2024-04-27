from .colors import Colors

class Style:
    #Title Bar Colors

    base_style01 = f'background-color: {Colors.baseColor02};'
    
    mini_button_style = f"""
    QPushButton {{
        background-color: {Colors.base_color_06};
        border-radius: 5px;  
    }}
    
    """
    
    list_button_style = f"""
    QPushButton {{
        background-color: {Colors.base_color_06};
        border-radius: 5px;
        border: none;
        text-align: center;
        font-size: 16px;
        margin-top: -2px;
    }}

    QPushButton:hover {{
        background-color: {Colors.base_color_05}; 
    }}

    QPushButton:pressed {{
        background-color: {Colors.base_color_04};
    }}

    QPushButton:focus {{
        outline: none;
    }}
    
    """

    list_widget_style = f"""
    background-color: {Colors.base_color_03};
    border-radius: 5px;
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

    menu_button_style = f"""
    QPushButton {{
        background-color: {Colors.buttonColor_01_base};
        border: 2px solid #000000;
        border-radius: 5px;
        color: white;
        padding: 10px 20px;
        text-align: center;
    }}
    QPushButton:hover {{
        background-color: {Colors.buttonColor_01_hover}; /* 마우스 오버시 배경색 변경 */
    }}
    QPushButton:pressed {{
        background-color: {Colors.buttonColor_01_select}; /* 클릭시 배경색 변경 */
    }}
    QPushButton:focus {{
        border: 2px solid {Colors.buttonColor_01_select};
    }}
    QPushButton:disabled {{
        background-color: {Colors.baseColor01}; /* 비활성화 상태 배경색 */
        border: 2px solid {Colors.borderColor01};
        color: #a1a1a1;
    }}
    QPushButton::hover:disabled {{
        background-color: {Colors.buttonColor_01_hover}; /* 마우스 오버시 비활성화 상태 배경색 변경 */
    }}
    """