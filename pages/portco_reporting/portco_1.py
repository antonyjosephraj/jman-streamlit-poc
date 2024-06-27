import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
import plotly.graph_objects as go


def main():

    # def style_dataframe(df):
    #     return df.style.set_table_styles(
    #         [{
    #             'selector': 'th',
    #             'props': [
    #                 ('background-color', '#19105B'),
    #                 ('color', 'white'),
    #                 ('font-family', 'Arial, sans-serif'),
    #                 ('font-size', '16px'),
    #                 ('border', '1px solid #e4e4e4')
    #             ]
    #         }, 
    #         {
    #             'selector': 'td',
    #             'props': [
    #                 ('font-size', '14px'),
    #                 ('border', '1px solid #e4e4e4')
    #             ]
    #         }]
    #     )

    applyCss = """
    <style>
    [data-testid="stAppViewBlockContainer"]{
    padding:30px;
    }
    [data-testid="stHorizontalBlock"] {
        border: 1px solid #66666633;
        border-radius: 10px;
        padding: 10px;
    } 
    div[data-testid="stDataFrameResizable"] > canvas > table > thead > tr > th {
        padding: 12px 15px;
        border:none;
    }
    div[data-testid="stDataFrameResizable"] > canvas > table >tbody > tr {
        text-align: center;
        background-color: green; 
    }
    </style>
    """
    st.markdown(applyCss, unsafe_allow_html=True)

    st.markdown("<h1 style='color: #19105B;'>Portfolio reporting 1</h1>", unsafe_allow_html=True)

    # st.set_page_config(layout="wide")

        # Investments
    investments = pd.read_csv('./inputs/investments.csv')
    investments['Date of Investment'] = pd.to_datetime(investments['Date of Investment'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
    # investments_edited_df = st.data_editor(investments)

    if 'investments_amount_pf1' not in ss:
        ss.investments_amount_pf1 = pd.DataFrame(investments)

    def str_to_int(value_str):
        return int(value_str.replace(',', ''))

    # Investments Details
    investments_details = pd.read_csv('./inputs/investments_details.csv') 
    investments_details['Exit Date'] = pd.to_datetime(investments_details['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    # investments_details['Invested Amount'] = investments_details['Invested Amount'].apply(lambda x: str_to_int(x))

    if 'investments_data_pf1' not in ss:
        ss.investments_data_pf1 = pd.DataFrame(investments_details)

    col1, col2 = st.columns(2)

    # revenue_return_df = pd.DataFrame()


    with st.container(border=True):
        with col1:
            
            # st.header("A cat")
            st.markdown("<h2 style='color: #19105B; font-size:28px;'>Investments:</h2>", unsafe_allow_html=True)

            investments_edited_df = de(ss.investments_amount_pf1)

            # investments_edited_df = de(style_dataframe(ss.investments_amount_pf1).to_html())
            # investments_edited_df = de(style_dataframe(ss.investments_amount_pf1).hide(axis="index")).to_html()
            # st.write(style_dataframe(investments_edited_df).hide(axis="index").to_html(), unsafe_allow_html=True)


            st.markdown("<h2 style='color: #19105B; font-size:28px;'>Investments Details:</h2>", unsafe_allow_html=True)

            investments_details_v2 = de(ss.investments_data_pf1)
            # st.write(style_dataframe(investments_details_v2).hide(axis="index").to_html(), unsafe_allow_html=True)

        # investments_details_v2 = de(ss.investments_data_pf1)

    column1, column2 = st.columns(2)


    # investments_details.loc[investments_details['Scenario'] == 'Low Case', 'Invested Amount'] = 30000
    # investments_details_edited_df = st.data_editor(investments_details)
    # print('ppppppppppppppppp', investments_details_edited_df)
    # investments_details_edited_df = st.data_editor(investments_details, num_rows="dynamic")

    # Calculations
    min_date = investments_edited_df['Date of Investment'].min()
    investments_at_entry = investments_edited_df['Investment at entry'].sum()


    # print('investments_edited_df \n', investments_edited_df['Date of Investment'])
    # print('min_date \n', min_date)


    # investments_details_v2['Exit Date'] = pd.to_datetime(investments_details_v2['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    max_date = investments_details_v2['Exit Date'].max()
    # print('investments_details_edited_df \n', investments_details_edited_df['Exit Date'])
    # print('max_date \n', max_date)

    # Assumptions
    # columns = ["Date" ,"Low Case" ,"Base Case" ,"High Case" ,"Comments"]
    # assumptions = pd.DataFrame(columns=columns)
    # st.write(assumptions)

    date_range = pd.date_range(start=min_date, end=max_date, freq='M')
    assumptions = pd.DataFrame(date_range, columns=['Date'])
    assumptions['Date'] = pd.to_datetime(assumptions['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    assumptions[["Low Case" ,"Base Case" ,"High Case" ,"Comments"]] = None
    assumptions.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]
    # st.write(assumptions)

    if 'assumptions_data_pf1' not in ss:
        ss.assumptions_data_pf1 = pd.DataFrame(assumptions)

    if not ss.investments_amount_pf1.equals(investments_edited_df):
        ss.investments_amount_pf1 = investments_edited_df
        min_date = ss.investments_amount_pf1['Date of Investment'].min()
        investments_at_entry = ss.investments_amount_pf1['Investment at entry'].sum()

        ss.assumptions_data_pf1.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]

    with st.container(border=True):

        with column1:
            st.markdown("<h2 style='color: #19105B; font-size:28px;'>Casual Assumptions:</h2>", unsafe_allow_html=True)

            assumptions_edited_df_v2 = de(ss.assumptions_data_pf1)

        # assumptions_edited_df = st.data_editor(assumptions)

        investment_update = assumptions_edited_df_v2

        low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
        base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
        high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()


        if not ss.assumptions_data_pf1.equals(assumptions_edited_df_v2):
            ss.assumptions_data_pf1 = assumptions_edited_df_v2
            # ss.investments_data_pf1.loc[ss.investments_data_pf1['Invested Amount'].notna(), 'Multiple at Exit'] = ss.investments_data_pf1['Invested Amount']
            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)
            rr()
        # investments_details.loc[investments_details['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
        # investments_details.loc[investments_details['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
        # investments_details.loc[investments_details['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)




        if not ss.investments_data_pf1.equals(investments_details_v2):

            ss.investments_data_pf1 = investments_details_v2

            max_date = ss.investments_data_pf1['Exit Date'].max()

            sample_data = ss.assumptions_data_pf1

            date_range = pd.date_range(start=min_date, end=max_date, freq='M')
            ss.assumptions_data_pf1 = pd.DataFrame(date_range, columns=['Date'])
            ss.assumptions_data_pf1['Date'] = pd.to_datetime(ss.assumptions_data_pf1['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
            ss.assumptions_data_pf1[["Low Case" ,"Base Case" ,"High Case" ,"Comments"]] = None
            merged_df = pd.merge(ss.assumptions_data_pf1, sample_data, on=['Date'], suffixes=('_df1', '_df2'), how='left')

            # Update 'Salary' in df1 where 'Salary_df2' is not NaN (indicating a match)
            merged_df['Low Case'] = merged_df.apply(lambda row: row['Low Case_df2'] if not pd.isna(row['Low Case_df2']) else row['Low Case_df1'], axis=1)
            merged_df['Base Case'] = merged_df.apply(lambda row: row['Base Case_df2'] if not pd.isna(row['Base Case_df2']) else row['Base Case_df1'], axis=1)
            merged_df['High Case'] = merged_df.apply(lambda row: row['High Case_df2'] if not pd.isna(row['High Case_df2']) else row['High Case_df1'], axis=1)
            merged_df['Comments'] = merged_df.apply(lambda row: row['Comments_df2'] if not pd.isna(row['Comments_df2']) else row['Comments_df1'], axis=1)

            # Select final columns and drop duplicates
            ss.assumptions_data_pf1 = merged_df[['Date', "Low Case" ,"Base Case" ,"High Case" ,"Comments"]].drop_duplicates()

            # ss.assumptions_data_pf1[["Low Case" ,"Base Case" ,"High Case" ,"Comments"]] = None
            
            
            investment_update = ss.assumptions_data_pf1

            low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
            base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
            high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()

            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
            ss.investments_data_pf1.loc[ss.investments_data_pf1['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)

            rr()

            

        column_values_list = investments_details_v2['Scenario'].tolist()
        column_values_values = investments_details_v2['EBITDA at Exit'].tolist()
        column_values_values2 = investments_details_v2['Multiple at Exit'].tolist()

        # st.write(column_values_list)

        data2 = {
            'Calc': ['ARR /Rev /EBITDA', 'Multiple'],
            'Entry': [200,10]
        }
        data_v2 = pd.DataFrame(data2)
        # data_v2 = pd.DataFrame(columns=column_values_list)
        data_v2[column_values_list] = None
        data_v2.loc[0, column_values_list] = column_values_values
        data_v2.loc[1, column_values_list] = column_values_values2

        ss.data_v2_pf1 = data_v2


        data3 = {
            'Calc': ['Net Debt', 'Cash flow adj'],
            'Entry': [None,None]
        }
        data_v3 = pd.DataFrame(data3)
        data_v3[column_values_list] = None
        
        if 'data_v3_pf1' not in ss:
            ss.data_v3_pf1 = data_v3


        # FUNCTIONS
        def calculate_equity(df, case):
            arr_rev_ebitda = df.loc[df['Calc'] == 'ARR /Rev /EBITDA', case].values
            multiple = df.loc[df['Calc'] == 'Multiple', case].values
            net_debt = df.loc[df['Calc'] == 'Net Debt', case].values
            cash_flow_adj = df.loc[df['Calc'] == 'Cash flow adj', case].values

            if isinstance(arr_rev_ebitda, list):
                arr_rev_ebitda = int(arr_rev_ebitda)
            if isinstance(multiple, list):
                multiple = int(multiple) 

            net_debt = 0 if net_debt == None else net_debt
            cash_flow_adj = 0 if cash_flow_adj == None else cash_flow_adj
            a = int(arr_rev_ebitda * multiple)
            b = int(int(net_debt) + int(cash_flow_adj))
            result = a + b
            return result

        def calculate_value(df, case):
            equity = df.loc[df['Calc'] == 'Equity', case].values
            ownership = df.loc[df['Calc'] == 'Ownership %', case].values

            equity = 1 if equity == None else equity
            ownership = 1 if ownership == None else ownership
            return (int(equity) * int(ownership))


        def calculate_money_multiple(df, case):
            value = df.loc[df['Calc'] == 'Value', case].values[0]
            investments = df.loc[df['Calc'] == 'Investment', case].values[0]

            print('LLL', value, investments)

            value = 1 if value == None else value
            investments = 1 if investments == None else investments

            return str(value / investments) + 'x' 

        with column1:
            st.markdown("<h2 style='color: #19105B; font-size:28px;'>Valuation Waterfall Output:</h2>", unsafe_allow_html=True)

            # with st.container(height=300, border=True, backgroundColor='red'):
            with st.container(height=300, border=True):
                # st.write(ss)

                st.write(data_v2)
                data_v3_edited_df = de(data_v3)
                
                if not ss.data_v3_pf1.equals(data_v3_edited_df):
                    sample_data = data_v3_edited_df
                    merged_df = pd.merge(ss.data_v3_pf1, sample_data, on=['Calc'], suffixes=('_df1', '_df2'), how='left')
                    merged_df['Entry'] = merged_df.apply(lambda row: row['Entry_df2'] if not pd.isna(row['Entry_df2']) else row['Entry_df1'], axis=1)
                    merged_df['Low Case'] = merged_df.apply(lambda row: row['Low Case_df2'] if not pd.isna(row['Low Case_df2']) else row['Low Case_df1'], axis=1)
                    merged_df['Base Case'] = merged_df.apply(lambda row: row['Base Case_df2'] if not pd.isna(row['Base Case_df2']) else row['Base Case_df1'], axis=1)
                    merged_df['High Case'] = merged_df.apply(lambda row: row['High Case_df2'] if not pd.isna(row['High Case_df2']) else row['High Case_df1'], axis=1)

                    # Select final columns and drop duplicates
                    ss.data_v3_pf1 = merged_df[['Calc', "Entry", "Low Case" ,"Base Case" ,"High Case"]].drop_duplicates()


                concatenated_df = pd.concat([data_v2, data_v3_edited_df], ignore_index=True)

                # Calculate Equity for each case
                equity_entry = calculate_equity(concatenated_df, 'Entry')
                equity_low_case = calculate_equity(concatenated_df, 'Low Case')
                equity_base_case = calculate_equity(concatenated_df, 'Base Case')
                equity_high_case = calculate_equity(concatenated_df, 'High Case')

                equity_data = {
                    'Calc': ['Equity'],
                    'Entry':[equity_entry],
                    'Low Case':[equity_low_case],
                    'Base Case':[equity_base_case],
                    'High Case':[equity_high_case]
                }

                equity_df = pd.DataFrame(equity_data)

                ss.equity_df_pf1 = equity_df

                st.write(ss.equity_df_pf1)

                ownership_data_pf1 = {
                    'Calc': ['Ownership %'],
                    'Entry': None,
                    'Low Case':None,
                    'Base Case':None,
                    'High Case':None
                }

                ownership_df = pd.DataFrame(ownership_data_pf1)

                if 'ownership_df_pf1' not in ss:
                    ss.ownership_df_pf1 = ownership_df

                # st.write(ownership_df_pf1)
                ownership_edited_df_pf1 = de(ownership_df)

                if not ss.ownership_df_pf1.equals(ownership_edited_df_pf1):
                    sample_data = ownership_edited_df_pf1
                    merged_df = pd.merge(ss.ownership_df_pf1, sample_data, on=['Calc'], suffixes=('_df1', '_df2'), how='left')
                    merged_df['Entry'] = merged_df.apply(lambda row: row['Entry_df2'] if not pd.isna(row['Entry_df2']) else row['Entry_df1'], axis=1)
                    merged_df['Low Case'] = merged_df.apply(lambda row: row['Low Case_df2'] if not pd.isna(row['Low Case_df2']) else row['Low Case_df1'], axis=1)
                    merged_df['Base Case'] = merged_df.apply(lambda row: row['Base Case_df2'] if not pd.isna(row['Base Case_df2']) else row['Base Case_df1'], axis=1)
                    merged_df['High Case'] = merged_df.apply(lambda row: row['High Case_df2'] if not pd.isna(row['High Case_df2']) else row['High Case_df1'], axis=1)

                    # Select final columns and drop duplicates
                    ss.ownership_df_pf1 = merged_df[['Calc', "Entry", "Low Case" ,"Base Case" ,"High Case"]].drop_duplicates()


                concatenated_df_v2 = pd.concat([equity_df, ss.ownership_df_pf1], ignore_index=True)

                # Calculate Equity for each case
                value_entry = calculate_value(concatenated_df_v2, 'Entry')
                value_low_case = calculate_value(concatenated_df_v2, 'Low Case')
                value_base_case = calculate_value(concatenated_df_v2, 'Base Case')
                value_high_case = calculate_value(concatenated_df_v2, 'High Case')


                value_and_investment = {
                    'Calc': ['Value', 'Investment'],
                    'Entry':[value_entry, investments_at_entry],
                    'Low Case':[value_low_case, investments_at_entry],
                    'Base Case':[value_base_case, investments_at_entry],
                    'High Case':[value_high_case, investments_at_entry]
                }

                value_and_investment_df = pd.DataFrame(value_and_investment)
                st.write(value_and_investment_df)
                ss.value_and_investment_df_pf1 = value_and_investment_df

                # Calculate Equity for each case
                money_multiple_entry = calculate_money_multiple(value_and_investment_df, 'Entry')
                money_multiple_low_case = calculate_money_multiple(value_and_investment_df, 'Low Case')
                money_multiple_base_case = calculate_money_multiple(value_and_investment_df, 'Base Case')
                money_multiple_high_case = calculate_money_multiple(value_and_investment_df, 'High Case')


                money_multiple = {
                    'Calc': ['Money Multiple'],
                    'Entry':[money_multiple_entry],
                    'Low Case':[money_multiple_low_case],
                    'Base Case':[money_multiple_base_case],
                    'High Case':[money_multiple_high_case]
                }

                money_multiple_df = pd.DataFrame(money_multiple)
                st.write(money_multiple_df)
                ss.money_multiple_df_pf1 = money_multiple_df



    money_multiple_value = money_multiple_df.iloc[0].tolist()

    # IRR
    df3 = assumptions_edited_df_v2

    df3['Low Case'] = pd.to_numeric(df3['Low Case'], errors='coerce')
    df3['Base Case'] = pd.to_numeric(df3['Base Case'], errors='coerce')
    df3['High Case'] = pd.to_numeric(df3['High Case'], errors='coerce')

    # # Calculate days from the start date for each cash flow
    df3['Date'] = pd.to_datetime(df3['Date'])

    df3['Days'] = (df3['Date'] - df3['Date'].iloc[0]).dt.days

    # Adjusted cash flows considering time value of money
    df3['Low Case Cash Flow'] = df3['Low Case'] / (1 + 0.05)**(df3['Days'] / 365)
    df3['Low Case Cash Flow'] = df3['Low Case Cash Flow'].fillna(1)

    df3['Base Case Cash Flow'] = df3['Base Case'] / (1 + 0.05)**(df3['Days'] / 365)
    df3['Base Case Cash Flow'] = df3['Base Case Cash Flow'].fillna(1)

    df3['High Case Cash Flow'] = df3['High Case'] / (1 + 0.05)**(df3['Days'] / 365)
    df3['High Case Cash Flow'] = df3['High Case Cash Flow'].fillna(1)

    # Calculate IRR based on adjusted cash flows
    low_case_irr = npf.irr(df3['Low Case Cash Flow'])
    base_case_irr = npf.irr(df3['Base Case Cash Flow'])
    high_case_irr = npf.irr(df3['High Case Cash Flow'])


    revenue_return = {
        'Return (calculated)': money_multiple_value[2:],
        'IRR (calculated)': [low_case_irr, base_case_irr, high_case_irr ]
    }

    revenue_return_df = pd.DataFrame(revenue_return)

    # st.write(revenue_return_df)
    ss.revenue_return_pf1 = revenue_return_df

    # elif 'revenue_return_pf1' not in ss:
    #     ss.revenue_return_pf1 = revenue_return_df

    with col2:
        # st.write(ss)
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Return Revenue:</h2>", unsafe_allow_html=True)
        st.write(revenue_return_df)
        # styled_df_1 = style_dataframe(ss.revenue_return_pf1)
        # st.write(style_dataframe(ss.revenue_return_pf1).hide(axis="index").to_html(), unsafe_allow_html=True)

    # Waterfall Data 
    waterfall_data = pd.concat([ss.data_v2_pf1, ss.data_v3_pf1, ss.equity_df_pf1, ss.ownership_df_pf1, ss.value_and_investment_df_pf1, ss.money_multiple_df_pf1], ignore_index=True)

    print('111111111111111', waterfall_data)
    investments_at_entry_amount = ss.investments_amount_pf1['Investment at entry'].sum()

    waterfall_options_pf1 = ['Low Case', 'Base Case', 'High Case']
    selected_option_pf1 = st.selectbox('Choose an Portco 1 option:', waterfall_options_pf1)

    ebitda_value = 0

    if selected_option_pf1 in waterfall_data.columns:
        # =((J22-H22)*H24+H25+H26)*H28
        case_value = waterfall_data[selected_option_pf1].iloc[0]
        entry_value = waterfall_data.loc[waterfall_data['Calc'] == 'ARR /Rev /EBITDA', 'Entry'].values
        actual_entry_value = int(case_value) - int(entry_value)
        # total_calc_column = waterfall_data['Calc'].isin(['Multiple', 'Net Debt', 'Cash flow adj'])
        # total_value = waterfall_data.loc[total_calc_column, 'Entry'].sum()
        multiple = waterfall_data.loc[waterfall_data['Calc'] == 'Multiple', selected_option_pf1].values
        net_debt = waterfall_data.loc[waterfall_data['Calc'] == 'Net Debt', selected_option_pf1].values
        cash_flow_adj = waterfall_data.loc[waterfall_data['Calc'] == 'Cash flow adj', selected_option_pf1].values
        if multiple == None:
            multiple = 0
        if net_debt == None:
            net_debt = 0
        if cash_flow_adj == None:
            cash_flow_adj = 0

        total_value = int(multiple) + int(net_debt) + int(cash_flow_adj)
        print('444444444444',actual_entry_value,  total_value, investments_at_entry_amount)
        ownership_data_v2 = waterfall_data.loc[waterfall_data['Calc'] == 'Ownership %', selected_option_pf1].values[0]
        if ownership_data_v2 == None:
            ownership_data_v2 = 0

        print('22222222222222222',actual_entry_value , total_value,  ownership_data_v2)

        ebitda_value = (actual_entry_value * total_value) * int(ownership_data_v2)

    print('33333333', ebitda_value )

    multiple_growth = 0
    if selected_option_pf1 in waterfall_data.columns:
       # =((J24-H24)*J22+H25)*H28
        case_value1 = waterfall_data.loc[waterfall_data['Calc'] == 'Multiple', 'Entry'].values
        case_value2 = waterfall_data.loc[waterfall_data['Calc'] == 'Multiple', selected_option_pf1].values
        multi_minus_value = int(case_value2) - int(case_value1)
        total_value1 = waterfall_data.loc[waterfall_data['Calc'] == 'ARR /Rev /EBITDA', 'Entry'].values
        total_value2 = waterfall_data.loc[waterfall_data['Calc'] == 'Cash flow adj', selected_option_pf1].values

        if total_value1 == None:
            total_value1 = 0
        if total_value2 == None:
            total_value2 = 0

        total_value3 = int(total_value1) + int(total_value2)
        ownership_data_v2 = waterfall_data.loc[waterfall_data['Calc'] == 'Ownership %', selected_option_pf1].values[0]
        if ownership_data_v2 == None:
            ownership_data_v2 = 0
        print('22222222222222222',multi_minus_value , total_value3,  ownership_data_v2)
        multiple_growth = (multi_minus_value * total_value3) * int(ownership_data_v2)

    print('111111111111111111111111', ebitda_value, multiple_growth )

    asset_value_v1 = waterfall_data.loc[waterfall_data['Calc'] == 'Value', 'Low Case'].values
    asset_value_v2 = waterfall_data.loc[waterfall_data['Calc'] == 'Value', 'Base Case'].values
    asset_value_v3 = waterfall_data.loc[waterfall_data['Calc'] == 'Value', 'High Case'].values

    asset_value_total = int(asset_value_v1) + int(asset_value_v2) + int(asset_value_v3)

    financial_engineering = (investments_at_entry_amount + ebitda_value + multiple_growth ) - asset_value_total
    print('yyyy', financial_engineering)
    print('ZZZZ', investments_at_entry_amount, ebitda_value, multiple_growth, financial_engineering, asset_value_total)
    print('--------------------')

    waterfall_data_flow = {
        'Category': ['Value at invetsment', 'EBITDA growth', 'Multiple growth', 'Financial engineering', 'Asset value'],
        'Values': [investments_at_entry_amount, ebitda_value, multiple_growth, financial_engineering, asset_value_total  ]
    }

    waterfall_data_flow_pf1 = pd.DataFrame(waterfall_data_flow)

    with column2:
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Waterfall Chart:</h2>", unsafe_allow_html=True)

        def get_chart_83992296():

            fig = go.Figure(go.Waterfall(
                name = "20", 
                # orientation = "v",
                measure = ['Low Case', 'Base Case', 'High Case'],
                x = waterfall_data_flow_pf1['Category'],
                # textposition = "outside",
                # text = ['Low', 'Base', 'High'],
                y = waterfall_data_flow_pf1['Values'],
                # connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))

            fig.update_layout(
                    title = "Proftolio Insights dashboard",
                    showlegend = True
            )

            st.plotly_chart(fig, theme="streamlit")
            # with tab2:
            #     st.plotly_chart(fig, theme=None)

        get_chart_83992296()

    

if __name__ == '__main__':
    main()