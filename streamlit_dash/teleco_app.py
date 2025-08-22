import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Streamlit layout and style
st.set_page_config(layout="wide")
sns.set(style="whitegrid")

# Load data
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("telecom_churned_data.csv")
    df['ChurnBinary'] = df['Churn'].map({'No': 0, 'Yes': 1})
    df['ChargeRange'] = pd.cut(df['MonthlyCharges'], bins=[0, 20, 40, 60, 80, 100, 120],
                               labels=["0-20", "21-40", "41-60", "61-80", "81-100", "101-120"])
    return df

df = load_data()

# Page title and metrics
st.title("\U0001F4CA Telco Customer Churn Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(df):,}")
col2.metric("Churn Rate", f"{df['ChurnBinary'].mean() * 100:.2f}%")
col3.metric("Avg. Monthly Charges", f"${df['MonthlyCharges'].mean():.2f}")

# Churn distribution and descriptive stats
col1, col2 = st.columns(2)
with col1:
    st.subheader("Churn Distribution")
    churn_summary = pd.DataFrame({
        "Count": df["Churn"].value_counts(),
        "Percentage": (df["Churn"].value_counts(normalize=True) * 100).round(2)
    })
    st.dataframe(churn_summary)

with col2:
    st.subheader("Descriptive Statistics")
    st.dataframe(df[['CitizensStatus', 'tenure', 'MonthlyCharges', 'TotalCharges']].describe())

# Spread percentage tables across layout columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("\U0001F4DD Churn by Gender")
    gender_count = df['gender'].value_counts()
    churn_gender_yes = df[df['Churn'] == 'Yes']['gender'].value_counts()
    churn_gender_no = df[df['Churn'] == 'No']['gender'].value_counts()
    gender_table = pd.DataFrame({'Count': gender_count, 'Churned': churn_gender_yes, 'Not Churned': churn_gender_no})
    st.dataframe(gender_table)

with col2:
    st.subheader("\U0001F4DD Churn by Citizenship")
    citizenship_total = df['CitizensStatus'].value_counts()
    citizenship_churned = df[df['Churn'] == 'Yes']['CitizensStatus'].value_counts()
    citizenship_percent = (citizenship_churned / citizenship_total * 100).round(2)
    citizenship_table = pd.DataFrame({'Total': citizenship_total, 'Churned': citizenship_churned, 'Percentage%': citizenship_percent})
    st.dataframe(citizenship_table)

with col3:
    st.subheader("\U0001F4DD Churn by Contract")
    contract_total = df['Contract'].value_counts()
    contract_churned = df[df['Churn'] == 'Yes']['Contract'].value_counts()
    contract_percent = (contract_churned / contract_total * 100).round(2)
    contract_table = pd.DataFrame({'Total': contract_total, 'Churned': contract_churned, 'Percentage%': contract_percent})
    st.dataframe(contract_table)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("\U0001F4DD Churn by Tech Support")
    tech_total = df['TechSupport'].value_counts()
    tech_churned = df[df['Churn'] == 'Yes']['TechSupport'].value_counts()
    tech_percent = (tech_churned / tech_total * 100).round(2)
    tech_table = pd.DataFrame({'Total': tech_total, 'Churned': tech_churned, 'Percentage%': tech_percent})
    st.dataframe(tech_table)

with col2:
    st.subheader("\U0001F4DD Churn by Internet Service")
    internet_total = df['InternetService'].value_counts()
    internet_churned = df[df['Churn'] == 'Yes']['InternetService'].value_counts()
    internet_percent = (internet_churned / internet_total * 100).round(2)
    internet_table = pd.DataFrame({'Total': internet_total, 'Churned': internet_churned, 'Percentage%': internet_percent})
    st.dataframe(internet_table)

with col3:
    st.subheader("\U0001F4DD Churn by Payment Method")
    pay_total = df['PaymentMethod'].value_counts()
    pay_churned = df[df['Churn'] == 'Yes']['PaymentMethod'].value_counts()
    pay_percent = (pay_churned / pay_total * 100).round(2)
    pay_table = pd.DataFrame({'Total': pay_total, 'Churned': pay_churned, 'Percentage%': pay_percent})
    st.dataframe(pay_table)

# Subplots
st.subheader("\U0001F50D Churn Analysis - Key Factors")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.tight_layout(pad=4.0)

sns.countplot(data=df, x='Churn', hue='Churn', ax=axes[0, 0], palette="Set1")
axes[0, 0].set_title("Customers Churn Count")

sns.countplot(data=df, x='CitizensStatus', hue='Churn', ax=axes[0, 1], palette="Set2")
axes[0, 1].set_title("Churn by Citizenship")

sns.countplot(data=df, x='Contract', hue='Churn', ax=axes[0, 2], palette="Set3")
axes[0, 2].set_title("Churn by Contract")

sns.countplot(data=df, x='TechSupport', hue='Churn', ax=axes[1, 0])
axes[1, 0].set_title("Churn by Tech Support")

sns.countplot(data=df, x='InternetService', hue='Churn', ax=axes[1, 1], palette="Paired")
axes[1, 1].set_title("Churn by Internet Service")

sns.boxplot(data=df, x='Churn', y='MonthlyCharges', hue='Churn', palette='Set1', ax=axes[1, 2])
axes[1, 2].set_title('MonthlyCharges vs Churn')
axes[1, 2].tick_params(axis='x', rotation=45)

st.pyplot(fig)

# Monthly Charge Range Table and Plot
st.subheader("\U0001F4DD Churn by Monthly Charge Range")
col1, col3 = st.columns([1, 1])
with col1:
    ChargeRange_count = df['ChargeRange'].value_counts(sort=False)
    ChargeRange_index = ChargeRange_count.index
    churned_by_range = df[df['Churn'] == 'Yes']['ChargeRange'].value_counts(sort=False)
    percentage_range = (churned_by_range / ChargeRange_count * 100).round(2)
    ChargeRange_summary = pd.DataFrame({'Range': ChargeRange_index, 'count': ChargeRange_count, 'Churned': churned_by_range, 'percentage%': percentage_range})
    ChargeRange_summary.index = range(1, len(ChargeRange_summary) + 1)
    st.dataframe(ChargeRange_summary)

with col3:
    fig_range = plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='ChargeRange', hue='Churn', palette='Dark2')
    plt.title('Churn by Monthly Charge Range')
    plt.xticks(rotation=45)
    st.pyplot(fig_range)

# Side-by-side: Regression Plot and Heatmap
col1, col2, col3 = st.columns([1, 0.1, 1])
with col1:
    st.subheader("\U0001F4C8 Churn Probability vs. Monthly Charges")
    fig2 = plt.figure(figsize=(6, 3))
    sns.regplot(x='MonthlyCharges', y='ChurnBinary', data=df, ci=None, scatter_kws={'alpha':0.2})
    plt.title('Churn Probability vs. Monthly Charges')
    plt.ylabel('Churn Probability')
    plt.xlabel('Monthly Charges')
    st.pyplot(fig2)

with col3:
    st.subheader("\U0001F525 Heatmap: Churn % by TotalCharges & Contract")
    step = 500
    bins = list(range(0, 9500, step))
    labels = [f"{i}-{i+step}" for i in bins[:-1]]
    df['TotalChargeRange'] = pd.cut(df['TotalCharges'], bins=bins, labels=labels)

    count_table = df.pivot_table(index='TotalChargeRange', columns='Contract', values='customerID', aggfunc='count', observed=True)
    churn_table = df.pivot_table(index='TotalChargeRange', columns='Contract', values='Churn', aggfunc=lambda x: (x == 'Yes').mean(), observed=True) * 100
    churn_table.columns = [f"{col} Churn %" for col in churn_table.columns]
    final_table = pd.concat([count_table, churn_table], axis=1).round(1)

    churn_pct = final_table[[col for col in final_table.columns if 'Churn' in col]]
    churn_pct.columns = [col.replace(' Churn %', '') for col in churn_pct.columns]

    fig3 = plt.figure(figsize=(7, 6))
    sns.heatmap(churn_pct, annot=True, fmt=".1f", cmap="coolwarm")
    plt.title("Churn % Heatmap by Contract Type and TotalChargeRange")
    plt.ylabel("TotalChargeRange")
    plt.xlabel("Contract Type")
    st.pyplot(fig3)

# Total Charges Summary in narrow column
col5, _, _ = st.columns([1, 0.01, 0.01])
with col5:
    st.subheader("\U0001F4DD TotalCharges Summary")
    total_charge_summary = pd.DataFrame({
        'Statistic': ['Minimum', 'Maximum'],
        'TotalCharges': [df['TotalCharges'].min(), df['TotalCharges'].max()]
    })
    st.dataframe(total_charge_summary)

# Footer
st.markdown("---")
st.markdown("Built by [Chile Okwuodu] | © 2025")
