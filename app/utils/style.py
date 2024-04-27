from .colors import Colors

class Style:
    #Title Bar Colors

    base_style01 = f'background-color: {Colors.baseColor02};'
    
    frame_style = f"""
        background-color: {Colors.base_color_06};
        border-radius: 5px;  
    """
    
    
    mini_button_style = f"""
    QPushButton {{
        background-color: {Colors.base_color_06};
        border-radius: 5px;  
    }}
    
    """
    
    line_edit_style = f"""
    QLineEdit {{
        background-color: rgb(33, 37, 43);
        border-radius: 5px;
        border: 2px solid rgb(33, 37, 43);
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
        border-left: 3px solid {Colors.base_color_01}; /* Add left border */
        border-top: 3px solid {Colors.base_color_01}; /* Add top border */
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