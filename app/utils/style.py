from .colors import Colors

class Style:
    #Title Bar Colors

    base_style01 = f'background-color: {Colors.baseColor02};'
    
    mini_button_style = f"""
    QPushButton {{
        border-radius: 5px;
    }}
    
    """
    
    

    menu_button_style = f"""
    QPushButton {{
        background-color: {Colors.buttonColor_01_base}; /* 배경색 */
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