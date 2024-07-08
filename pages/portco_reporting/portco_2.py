import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
import plotly.graph_objects as go
import string
import random

def main():

    applyCss = """
        <style>

        [data-testid="stAppViewBlockContainer"]{
            padding:30px;
        }
        
        [data-testid="stHorizontalBlock"] {
            border: 1px solid #19105B;
            border-radius: 10px;
            padding: 10px;
        } 
        
        hr {
            margin: 5px 0 20px 0;
            padding: 1px;
            background-color: #19105B;
        }
        div[data-testid="stDataFrameResizable"] > canvas > table > thead > tr > th {
            padding: 12px 15px;
            border:none;
        }
        div[data-testid="stDataFrameResizable"] > canvas > table >tbody > tr {
            text-align: center;
            background-color: green; 
        }
        .top-right {
            position: absolute; top: -80px; right: 5px;
            flex:row;
        } 
        .top-right > button:first-child {
            background-color: #19105B ;
            border: 1px solid black;
            padding: 8px 10px;
            border-radius: 10px;
            color: white;
        }

        .top-right > button:nth-child(2) {
            background-color: #19105B ;
            border: 1px solid black;
            padding: 8px 10px;
            border-radius: 10px;
            color: white;
            margin-left: 5px;
        }
        
        .st-emotion-cache-r421ms {
            border: 2px solid #19105B;
            border-radius: 10px;
            padding: 20px 300px;
        } 


        </style>
    """

    st.markdown(applyCss, unsafe_allow_html=True)
    st.markdown("<h1 style='color: #19105B; padding:0;'>Portfolio Reporting 2</h1>", unsafe_allow_html=True)
    st.divider()

    st.markdown('<div class="top-right"><button>Upload</button> <button>Download</button> </div>', unsafe_allow_html=True)

    # Investments
    investments = pd.read_csv('./inputs/investments_v2.csv')
    investments['Date of Investment'] = pd.to_datetime(investments['Date of Investment'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

    if 'investments_amount_pf2' not in ss:
        ss.investments_amount_pf2 = pd.DataFrame(investments)

    def str_to_int(value_str):
        return int(value_str.replace(',', ''))

    # Investments Details
    investments_details = pd.read_csv('./inputs/investments_details_v2.csv') 
    investments_details['Exit Date'] = pd.to_datetime(investments_details['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

    if 'investments_data_pf2' not in ss:
        ss.investments_data_pf2 = pd.DataFrame(investments_details)

    # Define Columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Investments</h2>", unsafe_allow_html=True)
        investments_edited_df = de(ss.investments_amount_pf2)

        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Investments Details</h2>", unsafe_allow_html=True)
        investments_details_v2 = de(ss.investments_data_pf2)

    column1, column2 = st.columns(2)

    # Calculations
    min_date = investments_edited_df['Date of Investment'].min()
    investments_at_entry = investments_edited_df['Investment at entry'].sum()

    # investments_details_v2['Exit Date'] = pd.to_datetime(investments_details_v2['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    max_date = investments_details_v2['Exit Date'].max()

    # Assumptions
    date_range = pd.date_range(start=min_date, end=max_date, freq='M')
    assumptions = pd.DataFrame(date_range, columns=['Date'])
    assumptions['Date'] = pd.to_datetime(assumptions['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    num_rows = assumptions.shape[0]
    sample_values = np.random.randint(1000, 10000, size=(num_rows, 3))
    mask = np.random.rand(*sample_values.shape) < 0.9
    sample_values[mask] = 0
    # assumptions[["Low Case" ,"Base Case" ,"High Case" ,"Comments"]] = None
    assumptions["Low Case"] = sample_values[:, 0]
    assumptions["Base Case"] = sample_values[:, 1]
    assumptions["High Case"] = sample_values[:, 2]
    assumptions["Comments"] = None
    assumptions.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]

    if 'assumptions_data_pf2' not in ss:
        ss.assumptions_data_pf2 = pd.DataFrame(assumptions)

    if not ss.investments_amount_pf2.equals(investments_edited_df):
        ss.investments_amount_pf2 = investments_edited_df
        min_date = ss.investments_amount_pf2['Date of Investment'].min()
        investments_at_entry = ss.investments_amount_pf2['Investment at entry'].sum()

        ss.assumptions_data_pf2.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]

    with column1:
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Cashflow Assumptions</h2>", unsafe_allow_html=True)

        assumptions_edited_df_v2 = de(ss.assumptions_data_pf2)

    investment_update = assumptions_edited_df_v2

    low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
    base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
    high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()


    if not ss.assumptions_data_pf2.equals(assumptions_edited_df_v2):
        ss.assumptions_data_pf2 = assumptions_edited_df_v2
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)
        rr()

    if not ss.investments_data_pf2.equals(investments_details_v2):
        ss.investments_data_pf2 = investments_details_v2

        max_date = ss.investments_data_pf2['Exit Date'].max()

        sample_data = ss.assumptions_data_pf2

        date_range = pd.date_range(start=min_date, end=max_date, freq='M')
        ss.assumptions_data_pf2 = pd.DataFrame(date_range, columns=['Date'])
        ss.assumptions_data_pf2['Date'] = pd.to_datetime(ss.assumptions_data_pf2['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        ss.assumptions_data_pf2[["Low Case" ,"Base Case" ,"High Case"]] = 0
        ss.assumptions_data_pf2[["Comments"]] = None

        merged_df = pd.merge(ss.assumptions_data_pf2, sample_data, on=['Date'], suffixes=('_df1', '_df2'), how='left')

        # Update 'Salary' in df1 where 'Salary_df2' is not NaN (indicating a match)
        merged_df['Low Case'] = merged_df.apply(lambda row: row['Low Case_df2'] if not pd.isna(row['Low Case_df2']) else row['Low Case_df1'], axis=1)
        merged_df['Base Case'] = merged_df.apply(lambda row: row['Base Case_df2'] if not pd.isna(row['Base Case_df2']) else row['Base Case_df1'], axis=1)
        merged_df['High Case'] = merged_df.apply(lambda row: row['High Case_df2'] if not pd.isna(row['High Case_df2']) else row['High Case_df1'], axis=1)
        merged_df['Comments'] = merged_df.apply(lambda row: row['Comments_df2'] if not pd.isna(row['Comments_df2']) else row['Comments_df1'], axis=1)

        # Select final columns and drop duplicates
        ss.assumptions_data_pf2 = merged_df[['Date', "Low Case" ,"Base Case" ,"High Case" ,"Comments"]].drop_duplicates()

        investment_update = ss.assumptions_data_pf2

        low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
        base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
        high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()

        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)

        rr()

    column_values_list = investments_details_v2['Scenario'].tolist()
    column_values_values = investments_details_v2['EBITDA at Exit'].tolist()
    column_values_values2 = investments_details_v2['Multiple at Exit'].tolist()

    editda_multiple = {
        'Calc': ['ARR /Rev /EBITDA', 'Multiple'],
        'Entry': [200, 100]
    }
    editda_multiple_df = pd.DataFrame(editda_multiple)
    editda_multiple_df[column_values_list] = None
    editda_multiple_df.loc[0, column_values_list] = column_values_values
    editda_multiple_df.loc[1, column_values_list] = column_values_values2

    ss.editda_multiple_df_pf2 = editda_multiple_df

    netdebt_and_cashflow_pf2 = {
        'Calc': ['Net Debt', 'Cash flow adj'],
        'Entry': [300, 280]
    }
    netdebt_and_cashflow_df_pf2 = pd.DataFrame(netdebt_and_cashflow_pf2)
    netdebt_and_cashflow_df_pf2['Low Case'] = [9,20]
    netdebt_and_cashflow_df_pf2['Base Case'] = [23,12]
    netdebt_and_cashflow_df_pf2['High Case'] = [7,13]


    if 'netdebt_and_cashflow_df_pf2' not in ss:
            ss.netdebt_and_cashflow_df_pf2 = netdebt_and_cashflow_df_pf2

    # FUNCTIONS
    def calculate_equity(df, case):
        arr_rev_ebitda = df.loc[df['Calc'] == 'ARR /Rev /EBITDA', case].values[0]
        multiple = df.loc[df['Calc'] == 'Multiple', case].values[0]
        net_debt = df.loc[df['Calc'] == 'Net Debt', case].values[0]
        cash_flow_adj = df.loc[df['Calc'] == 'Cash flow adj', case].values[0]

        arr_rev_ebitda = 0 if arr_rev_ebitda == None or arr_rev_ebitda == '' else arr_rev_ebitda
        multiple = 0 if multiple == None or multiple == ''  else multiple
        net_debt = 0 if net_debt == None or net_debt == '' else net_debt
        cash_flow_adj = 0 if cash_flow_adj == None or cash_flow_adj == ''  else cash_flow_adj

        a = int(arr_rev_ebitda * multiple)
        b = int(net_debt) + int(cash_flow_adj)
        result = a + b
        return result

    def calculate_value(df, case):
        equity = df.loc[df['Calc'] == 'Equity', case].values[0]
        ownership = df.loc[df['Calc'] == 'Ownership %', case].values[0]

        equity = 1 if equity == None else equity
        ownership = 1 if ownership == None else ownership
        return (int(equity) * int(ownership))


    def calculate_money_multiple(df, case):
        value = df.loc[df['Calc'] == 'Value', case].values[0]
        investments = df.loc[df['Calc'] == 'Investment', case].values[0]

        value = 1 if value == None else value
        investments = 1 if investments == None else investments

        value_invt = value / investments
        value_invt_v2 = f"{value_invt:.1f}"
        value_invt_v3 = str(value_invt_v2) + 'x' 
        return value_invt_v3

    with column2:
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Valuation Waterfall Output</h2>", unsafe_allow_html=True)

        with st.container(height=400, border=True):
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["EBITDA", "Cash Flow", "Equity", "Ownership", "Value & Invt", "MM"])
            
            with tab1:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>EBITDA</h2>", unsafe_allow_html=True)
                st.write(ss.editda_multiple_df_pf2)

            with tab2:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>Cash Flow</h2>", unsafe_allow_html=True)
                netdebt_and_cashflow_edited_df_pf2 = de(ss.netdebt_and_cashflow_df_pf2)

            if not ss.netdebt_and_cashflow_df_pf2.equals(netdebt_and_cashflow_edited_df_pf2):
                ss.netdebt_and_cashflow_df_pf2 = netdebt_and_cashflow_edited_df_pf2
                rr()

            concatenated_df = pd.concat([ss.editda_multiple_df_pf2, ss.netdebt_and_cashflow_df_pf2], ignore_index=True)

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
            ss.equity_df_pf2 = equity_df

            with tab3:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>Equity</h2>", unsafe_allow_html=True)
                st.write(ss.equity_df_pf2)

            ownership_data_pf2 = {
                'Calc': ['Ownership %'],
                'Entry': 10,
                'Low Case':17,
                'Base Case':8,
                'High Case':7
            }

            ownership_df_pf2 = pd.DataFrame(ownership_data_pf2)
            if 'ownership_df_pf2' not in ss:
                ss.ownership_df_pf2 = ownership_df_pf2
            with tab4:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>Ownership</h2>", unsafe_allow_html=True)
                ownership_edited_df_pf2 = de(ss.ownership_df_pf2)

            if not ss.ownership_df_pf2.equals(ownership_edited_df_pf2):
                ss.ownership_df_pf2 = ownership_edited_df_pf2
                rr()


            concatenated_df_v2 = pd.concat([ss.equity_df_pf2, ss.ownership_df_pf2], ignore_index=True)

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
            ss.value_and_investment_df_pf2 = value_and_investment_df
            
            with tab5:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>Value & Investments</h2>", unsafe_allow_html=True)
                st.write(value_and_investment_df)

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
            with tab6:
                st.markdown("<h2 style='color: #19105B; font-size:28px;'>Money Mutiple</h2>", unsafe_allow_html=True)
                st.write(money_multiple_df)
            ss.money_multiple_df_pf2 = money_multiple_df

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

    low_case_irr_v2 = f"{low_case_irr:.1f}"
    base_case_irr_v2 = f"{base_case_irr:.1f}"
    high_case_irr_v2 = f"{high_case_irr:.1f}"

    revenue_return = {
        'Scenario': ['Low Case', 'Base Case', 'High Case'],
        'Return (calculated)': money_multiple_value[2:],
        'IRR (calculated)': [low_case_irr_v2, base_case_irr_v2, high_case_irr_v2]
    }
    revenue_return_df = pd.DataFrame(revenue_return)
    ss.revenue_return_pf2 = revenue_return_df


    def style_dataframe(df):
        return df.style.set_table_styles(
        [   {
            'selector': 'th',
            'props': [
                ('background-color', '#19105B'),
                ('color', 'white'),
                ('font-family', 'Arial, sans-serif'),
                    ('font-size', '16px')
                ]
            }, 
            {
                'selector': 'td, th',
                'props': [
                    ('border', '2px solid #19105B')
                ]
            }
        ])

    revenue_return_pf2_styled_df = style_dataframe(ss.revenue_return_pf2)
    with col2:
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Return Revenue</h2>", unsafe_allow_html=True)
        st.write(revenue_return_pf2_styled_df.hide(axis="index").set_table_attributes('style="margin: 0 auto; text-align: center;"').to_html(), unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Waterfall Chart</h2>", unsafe_allow_html=True)

        # Waterfall Data 
        waterfall_data_pf2 = pd.concat([ss.editda_multiple_df_pf2, ss.netdebt_and_cashflow_df_pf2, ss.equity_df_pf2, ss.ownership_df_pf2, ss.value_and_investment_df_pf2, ss.money_multiple_df_pf2], ignore_index=True)

        print('WATERFALL DATA - PF2: ', waterfall_data_pf2)
        investments_at_entry_amount = ss.investments_amount_pf1['Investment at entry'].sum()

        waterfall_options_pf2 = ['Low Case', 'Base Case', 'High Case']
        selected_option_pf2 = st.selectbox('Select a Scenario for PortCo 2:', waterfall_options_pf2)
        ss.selected_option_pf2 = selected_option_pf2

        ebitda_value = 0

        if ss.selected_option_pf2 in waterfall_data_pf2.columns:
            case_value = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'ARR /Rev /EBITDA', ss.selected_option_pf1].values
            if case_value == None:
                case_value = 0
            entry_value = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'ARR /Rev /EBITDA', 'Entry'].values
            actual_entry_value = int(case_value) - int(entry_value)
            multiple = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Multiple', ss.selected_option_pf2].values
            net_debt = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Net Debt', ss.selected_option_pf2].values
            cash_flow_adj = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Cash flow adj', ss.selected_option_pf2].values
            if multiple == None:
                multiple = 0
            if net_debt == None:
                net_debt = 0
            if cash_flow_adj == None:
                cash_flow_adj = 0

            total_value = int(multiple) + int(net_debt) + int(cash_flow_adj)
            ownership_data_v2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Ownership %', ss.selected_option_pf2].values[0]
            if ownership_data_v2 == None:
                ownership_data_v2 = 0

            ebitda_value = (actual_entry_value * total_value) * int(ownership_data_v2)

        multiple_growth = 0
        if ss.selected_option_pf2 in waterfall_data_pf2.columns:
            case_value1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Multiple', 'Entry'].values
            case_value2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Multiple', ss.selected_option_pf2].values
            multi_minus_value = int(case_value2) - int(case_value1)
            total_value1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'ARR /Rev /EBITDA', 'Entry'].values
            total_value2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Cash flow adj', ss.selected_option_pf2].values

            if total_value1 == None:
                total_value1 = 0
            if total_value2 == None:
                total_value2 = 0

            total_value3 = int(total_value1) + int(total_value2)
            ownership_data_v2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Ownership %', ss.selected_option_pf2].values[0]
            if ownership_data_v2 == None:
                ownership_data_v2 = 0
            multiple_growth = (multi_minus_value * total_value3) * int(ownership_data_v2)

        asset_value_v1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'Low Case'].values
        asset_value_v2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'Base Case'].values
        asset_value_v3 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'High Case'].values

        asset_value_total = int(asset_value_v1) + int(asset_value_v2) + int(asset_value_v3)

        financial_engineering = (investments_at_entry_amount + ebitda_value + multiple_growth ) - asset_value_total

        waterfall_data_flow_pf2 = {
            'Category': ['Value at invetsment', 'EBITDA growth', 'Multiple growth', 'Financial engineering', 'Asset value'],
            'Values': [investments_at_entry_amount, ebitda_value, multiple_growth, financial_engineering, asset_value_total  ]
        }

        waterfall_data_flow_df_pf2 = pd.DataFrame(waterfall_data_flow_pf2)

        def get_chart_83992296():

            fig = go.Figure(go.Waterfall(
                name = "20", 
                # orientation = "v",
                measure = ["relative", "relative", "relative",  "relative", "total"],
                x = waterfall_data_flow_df_pf2['Category'],
                # textposition = "outside",
                # text = ['Low', 'Base', 'High'],
                y = waterfall_data_flow_df_pf2['Values'],
                # connector = {"line":{"color":"rgb(63, 63, 63)"}},
                connector = {"line":{"color":"#19105B"}},
                decreasing = {"marker":{"color":"#3411A3", }},
                increasing = {"marker":{"color":"#FF6196"}},
                totals = {"marker":{"color":"#19105B",}}
            ))

            fig.update_layout(
                title="Portfolio Insights Dashboard",
                title_font=dict(
                    size=20,  # Title font size
                    color='#FF6196'  # Title color
                ),
                xaxis=dict(
                    title='Categories',  # X-axis title
                    title_font=dict(
                        size=14,  # X-axis title font size
                        color='#19105B'  # X-axis title color
                    ),
                    tickfont=dict(
                        size=12,  # X-axis tick font size
                        color='#19105B'  # X-axis tick color
                    ),
                ),
                yaxis=dict(
                    title='Values',  # Y-axis title
                    title_font=dict(
                        size=14,  # Y-axis title font size
                        color='#19105B'  # Y-axis title color
                    ),
                    tickfont=dict(
                        size=12,  # Y-axis tick font size
                        color='#19105B'  # Y-axis tick color
                    ),
                ),
                showlegend=True
            )

            st.plotly_chart(fig, theme="streamlit")

        get_chart_83992296()

if __name__ == '__main__':
    main()