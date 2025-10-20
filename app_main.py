import streamlit as st
from app_home import run_home
from app_eda import run_eda
from app_ml import run_ml


def main():
    st.title('스타트업 수익 예측 앱')
    menu_list = ['Home', 'EDA', 'ML']
    menu_select = st.sidebar.selectbox('메뉴', menu_list)

    if menu_select == menu_list[0]:
        run_home()
    elif menu_select == menu_list[1]:
        run_eda()
    elif menu_select == menu_list[2]:
        run_ml()
    


if __name__ == '__main__':
    main()