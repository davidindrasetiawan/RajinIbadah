import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set page config
st.set_page_config(page_title="Commodity Price Analysis", layout="wide")

@st.cache_data
def load_and_preprocess_data():
    # Load data
    file_path = '/content/Tabel Harga Berdasarkan Daerah JAWA TENGAH.xlsx'
    df = pd.read_excel(file_path)
    
    # Preprocessing steps
    if 'No' in df.columns:
        df = df.drop(columns=['No'])

    # Melt to long format
    df_melted = df.melt(id_vars=['Komoditas (Rp)'], var_name='Date', value_name='Price')

    # Clean 'Price' column
    df_melted['Price'] = df_melted['Price'].astype(str).str.replace(',', '', regex=False)
    df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')

    # Clean 'Date' column
    df_melted['Date'] = df_melted['Date'].astype(str).str.replace(' ', '')
    df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%d/%m/%Y', errors='coerce')

    # Drop NaNs
    df_melted = df_melted.dropna(subset=['Price', 'Date'])

    # Feature Engineering
    df_melted['Date_Ordinal'] = df_melted['Date'].apply(lambda x: x.toordinal())
    df_melted['Komoditas_Code'] = df_melted['Komoditas (Rp)'].astype('category').cat.codes
    
    return df_melted

def main():
    st.title("Analysis of Commodity Prices in Central Java")
    
    # Load Data
    with st.spinner('Loading and processing data...'):
        df_melted = load_and_preprocess_data()
    
    st.subheader("Processed Data Sample")
    st.dataframe(df_melted.head())
    
    # Regression Model
    X = df_melted[['Date_Ordinal', 'Komoditas_Code']]
    y = df_melted['Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    st.subheader("Model Performance (Multiple Linear Regression)")
    col1, col2 = st.columns(2)
    col1.metric("Mean Squared Error (MSE)", f"{mse:,.2f}")
    col2.metric("R-squared (R2) Score", f"{r2:.4f}")
    
    # Visualizations
    st.subheader("Visualizations")
    
    # 1. Price Trends
    st.write("#### Commodity Price Trends Over Time")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_melted, x='Date', y='Price', hue='Komoditas (Rp)', ax=ax1)
    ax1.set_title('Commodity Price Trends Over Time')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig1)
    
    # 2. Actual vs Predicted
    st.write("#### Actual vs Predicted Prices")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=y_pred, color='blue', alpha=0.5, ax=ax2)
    
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax2.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    ax2.set_xlabel('Actual Price')
    ax2.set_ylabel('Predicted Price')
    ax2.set_title('Actual vs Predicted Prices')
    ax2.legend()
    st.pyplot(fig2)

if __name__ == "__main__":
    main()
