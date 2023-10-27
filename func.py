class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_sum_orders_df(self):
        sum_orders_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_orders_df.rename(columns={"product_id": "product_count"}, inplace=True)
        sum_orders_df = sum_orders_df.sort_values(by='product_count', ascending=False)
        return sum_orders_df
    
    def create_review_score_df(self):
        review_score_df = self.df['review_score'].value_counts().sort_values(ascending=False)
        return review_score_df
    
    def create_review_persentase_df(self):
        review_persentase_df = self.df['review_score'].value_counts().sort_values(ascending=False)
        return review_persentase_df
    
    def create_order_status_counts_df(self):
        order_status_counts_df = self.df["order_status"].value_counts().sort_values(ascending=False)
        return order_status_counts_df
    
    def create_state_counts_df(self):
        state_counts_df = self.df["customer_state"].value_counts().sort_values(ascending=False).head(15)
        return state_counts_df
    
    def create_city_counts_df(self):
        city_counts_df = self.df["customer_city"].value_counts().sort_values(ascending=False).head(15)
        return city_counts_df