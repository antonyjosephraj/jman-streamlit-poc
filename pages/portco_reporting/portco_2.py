import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
import plotly.graph_objects as go
import string
import random
import datetime as dt
from datetime import datetime
from pyxirr import xirr

def main():
    
    # Reading the CSS file
    with open('./styles/style.css') as f:
        css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='color: #19105B; padding:0;'>Portfolio Company 2</h1>", unsafe_allow_html=True)
    st.divider()

    # Header Buttons
    st.markdown('<div class="top-right"><button>Upload</button> <button>Download</button> </div>', unsafe_allow_html=True)

    # Investments
    investments = pd.read_csv('./inputs/investments_v2.csv')
    investments['Date of Investment'] = pd.to_datetime(investments['Date of Investment'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
    if 'investments_amount_pf2' not in ss:
        ss.investments_amount_pf2 = pd.DataFrame(investments)

    # Investments Details
    investments_details = pd.read_csv('./inputs/investments_details_v2.csv') 
    investments_details['Exit Date'] = pd.to_datetime(investments_details['Exit Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    if 'investments_data_pf2' not in ss:
        ss.investments_data_pf2 = pd.DataFrame(investments_details)

    if 'max_date_pf2' not in ss:
        max_date = investments_details['Exit Date'].max()
        ss.max_date_pf2 = datetime.strptime(max_date, '%Y-%m-%d').date()

    # Assumptions Calculations
    min_date = ss.investments_amount_pf2['Date of Investment'].min()
    investments_at_entry = ss.investments_amount_pf2['Investment at Entry'].sum()
    ss.investments_data_pf2['Exit Date'] = pd.to_datetime(ss.investments_data_pf2['Exit Date']).dt.date
    max_date = ss.investments_data_pf2['Exit Date'].max()
    max_date_str_pf2 = max_date.strftime('%Y-%m-%d')
    max_date = datetime.strptime(max_date_str_pf2, '%Y-%m-%d').date()
    ss.max_date_pf2 = max_date

    date_range = pd.date_range(start=min_date, end=max_date, freq='M')
    assumptions = pd.DataFrame(date_range, columns=['Date'])
    assumptions['Date'] = pd.to_datetime(assumptions['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    num_rows = assumptions.shape[0]
    sample_values = np.random.randint(1000, 3000, size=(num_rows, 3))
    mask = np.random.rand(*sample_values.shape) < 0.4
    sample_values[mask] = 0
    assumptions["Low Case"] = sample_values[:, 0]
    assumptions["Base Case"] = sample_values[:, 1]
    assumptions["High Case"] = sample_values[:, 2]
    assumptions["Comments"] = None

    assumptions.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]

    if 'assumptions_data_pf2' not in ss:
        ss.assumptions_data_pf2 = pd.DataFrame(assumptions)

    # Get Assumption Data
    def fetching_assumptions_data():

        min_date = ss.investments_amount_pf2['Date of Investment'].min()
        investments_at_entry = ss.investments_amount_pf2['Investment at Entry'].sum()
        ss.assumptions_data_pf2.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [0, 0, 0]

        max_date = ss.investments_data_pf2['Exit Date'].max()
        sample_data = ss.assumptions_data_pf2
        sample_data['Date'] = pd.to_datetime(sample_data['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        ss.max_date_pf2 = datetime.strptime(max_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()

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

        ss.assumptions_data_pf2.loc[0, ["Low Case" ,"Base Case" ,"High Case"]] = [ -investments_at_entry ,-investments_at_entry ,-investments_at_entry]

        investment_update = ss.assumptions_data_pf2

        low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
        base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
        high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()

        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
        ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)

    # Containers and columns    
    with st.container(border=True):
        
        # columns - 1
        col1, col2 = st.columns(2)

        with col1:

            if 'min_date_pf2' not in ss:
                investment_date = st.date_input('Investment Date', dt.date(2022, 7, 6), format="YYYY-MM-DD", min_value=None,  key='investment_min_date')
                ss.min_date_pf2 = investment_date
            
            else:
                # year, month, date = get_current_date(ss.min_date_pf2)
                investment_date = st.date_input('Investment Date2',  value=ss.min_date_pf2,  format="YYYY-MM-DD" )
                ss.min_date_pf2 = investment_date

            if ss.min_date_pf2 > ss.max_date_pf2:
                st.error('Please ensure that the Investment Date is before the Exit Date')
            else:
                ss.investments_amount_pf2.at[0, 'Date of Investment'] = ss.min_date_pf2
                # fetching_assumptions_data()
            
            input_col1, input_col2, input_col3 = st.columns(3)

            with input_col1:
                if 'lowcase_enddate_pf2' not in ss:
                    lowcase_enddate = st.date_input('Low Case Exit Date', dt.date(2023, 7, 16), format="YYYY-MM-DD")
                    ss.lowcase_enddate_pf2 = lowcase_enddate
                else:
                    lowcase_enddate = st.date_input('Low Case Exit Date', value=ss.lowcase_enddate_pf2, format="YYYY-MM-DD")
                    ss.lowcase_enddate_pf2 = lowcase_enddate

                if lowcase_enddate < ss.min_date_pf2:
                    ss.investments_data_pf2.at[0, 'Exit Date'] = ss.lowcase_enddate_pf2
                    st.error('Please ensure that the Investment Date is before the Exit Date1')
                else:
                    ss.lowcase_enddate_pf2 = lowcase_enddate
                    ss.investments_data_pf2.at[0, 'Exit Date'] = ss.lowcase_enddate_pf2
                    fetching_assumptions_data()
            
            with input_col2:
                if 'basecase_enddate_pf2' not in ss:
                    basecase_enddate = st.date_input('Base Case Exit Date', dt.date(2024, 8, 4), format="YYYY-MM-DD")
                    ss.basecase_enddate_pf2 = basecase_enddate
                else:
                    basecase_enddate = st.date_input('Base Case Exit Date', value=ss.basecase_enddate_pf2, format="YYYY-MM-DD")
                    ss.basecase_enddate_pf2 = basecase_enddate

                if basecase_enddate < ss.min_date_pf2:
                    ss.investments_data_pf2.at[1, 'Exit Date'] = ss.basecase_enddate_pf2
                    st.error('Please ensure that the Investment Date is before the Exit Date2')
                else:
                    ss.basecase_enddate_pf2 = basecase_enddate
                    ss.investments_data_pf2.at[1, 'Exit Date'] = ss.basecase_enddate_pf2
                    fetching_assumptions_data()

            with input_col3:

                if 'highcase_enddate_pf1' not in ss:
                    highcase_enddate = st.date_input('High Case Exit Date', dt.date(2025, 9, 29), format="YYYY-MM-DD")
                    ss.highcase_enddate_pf1 = highcase_enddate
                else:
                    highcase_enddate = st.date_input('High Case Exit Date', ss.highcase_enddate_pf1, format="YYYY-MM-DD")
                    ss.highcase_enddate_pf1 = highcase_enddate

                if highcase_enddate < ss.min_date_pf1:
                    ss.investments_data_pf1.at[2, 'Exit Date'] = ss.highcase_enddate_pf1
                    st.error('Please ensure that the Investment Date is before the Exit Date3')
                else:
                    ss.highcase_enddate_pf1 = highcase_enddate
                    ss.investments_data_pf1.at[2, 'Exit Date'] = ss.highcase_enddate_pf1
                    fetching_assumptions_data()
            
            st.markdown("<div class='empty-space'></div>", unsafe_allow_html=True)

            st.markdown("<h2 class='streamlit-tooltip'>Entry Metrics 📝<span class='tooltiptext'>Please input the entry metrics values</span></h2>", unsafe_allow_html=True)
            investments_edited_df = de(ss.investments_amount_pf2, use_container_width=True, width=800, height=80, hide_index=True, column_order=["Investment at Entry", "EBITDA at Entry", "Multiple at Entry"]) 

            st.markdown("<h2 class='streamlit-tooltip'>Scenario Assumptions 📝<span class='tooltiptext'>Please input the scenario assumptions</span></h2>", unsafe_allow_html=True)
            investments_details_v2 = de(ss.investments_data_pf2, use_container_width=True, height=150, hide_index=True, column_order=["Scenario", "Invested Amount", "EBITDA at Exit", "Multiple at Exit"],  disabled=["Scenario"])

        # Columns - 2
        column1, column2 = st.columns(2)

        with column1:
            st.markdown("<h2 class='streamlit-tooltip'>Cashflow Assumptions 📝 <span class='tooltiptext'>Please input the cashflow amounts</span></h2>", unsafe_allow_html=True)
            assumptions_edited_df_v2 = de(ss.assumptions_data_pf2,  use_container_width=True, height=880, hide_index=True, disabled=["Date"])


        ebitda_entry_value = ss.investments_amount_pf2['EBITDA at Entry'].sum()
        ebitda_multiple_entry_value = ss.investments_amount_pf2['Multiple at Entry'].sum()
        column_values_list = investments_details_v2['Scenario'].tolist()
        column_values_values = investments_details_v2['EBITDA at Exit'].tolist()
        column_values_values2 = investments_details_v2['Multiple at Exit'].tolist()

        editda_multiple = {
            'Calc': ['ARR /Rev /EBITDA', 'Multiple'],
            'Entry': [ebitda_entry_value, ebitda_multiple_entry_value]
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

            # a = int(arr_rev_ebitda * multiple)
            # b = int(net_debt) + int(cash_flow_adj)
            # result = a + b
            result = arr_rev_ebitda * (multiple + net_debt + cash_flow_adj)
            return result

        def calculate_value(df, case):
            equity = df.loc[df['Calc'] == 'Equity', case].values[0]
            ownership = df.loc[df['Calc'] == 'Ownership %', case].values[0]

            equity = 1 if equity == None else equity
            ownership = 1 if ownership == None else ownership
            return (int(equity) * (int(ownership) / 100)) 


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
            st.markdown("<h2 class='streamlit-tooltip'>Valuation Assumptions<span class='tooltiptext'>View the valuation assumptions values</span></h2>", unsafe_allow_html=True)

            with st.container(height=400, border=True):
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["EBITDA", "Cash Flow", "Equity", "Ownership", "Value & Invt", "Multiple"])
                
                with tab1:
                    st.markdown("<div style='text-align: center;'><h3 text class='streamlit-tooltip'>EBITDA <span class='tooltiptext'>View the EDITDA values</span></h3></div>", unsafe_allow_html=True)
                    editda_multiple_df_pf2_styled_df = ss.editda_multiple_df_pf2
                    st.markdown(editda_multiple_df_pf2_styled_df.style.hide(axis="index").set_table_attributes('style="margin: 0 auto;"').to_html(), unsafe_allow_html=True)
                        
                with tab2:
                    st.markdown("<div style='text-align: center;'><h3 class='streamlit-tooltip'>Cash Flow 📝 <span class='tooltiptext'>Please input the cashflow calues</span></h3></div>", unsafe_allow_html=True)
                    netdebt_and_cashflow_edited_df_pf2 = de(ss.netdebt_and_cashflow_df_pf2, width=550, height=110, hide_index=True, disabled=["Calc"])

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
                    st.markdown("<div style='text-align: center;'><h3 class='streamlit-tooltip'>Equity <span class='tooltiptext'>View the equity values</span></h3></div>", unsafe_allow_html=True)
                    equity_df_pf2_styled_df = ss.equity_df_pf2
                    st.markdown(equity_df_pf2_styled_df.style.hide(axis="index").set_table_attributes('style="margin: 0 auto;"').to_html(), unsafe_allow_html=True)

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
                    st.markdown("<div style='text-align: center;'><h3 class='streamlit-tooltip'>Ownership 📝<span class='tooltiptext'>Please input the ownership values</span></h3></div>", unsafe_allow_html=True)
                    ownership_edited_df_pf2 = de(ss.ownership_df_pf2, width=550, height=70, hide_index=True, disabled=["Calc"])
                    
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
                    st.markdown("<div style='text-align: center;'><h3 class='streamlit-tooltip'>Value & Investments <span class='tooltiptext'>View the investment values</span></h3></div>", unsafe_allow_html=True)
                    value_and_investment_df_pf2_styled_df = ss.value_and_investment_df_pf2
                    st.markdown(value_and_investment_df_pf2_styled_df.style.hide(axis="index").set_table_attributes('style="margin: 0 auto;"').to_html(), unsafe_allow_html=True)

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
                ss.money_multiple_df_pf2 = money_multiple_df
                
                with tab6:
                    st.markdown("<div style='text-align: center;'><h3 class='streamlit-tooltip'>Money Multiple <span class='tooltiptext'>View the money multiple values</span> </h3></div>", unsafe_allow_html=True)
                    money_multiple_df_pf2_styled_df = ss.money_multiple_df_pf2
                    st.markdown(money_multiple_df_pf2_styled_df.style.hide(axis="index").set_table_attributes('style="margin: 0 auto;"').to_html(), unsafe_allow_html=True)

        money_multiple_value = money_multiple_df.iloc[0].tolist()

        # IRR
        df3 = assumptions_edited_df_v2

        df3['Low Case'] = pd.to_numeric(df3['Low Case'], errors='coerce')
        df3['Base Case'] = pd.to_numeric(df3['Base Case'], errors='coerce')
        df3['High Case'] = pd.to_numeric(df3['High Case'], errors='coerce')

        # # Calculate days from the start date for each cash flow
        df3['Date'] = pd.to_datetime(df3['Date'])

        # Calculate IRR based on adjusted cash flows
        low_case_irr =xirr(df3['Date'], df3['Low Case'])
        base_case_irr =xirr(df3['Date'], df3['Base Case'])
        high_case_irr =xirr(df3['Date'], df3['High Case'])

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
            st.markdown("<h2  class='streamlit-tooltip'>Returns Calculations<span class='tooltiptext'>View the return calculations value</span></h2>", unsafe_allow_html=True)
            st.write(revenue_return_pf2_styled_df.hide(axis="index").set_table_attributes('style="height:160px;"').to_html(), unsafe_allow_html=True)
    

        if st.button("Submit"):

            # Update the investment Amount
                if not ss.investments_amount_pf2.equals(investments_edited_df):
                    ss.investments_amount_pf2 = investments_edited_df
                    fetching_assumptions_data()

                if not ss.investments_data_pf2.equals(investments_details_v2):
                    ss.investments_data_pf2 = investments_details_v2
                    fetching_assumptions_data()
                
                if not ss.assumptions_data_pf2.equals(assumptions_edited_df_v2):
                    investment_update = assumptions_edited_df_v2

                    low_case_sum_of_negatives = investment_update[investment_update['Low Case'] < 0]['Low Case'].sum()
                    base_case_sum_of_negatives = investment_update[investment_update['Base Case'] < 0]['Base Case'].sum()
                    high_case_sum_of_negatives = investment_update[investment_update['High Case'] < 0]['High Case'].sum()
                
                    ss.assumptions_data_pf2 = assumptions_edited_df_v2
                    ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Low Case', 'Invested Amount'] = abs(low_case_sum_of_negatives)
                    ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'Base Case', 'Invested Amount'] = abs(base_case_sum_of_negatives)
                    ss.investments_data_pf2.loc[ss.investments_data_pf2['Scenario'] == 'High Case', 'Invested Amount'] = abs(high_case_sum_of_negatives)
                
                if not ss.netdebt_and_cashflow_df_pf2.equals(netdebt_and_cashflow_edited_df_pf2):
                    ss.netdebt_and_cashflow_df_pf2 =netdebt_and_cashflow_edited_df_pf2
                
                if not ss.ownership_df_pf2.equals(ownership_edited_df_pf2):
                    ss.ownership_df_pf2 = ownership_edited_df_pf2
                
                rr()


    with st.container(border=True):
        st.markdown("<div style='text-align: center;'><h2 style='color: #19105B; font-size:28px;'class='streamlit-tooltip'>Valuation Waterfall <span class='tooltiptext'>View the PortCo 1 Valuation Waterfall chart</span></h2></div>", unsafe_allow_html=True)

        # Waterfall Data 
        waterfall_data_pf2 = pd.concat([ss.editda_multiple_df_pf2, ss.netdebt_and_cashflow_df_pf2, ss.equity_df_pf2, ss.ownership_df_pf2, ss.value_and_investment_df_pf2, ss.money_multiple_df_pf2], ignore_index=True)
        investments_at_entry_amount = ss.investments_amount_pf2['Investment at Entry'].sum()

        waterfall_options_pf2 = ['Low Case', 'Base Case', 'High Case']
        selected_option_pf2 = st.selectbox('Select a Scenario for PortCo 2:', waterfall_options_pf2)
        ss.selected_option_pf2 = selected_option_pf2

        ebitda_value = 0

        if ss.selected_option_pf2 in waterfall_data_pf2.columns:
            case_value = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'ARR /Rev /EBITDA', ss.selected_option_pf2].values
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

            ebitda_value = (actual_entry_value * total_value) * (int(ownership_data_v2) / 100)

        multiple_growth = 0
        if ss.selected_option_pf2 in waterfall_data_pf2.columns:
            case_value1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Multiple', 'Entry'].values
            case_value2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Multiple', ss.selected_option_pf2].values
            multi_minus_value = int(case_value2) - int(case_value1)
            total_value1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'ARR /Rev /EBITDA', ss.selected_option_pf2].values
            total_value2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Net Debt', 'Entry'].values

            if total_value1 == None:
                total_value1 = 0
            if total_value2 == None:
                total_value2 = 0

            total_value3 = int(total_value1) + int(total_value2)
            ownership_data_v2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Ownership %', ss.selected_option_pf2].values[0]
            if ownership_data_v2 == None:
                ownership_data_v2 = 0
            multiple_growth = (multi_minus_value * total_value3) * (int(ownership_data_v2)/ 100)

        asset_value_v1 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'Low Case'].values
        asset_value_v2 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'Base Case'].values
        asset_value_v3 = waterfall_data_pf2.loc[waterfall_data_pf2['Calc'] == 'Value', 'High Case'].values

        asset_value_total = int(asset_value_v1) + int(asset_value_v2) + int(asset_value_v3)

        financial_engineering = (investments_at_entry_amount + ebitda_value + multiple_growth ) - asset_value_total

        waterfall_data_flow_pf2 = {
            'Category': ['Value at investment', 'EBITDA growth', 'Multiple growth', 'Financial engineering', 'Asset value'],
            'Values': [investments_at_entry_amount, ebitda_value, multiple_growth, financial_engineering, asset_value_total  ]
        }

        waterfall_data_flow_df_pf2 = pd.DataFrame(waterfall_data_flow_pf2)

        with st.form("my_form"):

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
                # title="Portfolio Insights Dashboard",
                # title_font=dict(
                #     size=20,  # Title font size
                #     color='#FF6196'  # Title color
                # ),
                xaxis=dict(
                    # title='Categories',  # X-axis title
                    title_font=dict(
                        size=14,  # X-axis title font size
                        color='#19105B'  # X-axis title color
                    ),
                    tickfont=dict(
                        size=14,  # X-axis tick font size
                        color='#19105B'  # X-axis tick color
                    ),
                ),
                yaxis=dict(
                    title='£',  # Y-axis title
                    title_font=dict(
                        size=18,  # Y-axis title font size
                        color='#19105B'  # Y-axis title color
                    ),
                    tickfont=dict(
                        size=14,  # Y-axis tick font size
                        color='#19105B'  # Y-axis tick color
                    ),
                ),
                showlegend=True
            )

            st.plotly_chart(fig, theme="streamlit")
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.write("slider")

if __name__ == '__main__':
    main()