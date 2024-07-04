import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
from streamlit import session_state as ss, data_editor as de, rerun as rr
import datetime
import matplotlib.pyplot as plt
# import seaborn as sns



def main(): 

    applyCss = """
    <style> 

    .st-emotion-cache-4uzi61 {
        border: 2px solid #19105B;
        border-radius: 10px;
        padding: 20px;
    }

    [data-testid="stAppViewBlockContainer"]{
        padding:30px;
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
    </style>
    """
    st.markdown(applyCss, unsafe_allow_html=True)

    st.markdown("<h1 style='color: #19105B;padding:0;'>Aggregated Fund Summary</h1>", unsafe_allow_html=True)
    st.divider()

    # Collecting All Data

    data_investments_details_pf1 = ss.investments_data_pf1
    data_investments_amount_pf1 = ss.investments_amount_pf1
    data_revenue_return_pf1 = ss.revenue_return_pf1

    data_investments_details_pf2 = ss.investments_data_pf2
    data_investments_amount_pf2 = ss.investments_amount_pf2
    data_revenue_return_pf2 = ss.revenue_return_pf2

    data_investments_details_pf3 = ss.investments_data_pf3
    data_investments_amount_pf3 = ss.investments_amount_pf3
    data_revenue_return_pf3 = ss.revenue_return_pf3

    data = {'Name': ['Portco 1', 'Portco 2', 'Portco 3']}
    df = pd.DataFrame(data)

    with st.container(border=True):
        st.markdown('<div class="custom-container1">', unsafe_allow_html=True)

        st.markdown("<h5 style='color: #19105B;padding:0;'>Select a Scenario for Each PortCo</h5>", unsafe_allow_html=True)
        st.markdown("<div style='marging:2px 0;'></div>", unsafe_allow_html=True)

        # Columns - 1  
        col1, col2, col3 = st.columns(3)

        with col1:
            portco1_options = ['Low Case', 'Base Case', 'High Case']
            portco1_selected_option = st.selectbox('PortCo 1:', portco1_options)
            ss.portco1_selected_option = portco1_selected_option


        with col2:
            portco2_options = ['Base Case', 'Low Case', 'High Case' ]
            portco2_selected_option = st.selectbox('PortCo 2:', portco2_options)
            ss.portco2_selected_option = portco2_selected_option


        with col3:
            portco3_options = ['High Case', 'Low Case', 'Base Case']
            portco3_selected_option = st.selectbox('PortCo 3:', portco3_options)
            ss.portco3_selected_option = portco3_selected_option


        # col11= st.columns(1)


        # Add a column with a dropdown list
        for i in df.index:
            if i  == 0:
                for pf1 in data_investments_details_pf1.index:
                    if ss.portco1_selected_option == data_investments_details_pf1.at[pf1, 'Scenario']:
                        df.at[0, 'Scenario'] = ss.portco1_selected_option
                        df.at[0, 'Date of Investment'] = data_investments_amount_pf1.iloc[0]['Date of Investment']
                        df.at[0, 'Invested Amount'] = data_investments_details_pf1.at[pf1, 'Invested Amount']
                        df.at[0, 'EBITDA at Entry'] = data_investments_amount_pf1.iloc[0]['EBITDA at entry']
                        df.at[0, 'EBITDA at Exit'] = data_investments_details_pf1.at[pf1, 'EBITDA at Exit']
                        df.at[0, 'Multiple at entry'] = data_investments_amount_pf1.iloc[0]['Multiple at Entry']
                        df.at[0, 'Multiple at Exit'] = data_investments_details_pf1.at[pf1, 'Multiple at Exit']
                        df.at[0, 'Exit Date'] = data_investments_details_pf1.at[pf1, 'Exit Date']
                        if ss.portco1_selected_option == 'Low Case':
                            df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[0, 'Return (calculated)']
                            df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[0, 'IRR (calculated)']

                        if ss.portco1_selected_option == 'Base Case':
                            df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[1, 'Return (calculated)']
                            df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[1, 'IRR (calculated)']

                        if ss.portco1_selected_option == 'High Case':
                            df.at[0, 'Return (calculated)'] = data_revenue_return_pf1.at[2, 'Return (calculated)']
                            df.at[0, 'IRR (calculated)'] = data_revenue_return_pf1.at[2, 'IRR (calculated)']

            if i  == 1:
                for pf1 in data_investments_details_pf2.index:
                    if ss.portco2_selected_option == data_investments_details_pf2.at[pf1, 'Scenario']:
                        df.at[1, 'Scenario'] = ss.portco2_selected_option
                        df.at[1, 'Date of Investment'] = data_investments_amount_pf2.iloc[0]['Date of Investment']
                        df.at[1, 'Invested Amount'] = data_investments_details_pf2.at[pf1, 'Invested Amount']
                        df.at[1, 'EBITDA at Entry'] = data_investments_amount_pf2.iloc[0]['EBITDA at entry']
                        df.at[1, 'EBITDA at Exit'] = data_investments_details_pf2.at[pf1, 'EBITDA at Exit']
                        df.at[1, 'Multiple at entry'] = data_investments_amount_pf2.iloc[0]['Multiple at Entry']
                        df.at[1, 'Multiple at Exit'] = data_investments_details_pf2.at[pf1, 'Multiple at Exit']
                        df.at[1, 'Exit Date'] = data_investments_details_pf2.at[pf1, 'Exit Date']
                        if ss.portco2_selected_option == 'Low Case':
                            df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[0, 'Return (calculated)']
                            df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[0, 'IRR (calculated)']

                        if ss.portco2_selected_option == 'Base Case':
                            df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[1, 'Return (calculated)']
                            df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[1, 'IRR (calculated)']

                        if ss.portco2_selected_option == 'High Case':
                            df.at[1, 'Return (calculated)'] = data_revenue_return_pf2.at[2, 'Return (calculated)']
                            df.at[1, 'IRR (calculated)'] = data_revenue_return_pf2.at[2, 'IRR (calculated)']

            
            if i  == 2:
                for pf1 in data_investments_details_pf3.index:
                    if ss.portco3_selected_option == data_investments_details_pf3.at[pf1, 'Scenario']:
                        df.at[2, 'Scenario'] = ss.portco3_selected_option
                        df.at[2, 'Date of Investment'] = data_investments_amount_pf3.iloc[0]['Date of Investment']
                        df.at[2, 'Invested Amount'] = data_investments_details_pf3.at[pf1, 'Invested Amount']
                        df.at[2, 'EBITDA at Entry'] = data_investments_amount_pf3.iloc[0]['EBITDA at entry']
                        df.at[2, 'EBITDA at Exit'] = data_investments_details_pf3.at[pf1, 'EBITDA at Exit']
                        df.at[2, 'Multiple at entry'] = data_investments_amount_pf3.iloc[0]['Multiple at Entry']
                        df.at[2, 'Multiple at Exit'] = data_investments_details_pf3.at[pf1, 'Multiple at Exit']
                        df.at[2, 'Exit Date'] = data_investments_details_pf3.at[pf1, 'Exit Date']
                        if ss.portco3_selected_option == 'Low Case':
                            df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[0, 'Return (calculated)']
                            df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[0, 'IRR (calculated)']

                        if ss.portco3_selected_option == 'Base Case':
                            df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[1, 'Return (calculated)']
                            df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[1, 'IRR (calculated)']

                        if ss.portco3_selected_option == 'High Case':
                            df.at[2, 'Return (calculated)'] = data_revenue_return_pf3.at[2, 'Return (calculated)']
                            df.at[2, 'IRR (calculated)'] = data_revenue_return_pf3.at[2, 'IRR (calculated)']
        


        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Total of Fund Level:</h2>", unsafe_allow_html=True)



        st.write(df)
        df1 = df
        df1['Return (calculated)'] = pd.to_numeric(df1['Return (calculated)'].str.replace('x', ''))

        total_investment_amout = df1['Invested Amount'].sum()
        total_return_amount = df1['Return (calculated)'].sum()
        total_return_amount_v2 = str(total_return_amount) + ' x'

        fun_level_data = {
            'Invested Amount': [total_investment_amout],
            'Return (calculated)': [total_return_amount_v2]
        }
        
        fun_level_data_df = pd.DataFrame(fun_level_data)

        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Total of Fund Level - Amount:</h2>", unsafe_allow_html=True)

        st.write(fun_level_data_df)

        st.markdown('</div>', unsafe_allow_html=True)

    # Get Assumptions Data
    assumptions_data_portco1 = ss.assumptions_data_pf1
    assumptions_data_portco2 = ss.assumptions_data_pf2
    assumptions_data_portco3 = ss.assumptions_data_pf3

    today = pd.Timestamp(datetime.datetime.now().date())

    def sum_positive_values(df_subset, option):
        if option in df_subset.columns:
            positive_sum = df_subset[[option]].apply(lambda x: x[x > 0].sum(), axis=1).sum()
            return positive_sum

    def calculation_value(df, option):

        df['Date1'] = pd.to_datetime(df['Date'])
        df['year'] = df['Date1'].dt.year

        past_values = df[df['Date1'] < today]
        future_values = df[df['Date1'] >= today]

        years = sorted(df['year'].unique())  # List of all years in the data
        df = df.drop(columns=['Date1', 'year'], inplace=True)

        past_value = []
        future_value = []

        for year in years:
            past_sum = sum_positive_values(past_values[past_values['year'] == year], option)
            future_sum = sum_positive_values(future_values[future_values['year'] == year], option)
            past_value.append(past_sum)
            future_value.append(future_sum)

        return_data = pd.DataFrame({
            'year': years,
            'past_value': past_value,
            'future_value': future_value
        })
        
        return return_data
        
    df1 = calculation_value(assumptions_data_portco1, ss.portco1_selected_option)
    df2 = calculation_value(assumptions_data_portco2, ss.portco2_selected_option)
    df3 = calculation_value(assumptions_data_portco3, ss.portco3_selected_option)

    def calculation_investment(df, option):
        df['Date1'] = pd.to_datetime(df['Date'])

        first_row = df.iloc[0]
        year = [first_row['Date1'].year]
        value = 0
        if option in df.columns:
            value = df[[option]].apply(lambda x: x[x < 0].sum(), axis=1).sum()

        df = df.drop(columns=['Date1'], inplace=True)

        return_data = pd.DataFrame({
            'year': year,
            'investment': value
        })
        return return_data
    
    in_df1 = calculation_investment(assumptions_data_portco1, ss.portco1_selected_option)
    in_df2 = calculation_investment(assumptions_data_portco2, ss.portco2_selected_option)
    in_df3 = calculation_investment(assumptions_data_portco3, ss.portco3_selected_option)

    # Merge the dataframes on 'id' column
    merged_df = pd.merge(df1, df2, on='year', how='outer')
    merged_df = pd.merge(merged_df, df3, on='year', how='outer')
    merged_df['past_value'] = merged_df['past_value_x'].fillna(0) + merged_df['past_value_y'].fillna(0) + merged_df['past_value'].fillna(0)
    merged_df['future_value'] = merged_df['future_value_x'].fillna(0) + merged_df['future_value_y'].fillna(0) + merged_df['future_value'].fillna(0)

    merged_df_v2 = merged_df[['year', 'past_value', 'future_value']]

    in_merged_df = pd.merge(in_df1, in_df2, on='year', how='outer')
    in_merged_df = pd.merge(in_merged_df, in_df3, on='year', how='outer')
    in_merged_df['investment'] = in_merged_df['investment_x'].fillna(0) + in_merged_df['investment_y'].fillna(0) + in_merged_df['investment'].fillna(0)

    in_merged_df_v2 = in_merged_df[['year', 'investment']]

    fund_level_report_df =  pd.merge(merged_df_v2, in_merged_df_v2, on='year', how='outer')
    fund_level_report_df['investment'] = fund_level_report_df['investment'].fillna(0)

    fund_level_report_df_v2 = fund_level_report_df
    fund_level_report_df_v2['Year'] = fund_level_report_df_v2['year']
    fund_level_report_df_v2['Invested Capital'] = fund_level_report_df_v2['investment']
    fund_level_report_df_v2['Distributions'] = fund_level_report_df_v2['past_value']
    fund_level_report_df_v2['Residual Value'] = fund_level_report_df_v2['future_value']
    fund_level_report_df_v2['Asset Value'] = (fund_level_report_df_v2['past_value'] + fund_level_report_df_v2['future_value'])
    fund_level_report_df_v2['Total Returns'] = (fund_level_report_df_v2['past_value'] + fund_level_report_df_v2['future_value']) + fund_level_report_df_v2['investment']

    fund_level_report_df_v3 = fund_level_report_df_v2[['Year', 'Invested Capital', 'Asset Value', 'Distributions', 'Residual Value', 'Total Returns']]

    fund_level_report_df_v4 = fund_level_report_df_v3[['Invested Capital', 'Distributions', 'Asset Value', 'Residual Value']]
    fund_level_report_df_v4['Invested Capital'] = fund_level_report_df_v4['Invested Capital'].abs()
    
    sum_invested_captital_amount = fund_level_report_df_v4['Invested Capital'].sum()
    sum_asset_value_amount = fund_level_report_df_v4['Asset Value'].sum()
    
    fund_level_report_df_v5 = pd.DataFrame({
            'Category': ['Invested Capital', 'Asset Value'],
            'Values': [sum_invested_captital_amount, sum_asset_value_amount]
    })

    with st.container(border=True):

        # st.markdown("<div style='background-color: #19105B; padding:0.3px; marging:5px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #19105B; font-size:28px;'>Agg Fun Summary Chart:</h2>", unsafe_allow_html=True)
        st.markdown("<div style='marging:5px 0;'></div>", unsafe_allow_html=True)

        # Columns - 2:
        col1, col2 = st.columns(2)

        with col1:
            colors = ['#19105B', '#FF6196']
            
            fig, ax = plt.subplots(figsize=(9.5, 6))
            bin_width = 0.3

            ax.bar(fund_level_report_df_v5['Category'], fund_level_report_df_v5['Values'], color=colors, width=bin_width)

            # Customize labels and title
            ax.set_xlabel('Fund Level Categories', color='#19105B', fontsize=10)
            ax.set_ylabel('Fund Level Values', color='#19105B', fontsize=10)
            ax.set_title('Bar Chart with Fund Level Data', color='#FF6196', fontsize=10)

            ax.tick_params(axis='x', labelsize=7, labelcolor='#19105B')
            ax.tick_params(axis='y', labelsize=7, labelcolor='#19105B')

            ax.grid(True, axis='y', linestyle='-', color='#19105B', alpha=0.1)  # Change axis to 'x' or 'both' if needed
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # ax.spines['bottom'].set_visible(False)
            # ax.spines['left'].set_visible(False)

            # Show plot in Streamlit
            st.pyplot(fig)



            # st.bar_chart(fund_level_report_df_v5, x="Index", y=['Invested Capital', 'Asset Value'])

        with col2:


            # # Create the bar chart
            fig1, ax1 = plt.subplots(figsize=(9, 6))

            unique_years = fund_level_report_df_v3['Year'].apply(int).unique()
            
            # Create stacked bars
            ax1.bar(fund_level_report_df_v3['Year'], fund_level_report_df_v3['Invested Capital'], color='#19105B')
            ax1.bar(fund_level_report_df_v3['Year'], fund_level_report_df_v3['Distributions'], color='#3411A3')
            ax1.bar(fund_level_report_df_v3['Year'], fund_level_report_df_v3['Residual Value'], color='#FF6196')

            # Plot the net values line on the same x-axis
            ax2 = ax1.twinx()
            ax2.plot(fund_level_report_df_v3['Year'], fund_level_report_df_v3['Total Returns'], color='b', marker='o')
            
            # Synchronize the y-axis limits
            ax2.set_ylim(ax1.get_ylim())
            # ax2.set_ylim(bottom=0)

            
            # Add labels and title
            ax1.set_xlabel('Categories', color='#19105B', fontsize=10)
            ax1.set_ylabel('Bar Values', color='#19105B', fontsize=10)
            # ax2.set_ylabel('Net Values', color='#19105B', fontsize=10)
            plt.title('Stacked Bar Chart with Net Values Line Graph', color='#FF6196', fontsize=10)
            

            plt.xticks(unique_years)
            # Add legend
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')

            ax1.tick_params(axis='x', labelsize=7, labelcolor='#19105B')
            ax1.tick_params(axis='y', labelsize=7, labelcolor='#19105B')
            ax2.tick_params(axis='y', labelsize=0)

            ax2.grid(True, axis='y', linestyle='-', color='#19105B', alpha=0.1)  # Change axis to 'x' or 'both' if needed
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            # ax1.spines['bottom'].set_visible(False)
            # ax1.spines['left'].set_visible(False)

            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            # ax2.spines['bottom'].set_visible(False)
            # ax2.spines['left'].set_visible(False)
            # Show the plot
            st.pyplot(fig1)

if __name__ == '__main__':
    main()