from .colors import Colors

class Style:
    #Title Bar Colors

    base_style01 = f'background-color: {Colors.baseColor02};'
    

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

    QPushButton:checked {{
        background-color: {Colors.base_color_X};
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
    """



    setting_list_button_style = f"""
    QWidget{{
        background-color: {Colors.base_color_06};
        border: 1px solid rgb(00, 00, 00);
        padding: 0px;
        margin: 0px;
    }}

    QPushButton {{
        background-color: {Colors.base_color_06};
        padding: 5px;
        margin: 0px;
        border-radius: 0px;
        border: none;
        text-align: center;
        font-size: 16px;
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

    QPushButton:checked {{
        background-color: {Colors.base_color_04};
    }}

    QPushButton:selected {{
        background-color: {Colors.base_color_04};
    }}
    """