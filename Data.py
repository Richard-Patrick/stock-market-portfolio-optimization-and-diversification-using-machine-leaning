import model.mining_company_data as mining_company_data
import model.mining_Stock_data as mining_stock_data
import model.data_preprocess as data_preprocess
if __name__ == "__main__":
    mining_company_data.company.get_data()
    mining_stock_data.Stock_data.get_data()
    data_preprocess.data_process.clean()