import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objects as go


def main(): 

    st.markdown("<h1 style='color: #19105B;'>Agg Fund Summary</h1>", unsafe_allow_html=True)

    # Investments Details
    # st.subheader(':blue[Investments Details:]')      
    # investments_details = pd.read_csv('./inputs/investments_details.csv') 
    # investments_details['Exit Date'] = pd.to_datetime(investments_details['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

    data_investments_details_pf1 = ss.investments_data_pf1
    data_investments_amount_pf1 = ss.investments_amount_pf1
    data_revenue_return_pf1 = ss.revenue_return_pf1


    data_investments_details_pf2 = ss.investments_data_pf2
    data_investments_amount_pf2 = ss.investments_amount_pf2
    data_revenue_return_pf2 = ss.revenue_return_pf2


    # print('1111111111111111111', data_investments_details_pf2)
    data_investments_details_pf3 = ss.investments_data_pf3
    data_investments_amount_pf3 = ss.investments_amount_pf3
    data_revenue_return_pf3 = ss.revenue_return_pf3

    data = {'Name': ['Portco 1', 'Portco 2', 'Portco 3']}
    df = pd.DataFrame(data)

    col1, col2, col3 = st.columns(3)

    with col1:
        portco1_options = ['Low Case', 'Base Case', 'High Case']
        portco1_selected_option = st.selectbox('Choose an Portco 1 option:', portco1_options)

    with col2:
        portco2_options = ['Base Case', 'Low Case', 'High Case' ]
        portco2_selected_option = st.selectbox('Choose an Portco 2 option:', portco2_options)

    with col3:
        portco3_options = ['High Case', 'Low Case', 'Base Case']
        portco3_selected_option = st.selectbox('Choose an Portco 3 option:', portco3_options)

    # Display the selected option
    # st.write(f'You selected: {selected_option}')


    # Add a column with a dropdown list
    for i in df.index:
        # df.at[i, 'Scenario'] = st.selectbox('Select Action:', ['Low Case', 'High Case', 'Base Case'], key=i)
        if i  == 0:
            for pf1 in data_investments_details_pf1.index:
                # st.write(data_investments_details_pf1.at[pf1, 'Scenario'])
                if portco1_selected_option == data_investments_details_pf1.at[pf1, 'Scenario']:
                    df.at[0, 'Scenario'] = portco1_selected_option
                    df.at[0, 'Date of Investment'] = data_investments_amount_pf1.iloc[0]['Date of Investment']
                    df.at[0, 'Invested Amount'] = data_investments_details_pf1.at[pf1, 'Invested Amount']
                    df.at[0, 'EBITDA at Entry'] = data_investments_amount_pf1.iloc[0]['EBITDA at entry']
                    df.at[0, 'EBITDA at Exit'] = data_investments_details_pf1.at[pf1, 'EBITDA at Exit']
                    df.at[0, 'Multiple at entry'] = data_investments_amount_pf1.iloc[0]['Multiple at Entry']
                    df.at[0, 'Multiple at Exit'] = data_investments_details_pf1.at[pf1, 'Multiple at Exit']
                    df.at[0, 'Exit Date'] = data_investments_details_pf1.at[pf1, 'Exit Date']
                    if portco1_selected_option == 'Low Case':
                        df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[0, 'Return (calculated)']
                        df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[0, 'IRR (calculated)']

                    if portco1_selected_option == 'Base Case':
                        df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[1, 'Return (calculated)']
                        df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[1, 'IRR (calculated)']

                    if portco1_selected_option == 'High Case':
                        df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[2, 'Return (calculated)']
                        df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[2, 'IRR (calculated)']

        if i  == 1:
            for pf1 in data_investments_details_pf2.index:
                # st.write(data_investments_details_pf2.at[pf1, 'Scenario'])
                if portco2_selected_option == data_investments_details_pf2.at[pf1, 'Scenario']:
                    df.at[1, 'Scenario'] = portco2_selected_option
                    df.at[1, 'Date of Investment'] = data_investments_amount_pf2.iloc[0]['Date of Investment']
                    df.at[1, 'Invested Amount'] = data_investments_details_pf2.at[pf1, 'Invested Amount']
                    df.at[1, 'EBITDA at Entry'] = data_investments_amount_pf2.iloc[0]['EBITDA at entry']
                    df.at[1, 'EBITDA at Exit'] = data_investments_details_pf2.at[pf1, 'EBITDA at Exit']
                    df.at[1, 'Multiple at entry'] = data_investments_amount_pf2.iloc[0]['Multiple at Entry']
                    df.at[1, 'Multiple at Exit'] = data_investments_details_pf2.at[pf1, 'Multiple at Exit']
                    df.at[1, 'Exit Date'] = data_investments_details_pf2.at[pf1, 'Exit Date']
                    if portco2_selected_option == 'Low Case':
                        df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[0, 'Return (calculated)']
                        df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[0, 'IRR (calculated)']

                    if portco2_selected_option == 'Base Case':
                        df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[1, 'Return (calculated)']
                        df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[1, 'IRR (calculated)']

                    if portco2_selected_option == 'High Case':
                        df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[2, 'Return (calculated)']
                        df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[2, 'IRR (calculated)']

        
        if i  == 2:
            for pf1 in data_investments_details_pf3.index:
                # st.write(data_investments_details_pf3.at[pf1, 'Scenario'])
                if portco3_selected_option == data_investments_details_pf3.at[pf1, 'Scenario']:
                    df.at[2, 'Scenario'] = portco3_selected_option
                    df.at[2, 'Date of Investment'] = data_investments_amount_pf3.iloc[0]['Date of Investment']
                    df.at[2, 'Invested Amount'] = data_investments_details_pf3.at[pf1, 'Invested Amount']
                    df.at[2, 'EBITDA at Entry'] = data_investments_amount_pf3.iloc[0]['EBITDA at entry']
                    df.at[2, 'EBITDA at Exit'] = data_investments_details_pf3.at[pf1, 'EBITDA at Exit']
                    df.at[2, 'Multiple at entry'] = data_investments_amount_pf3.iloc[0]['Multiple at Entry']
                    df.at[2, 'Multiple at Exit'] = data_investments_details_pf3.at[pf1, 'Multiple at Exit']
                    df.at[2, 'Exit Date'] = data_investments_details_pf3.at[pf1, 'Exit Date']
                    if portco3_selected_option == 'Low Case':
                        df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[0, 'Return (calculated)']
                        df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[0, 'IRR (calculated)']

                    if portco2_selected_option == 'Base Case':
                        df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[1, 'Return (calculated)']
                        df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[1, 'IRR (calculated)']

                    if portco2_selected_option == 'High Case':
                        df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[2, 'Return (calculated)']
                        df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[2, 'IRR (calculated)']
    
    st.markdown("<h2 style='color: #19105B; font-size:28px;'>Total of Fund Level:</h2>", unsafe_allow_html=True)

    st.write(df)

    total_investment_amout = df['Invested Amount'].sum()
    # total_return_amount = df['Return (calculated)'].sum()

    fun_level_data = {
        'Invested Amount': [total_investment_amout],
        'Return (calculated)': [23]
    }
    
    fun_level_data_df = pd.DataFrame(fun_level_data)

    st.markdown("<h2 style='color: #19105B; font-size:28px;'>Total of Fund Level - Amount:</h2>", unsafe_allow_html=True)

    st.write(fun_level_data_df)

    
    # df = pd.DataFrame({
    #     'Column 1': [st.selectbox('d',options), st.selectbox('d',options), st.selectbox('d',options)],
    #     'Column 2': ['A', 'B', 'C']
    # })

    # def add_dropdowns(dataframe):
    #     # Example function to add dropdowns
    #     return dataframe

    # st.dataframe(add_dropdowns(df))

    # Create a sample dataframe
    # data = {
    #     'Category': ['Fruit', 'Vegetable', 'Fruit', 'Meat', 'Vegetable'],
    #     'Subcategory': ['Apple', 'Carrot', 'Banana', 'Beef', 'Broccoli']
    # }

    # df = pd.DataFrame(data)

    # # Create the primary dropdown for Category
    # selected_category = st.selectbox("Select Category", df['Category'].unique())

    # # Filter the dataframe based on the selected category
    # filtered_df = df[df['Category'] == selected_category]

    # # Create a dictionary for dependent dropdown options
    # dependent_dropdown_options = {
    #     'options': filtered_df['Subcategory'].unique().tolist(),
    #     'default': None  # You can set a default value here if needed
    # }

    # # Display the dependent dropdown using st_aggrid
    # grid_options = GridOptionsBuilder.from_dataframe(filtered_df).build()
    # AgGrid(filtered_df, gridOptions=grid_options, data_editor=dependent_dropdown_options)


    # @st.cache_data
    def get_chart_83992296():

        fig = go.Figure(go.Waterfall(
            name = "20", 
            # orientation = "v",
            measure = df['EBITDA at Entry'].tolist(),
            x = df['Name'].tolist(),
            # textposition = "outside",
            text = df['Return (calculated)'].tolist(),
            y = df['Date of Investment'].tolist(),
            # connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

        fig.update_layout(
                title = "Profit and loss statement 2018",
                showlegend = True
        )

        tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
        with tab1:
            st.plotly_chart(fig, theme="streamlit")
        # with tab2:
        #     st.plotly_chart(fig, theme=None)

    get_chart_83992296()


if __name__ == '__main__':
    main()


    # fig = go.Figure(go.Waterfall(
    #         x = ["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
    #         y = [60, 80, 0, -40, -20, 0],
    #     ))
    #     st.plotly_chart(fig, theme="streamlit")
    