import csv
from collections import defaultdict
from datetime import datetime
from os import path
from typing import List, Dict, Union


class Trade:
    """
    Represents a trade.

    Attributes:
        trade_id (int): A unique identifier for each trade.
        customer_id (str): Identifier for the customer.
        trade_date (datetime): Date of the trade.
        ticker (str): Ticker symbol of the stock.
        trade_type (str): Type of trade - either BUY or SELL.
        quantity (int): Number of shares traded.
        price (float): Price of the stock at the time of the trade.
    """

    def __init__(
            self,
            trade_id: int,
            customer_id: str,
            trade_date: str,
            ticker: str,
            trade_type: str,
            quantity: int,
            price: float
    ):
        self.trade_id = trade_id
        self.customer_id = customer_id
        self.trade_date = datetime.strptime(trade_date, '%Y-%m-%d')
        self.ticker = ticker
        self.trade_type = trade_type
        self.quantity = quantity
        self.price = price


class TradeAnalyzer:
    def __init__(self, file_path: str):
        self.trades = self.load_trades(file_path)
        self.customer_trades = defaultdict(list)

    @staticmethod
    def load_trades(file_path: str) -> List[Trade]:
        """
        Loads trade data from a CSV file.

        Args:
            file_path (str): The path to the CSV file containing trade data.

        Returns:
            List[Trade]: A list of Trade objects.
        """
        trades = []
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    trade = Trade(
                        int(row['trade_id']),
                        row['customer_id'],
                        row['trade_date'],
                        row['ticker'],
                        row['trade_type'],
                        int(row['quantity']),
                        float(row['price'])
                    )
                    trades.append(trade)
        except FileNotFoundError as err:
            print(err)
        return trades

    def calculate_volume_by_ticker(self) -> Dict[str, Dict[str, int]]:
        """
        Calculates the total buying and selling volume for each ticker.

        Returns:
            Dict[str, Dict[str, int]]: A dictionary mapping ticker symbols to buy and sell volumes.
        """
        volume_by_ticker = defaultdict(lambda: defaultdict(int))
        for trade in self.trades:
            if trade.trade_type == 'BUY':
                volume_by_ticker[trade.ticker]['buy_volume'] += trade.quantity
            elif trade.trade_type == 'SELL':
                volume_by_ticker[trade.ticker]['sell_volume'] += trade.quantity
        return dict(volume_by_ticker)

    def identify_potential_discrepancies(self) -> List[Dict[str, Union[str, datetime.date, int]]]:
        """
        Identify customers with more than 3 trades in a single day.

        Returns:
            List[Dict[str, Union[str, datetime.date, int]]]: List of potential discrepancies.
        """
        for trade in self.trades:
            self.customer_trades[trade.customer_id].append(trade)

        potential_discrepancies = []
        for customer_id, trades in self.customer_trades.items():
            trade_dates = [trade.trade_date for trade in trades]
            date_counts = {date: trade_dates.count(date) for date in trade_dates}
            for date, count in date_counts.items():
                if count > 3:
                    potential_discrepancies.append({
                        'customer_id': customer_id,
                        'date': date.date(),
                        'trade_count': count
                    })
        return potential_discrepancies

    def calculate_average_price(self, ticker: str) -> float:
        """
        Calculate the average price for a given ticker on days it was traded.

        Args:
            ticker (str): Ticker symbol.

        Returns:
            float: Average price.
        """
        total_price = 0
        total_trades = 0
        for trade in self.trades:
            if trade.ticker == ticker:
                total_price += trade.price
                total_trades += 1
        if total_trades > 0:
            return total_price / total_trades
        else:
            return 0

    def get_trades_by_ticker_and_date(self, ticker: str, date: str) -> List:
        """
        Get a list of trades for a given ticker on the provided date.

        Args:
            ticker (str): Ticker symbol.
            date (str): Date in 'YYYY-MM-DD' format.

        Returns:
            List[Dict[str, Union[int, str, float, datetime.date]]]: List of trades.
        """
        target_date = datetime.strptime(date, '%Y-%m-%d')
        return [trade for trade in self.trades if trade.ticker == ticker and trade.trade_date == target_date]


# Example Usage:
if __name__ == '__main__':
    trade_filepath = path.join('files', 'trade_data.csv')
    analyzer = TradeAnalyzer(trade_filepath)
    analyzer.calculate_volume_by_ticker()
    potential_discrepancies = analyzer.identify_potential_discrepancies()
    avg_price_aapl = analyzer.calculate_average_price('AAPL')
    avg_price_googl = analyzer.calculate_average_price('GOOGL')
    trades_googl = analyzer.get_trades_by_ticker_and_date('GOOGL', '2023-08-02')
    trades_aapl = analyzer.get_trades_by_ticker_and_date('AAPL', '2023-08-01')

    volume_by_ticker = analyzer.calculate_volume_by_ticker()
    print("Total Buying and Selling Volume by Ticker:")
    for ticker, volume in volume_by_ticker.items():
        print(f"{ticker}: Buy - {volume['buy_volume']}, Sell - {volume['sell_volume']}")

    print("\nPotential Discrepancies:")
    for discrepancy in potential_discrepancies:
        print(
            f"Customer {discrepancy['customer_id']} has {discrepancy['trade_count']} trades on {discrepancy['date']}.")

    print(f"\nAverage Price for AAPL: {avg_price_aapl}")
    print(f"Average Price for GOOGL: {avg_price_googl}")

    print("\nTrades for APPL on 2023-08-01:")
    for trade in trades_aapl:
        print(
            f"Trade ID: {trade.trade_id}, Customer ID: {trade.customer_id}, Quantity: {trade.quantity}, Price: {trade.price}")
    print("\nTrades for GOOGL on 2023-08-02:")
    for trade in trades_googl:
        print(
            f"Trade ID: {trade.trade_id}, Customer ID: {trade.customer_id}, Quantity: {trade.quantity}, Price: {trade.price}")
